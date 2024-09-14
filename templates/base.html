<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}EventMaster{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Tailwind configuration
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#4F46E5', // Indigo
                        secondary: '#7C3AED', // Purple
                        background: '#F3F4F6', // Light gray
                        surface: '#FFFFFF', // White
                        text: '#1F2937', // Dark gray
                        accent: '#10B981', // Emerald green
                    },
                    fontFamily: {
                        sans: ['Poppins', 'sans-serif'],
                    },
                },
            },
        }
    </script>
    <style>
        /* Global styles */
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #F3F4F6;
            color: #1F2937;
        }
        /* Animation for fade-in effect */
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Hover effect for interactive elements */
        .hover-lift {
            transition: transform 0.3s ease-out;
        }
        .hover-lift:hover {
            transform: translateY(-3px);
        }
    </style>
</head>
<body class="flex h-screen bg-background">
    <!-- Sidebar Navigation -->
    <aside class="w-64 bg-surface shadow-lg">
        <div class="p-4">
            <h1 class="text-2xl font-bold text-primary">EventMaster</h1>
        </div>
        <nav class="mt-8">
            <a href="{{ url_for('index') }}" class="block py-2 px-4 text-gray-600 hover:bg-primary hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
                Dashboard
            </a>
            <a href="{{ url_for('list_events') }}" class="block py-2 px-4 text-gray-600 hover:bg-primary hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
                Events
            </a>
            <a href="{{ url_for('create_event') }}" class="block py-2 px-4 text-gray-600 hover:bg-primary hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                </svg>
                Create Event
            </a>
            <a href="{{ url_for('activity_logs') }}" class="block py-2 px-4 text-gray-600 hover:bg-primary hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                </svg>
                Activity Logs
            </a>
        </nav>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top Navigation Bar -->
        <header class="bg-surface shadow-sm">
            <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                <h1 class="text-2xl font-semibold text-gray-900">{% block header %}Dashboard{% endblock %}</h1>
            </div>
        </header>

        <!-- Main Content -->
        <main class="flex-1 overflow-x-hidden overflow-y-auto bg-background">
            <div class="container mx-auto px-6 py-8">
                {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                {% for category, message in messages %}
                <div class="mb-4 p-4 rounded {% if category == 'success' %}bg-green-100 text-green-700{% else %}bg-red-100 text-red-700{% endif %} animate-fade-in">
                    {{ message }}
                </div>
                {% endfor %}
                {% endif %}
                {% endwith %}

                {% block content %}{% endblock %}
            </div>
        </main>

        <!-- Footer -->
        <footer class="bg-surface text-center py-4 text-sm text-gray-600">
            &copy; 2023 EventMaster. All rights reserved.
        </footer>
    </div>

    <!-- Notification Area -->
    <div id="notifications" class="fixed bottom-4 right-4 w-64 bg-surface rounded shadow-lg p-4 hidden"></div>

    <!-- Load JavaScript -->
    <script src="{{ url_for('static', filename='js/notifications.js') }}"></script>
</body>
</html>
