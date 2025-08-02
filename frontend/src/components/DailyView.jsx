const DailyView = () => {
  const [selectedDate, setSelectedDate] = React.useState(new Date().toISOString().split('T')[0]);
  const [habitsForDate, setHabitsForDate] = React.useState([]);
  const [completions, setCompletions] = React.useState(new Set());
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    loadHabitsForDate();
  }, [selectedDate]);

  const loadHabitsForDate = async () => {
    setLoading(true);
    try {
      const habits = await apiService.getHabitsForDate(selectedDate);
      setHabitsForDate(habits);
      
      // Load completions to show current status
      const allCompletions = await apiService.getCompletions();
      const completionsForDate = new Set(
        allCompletions
          .filter(c => c.completion_date === selectedDate)
          .map(c => c.habit_id)
      );
      setCompletions(completionsForDate);
    } catch (error) {
      console.error('Error loading habits for date:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleHabitCompletion = async (habitId) => {
    try {
      if (completions.has(habitId)) {
        await apiService.uncompleteHabit(habitId, selectedDate);
        setCompletions(prev => {
          const newSet = new Set(prev);
          newSet.delete(habitId);
          return newSet;
        });
      } else {
        await apiService.completeHabit(habitId, selectedDate);
        setCompletions(prev => new Set([...prev, habitId]));
      }
    } catch (error) {
      console.error('Error toggling habit completion:', error);
      alert('Failed to update habit completion');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getCompletionStats = () => {
    const total = habitsForDate.length;
    const completed = completions.size;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { total, completed, percentage };
  };

  const stats = getCompletionStats();

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Daily View</h2>
        
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div>
            <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
              Select Date
            </label>
            <input
              type="date"
              id="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-600">{stats.percentage}%</div>
            <div className="text-sm text-gray-600">
              {stats.completed} of {stats.total} completed
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Habits for {formatDate(selectedDate)}
        </h3>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading habits...</p>
          </div>
        ) : habitsForDate.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">No habits scheduled for this date</p>
          </div>
        ) : (
          <div className="space-y-3">
            {habitsForDate.map((habit) => {
              const isCompleted = completions.has(habit.id);
              return (
                <div
                  key={habit.id}
                  className={`flex items-center justify-between p-4 rounded-lg border-2 transition-colors ${
                    isCompleted
                      ? 'bg-green-50 border-green-200'
                      : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => toggleHabitCompletion(habit.id)}
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                        isCompleted
                          ? 'bg-green-500 border-green-500 text-white'
                          : 'border-gray-300 hover:border-green-500'
                      }`}
                    >
                      {isCompleted && (
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </button>
                    
                    <div>
                      <h4 className={`font-medium ${isCompleted ? 'text-green-800 line-through' : 'text-gray-900'}`}>
                        {habit.name}
                      </h4>
                      {habit.tags && (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {habit.tags.split(',').filter(tag => tag.trim()).map((tag, index) => (
                            <span key={index} className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded">
                              #{tag.trim()}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className={`text-sm font-medium ${isCompleted ? 'text-green-600' : 'text-gray-500'}`}>
                    {isCompleted ? 'Completed' : 'Pending'}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};