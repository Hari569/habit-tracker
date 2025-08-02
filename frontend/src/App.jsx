const { BrowserRouter, Routes, Route, Link, Navigate } = ReactRouterDOM;

function App() {
  const [habits, setHabits] = React.useState([]);
  const [editingHabit, setEditingHabit] = React.useState(null);
  const [showHabitForm, setShowHabitForm] = React.useState(false);
  const { user, logout, loading, isAuthenticated } = useAuth();

  React.useEffect(() => {
    if (isAuthenticated) {
      loadHabits();
    }
  }, [isAuthenticated]);

  const loadHabits = async () => {
    try {
      const habitsData = await apiService.getHabits();
      setHabits(habitsData);
    } catch (error) {
      console.error('Error loading habits:', error);
    }
  };

  const handleSaveHabit = async (habitData) => {
    try {
      if (editingHabit) {
        await apiService.updateHabit(editingHabit.id, habitData);
      } else {
        await apiService.createHabit(habitData);
      }
      
      await loadHabits();
      setShowHabitForm(false);
      setEditingHabit(null);
    } catch (error) {
      console.error('Error saving habit:', error);
      throw error;
    }
  };

  const handleEditHabit = (habit) => {
    setEditingHabit(habit);
    setShowHabitForm(true);
  };

  const handleDeleteHabit = async (habitId) => {
    if (window.confirm('Are you sure you want to delete this habit?')) {
      try {
        await apiService.deleteHabit(habitId);
        await loadHabits();
      } catch (error) {
        console.error('Error deleting habit:', error);
        alert('Failed to delete habit');
      }
    }
  };

  const handleToggleComplete = async (habitId) => {
    const today = new Date().toISOString().split('T')[0];
    try {
      await apiService.completeHabit(habitId, today);
      alert('Habit marked as complete for today!');
    } catch (error) {
      console.error('Error completing habit:', error);
      alert('Failed to mark habit as complete');
    }
  };

  const handleCancelForm = () => {
    setShowHabitForm(false);
    setEditingHabit(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthForm />;
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="text-xl font-bold text-gray-900">
                  Habit Tracker
                </Link>
              </div>
              
              <div className="flex items-center space-x-4">
                <Link
                  to="/"
                  className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Habits
                </Link>
                <Link
                  to="/daily"
                  className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Daily View
                </Link>
                <Link
                  to="/analytics"
                  className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Analytics
                </Link>
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-700">
                    Welcome, {user?.full_name || user?.email}
                  </span>
                  <button
                    onClick={logout}
                    className="bg-red-500 hover:bg-red-700 text-white text-sm px-3 py-1 rounded"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route 
              path="/" 
              element={
                <HabitList
                  habits={habits}
                  onEdit={handleEditHabit}
                  onDelete={handleDeleteHabit}
                  onToggleComplete={handleToggleComplete}
                />
              } 
            />
            <Route path="/daily" element={<DailyView />} />
            <Route path="/analytics" element={<AnalyticsDashboard />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Habit Form Modal */}
        {showHabitForm && (
          <HabitForm
            habit={editingHabit}
            onSave={handleSaveHabit}
            onCancel={handleCancelForm}
          />
        )}
      </div>
    </BrowserRouter>
  );
}

// Main App with Auth Provider
function MainApp() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}

ReactDOM.render(<MainApp />, document.getElementById('root'));