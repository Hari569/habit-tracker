# Habit Tracker Application

A full-stack habit tracking application built with FastAPI (backend) and React (frontend), integrated with LangGraph for natural language processing.

## Features

### Backend
- **FastAPI REST API** with comprehensive endpoints
- **SQLite Database** with SQLAlchemy ORM
- **JWT Authentication** for user management
- **LangGraph Integration** for natural language habit management
- **Analytics** with completion rates and streaks
- **CRUD Operations** for habits and completions

### Frontend
- **React SPA** with modern UI components
- **Tailwind CSS** for responsive design
- **Authentication** with JWT tokens
- **Daily View** for habit tracking
- **Analytics Dashboard** with charts
- **Real-time Updates** via API integration

## Project Structure

```
/
├── backend/
│   ├── routers/
│   │   ├── habits.py          # Habit CRUD endpoints
│   │   ├── completions.py     # Completion tracking
│   │   ├── analytics.py       # Analytics and insights
│   │   └── auth.py           # Authentication
│   ├── models/
│   │   ├── habit.py          # Habit database model
│   │   └── user.py           # User database model
│   ├── tools/
│   │   └── habit_tools.py    # LangGraph tools
│   ├── database.py           # Database configuration
│   ├── main.py              # FastAPI application
│   └── langgraph_setup.py   # LangGraph agent setup
├── frontend/
│   ├── public/
│   │   └── index.html       # Main HTML file
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # React context
│   │   ├── services/        # API service
│   │   └── App.jsx         # Main React component
│   └── tailwind.config.js  # Tailwind configuration
├── requirements.txt         # Python dependencies
├── start_backend.py        # Backend startup script
└── README.md              # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_jwt_secret_key_here
```

### 3. Start the Backend

```bash
python start_backend.py
```

This will:
- Create the SQLite database
- Start the FastAPI server on http://localhost:8000
- Enable auto-reload for development

### 4. Open the Frontend

Open `frontend/public/index.html` in your web browser, or serve it with a local server:

```bash
cd frontend/public
python -m http.server 3000
```

Then visit http://localhost:3000

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Habits
- `GET /api/habits/` - List all habits
- `POST /api/habits/` - Create new habit
- `GET /api/habits/{id}` - Get specific habit
- `PUT /api/habits/{id}` - Update habit
- `DELETE /api/habits/{id}` - Delete habit
- `GET /api/habits/date/{date}` - Get habits for specific date

### Completions
- `POST /api/completions/` - Mark habit as complete
- `GET /api/completions/` - List completions
- `DELETE /api/completions/` - Remove completion

### Analytics
- `GET /api/analytics/completion-rate` - Get completion rates
- `GET /api/analytics/streaks` - Get habit streaks
- `GET /api/analytics/summary` - Get analytics summary

## LangGraph Integration

The application includes a LangGraph agent that can process natural language commands for habit management. The agent can:

- Add new habits with natural language descriptions
- Mark habits as complete for specific dates
- Show habits scheduled for particular dates
- Delete habits when requested

### Example Usage

```python
from backend.langgraph_setup import process_message

# Add a new habit
response = process_message("Add a habit for reading every weekday #learning")

# Complete a habit
response = process_message("Mark the workout habit as complete for today")

# Show habits for a date
response = process_message("What habits do I have scheduled for tomorrow?")
```

## Development

### Backend Development

1. Make changes to Python files in the `backend/` directory
2. The server will auto-reload thanks to uvicorn's `--reload` flag
3. Test API endpoints at http://localhost:8000/docs

### Frontend Development

1. Edit React components in `frontend/src/`
2. Refresh your browser to see changes
3. For production builds, consider using a proper build system like Vite or Create React App

### Database Management

The SQLite database (`habits.db`) is created automatically. To reset the database:

```bash
rm habits.db
python start_backend.py
```

## Production Deployment

### Backend
- Deploy to platforms like Heroku, Railway, or Render
- Set environment variables for production
- Use PostgreSQL instead of SQLite for better performance

### Frontend
- Build static files and deploy to Netlify, Vercel, or similar
- Update API base URL in `frontend/src/services/api.js`
- Set up proper CORS configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the GitHub repository.