import os
from typing import Annotated, List, Literal, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from tools.habit_tools import tools
import sqlite3

# Initialize LLM
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
llm = llm.bind_tools(tools)

class AppState(TypedDict):
    messages: Annotated[list, add_messages]
    habits: List[dict]

SYSTEM_TEMPLATE = PromptTemplate.from_template(
    """You are a helpful habit tracking assistant. You can help users manage their habits by:
    - Adding new habits with specific repeat schedules
    - Marking habits as completed for specific dates
    - Showing habits scheduled for specific dates
    - Deleting habits when requested

Current habits in the system:
{habits}

Always be helpful and provide clear feedback about the actions you take.
"""
)

def get_habits_from_db():
    """Get all habits from the database"""
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, repeat_frequency, tags FROM habits")
    habits = []
    for row in cursor.fetchall():
        habits.append({
            "id": row[0],
            "name": row[1],
            "repeat_frequency": row[2],
            "tags": row[3].split(",") if row[3] else []
        })
    conn.close()
    return habits

def update_habits(state: AppState):
    """Update the habits in the state from the database"""
    return {"habits": get_habits_from_db()}

def call_model(state: AppState):
    """Call the LLM with the current state"""
    messages = state["messages"]
    system_message = SystemMessage(SYSTEM_TEMPLATE.format(habits=state["habits"]))
    
    # Insert system message at the beginning if not already there
    if not messages or messages[0].type != "system":
        messages.insert(0, system_message)
    else:
        messages[0] = system_message
    
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AppState) -> Literal["tools", END]:
    """Determine whether to continue to tools or end"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Create the graph
graph = StateGraph(AppState)

# Add nodes
graph.add_node("update_habits", update_habits)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))

# Add edges
graph.add_edge("update_habits", "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "update_habits")

# Set entry point
graph.set_entry_point("update_habits")

# Create checkpointer for persistence
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Compile the graph
app = graph.compile(checkpointer=checkpointer)

def process_message(message: str, thread_id: str = "default"):
    """Process a message through the LangGraph agent"""
    config = {"configurable": {"thread_id": thread_id}}
    
    state = app.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    return state["messages"][-1].content