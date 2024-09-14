let notificationDiv;
let notificationTimeout;

function checkNotifications() {
    fetch("/notifications")
        .then(response => response.json())
        .then(data => {
            if (!notificationDiv) {
                notificationDiv = document.getElementById("notifications");
            }

            if (data.upcoming_events && data.upcoming_events.length > 0) {
                showNotification(data.upcoming_events[0], 'event');
            } else if (data.message) {
                showNotification(data.message, 'message');
            } else {
                hideNotification();
            }
        })
        .catch(error => {
            console.error("Error fetching notifications:", error);
        });
}

function showNotification(content, type) {
    clearTimeout(notificationTimeout);
    
    let message;
    if (type === 'event') {
        message = `
            <h3 class="text-lg font-semibold mb-2 text-primary">Upcoming Event</h3>
            <p class="mb-2 text-gray-300">${content[1]} is happening at ${content[4]} on ${content[3]}</p>
        `;
    } else {
        message = `<p class="mb-2 text-gray-300">${content}</p>`;
    }

    notificationDiv.innerHTML = `
        ${message}
        <button id="closeNotification" class="text-sm text-gray-400 hover:text-gray-200">Dismiss</button>
    `;
    notificationDiv.classList.remove("hidden");
    notificationDiv.classList.add("animate-fade-in");

    document.getElementById("closeNotification").addEventListener("click", hideNotification);

    // Auto-hide notification after 10 seconds
    notificationTimeout = setTimeout(hideNotification, 10000);
}

function hideNotification() {
    if (notificationDiv) {
        notificationDiv.classList.add("animate-fade-out");
        setTimeout(() => {
            notificationDiv.classList.add("hidden");
            notificationDiv.classList.remove("animate-fade-out");
        }, 300);
    }
}

// Check for notifications every 30 seconds
const NOTIFICATION_INTERVAL = 30 * 1000;
setInterval(checkNotifications, NOTIFICATION_INTERVAL);

// Check immediately on page load
document.addEventListener("DOMContentLoaded", checkNotifications);

// Add these styles to your CSS or in a <style> tag in your HTML
const styles = `
    .animate-fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    .animate-fade-out {
        animation: fadeOut 0.3s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(20px); }
    }
`;

const styleElement = document.createElement("style");
styleElement.textContent = styles;
document.head.appendChild(styleElement);