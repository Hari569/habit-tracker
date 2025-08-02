const HabitList = ({ habits, onEdit, onDelete, onToggleComplete }) => {
  const getDaysOfWeek = (repeatFrequency) => {
    if (!repeatFrequency) return [];
    return repeatFrequency.split(',').map(day => day.charAt(0) + day.slice(1).toLowerCase());
  };

  const formatTags = (tags) => {
    if (!tags) return [];
    return tags.split(',').filter(tag => tag.trim());
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Your Habits</h2>
        <button
          onClick={() => onEdit(null)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Add New Habit
        </button>
      </div>

      {habits.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500">No habits yet. Create your first habit!</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {habits.map((habit) => (
            <div key={habit.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{habit.name}</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={() => onEdit(habit)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onDelete(habit.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Repeat:</p>
                  <div className="flex flex-wrap gap-1">
                    {getDaysOfWeek(habit.repeat_frequency).map((day) => (
                      <span key={day} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                        {day}
                      </span>
                    ))}
                  </div>
                </div>

                {habit.tags && (
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Tags:</p>
                    <div className="flex flex-wrap gap-1">
                      {formatTags(habit.tags).map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <button
                  onClick={() => onToggleComplete(habit.id)}
                  className="w-full mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  Mark Complete Today
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};