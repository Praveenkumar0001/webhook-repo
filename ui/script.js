// Poll for events every 15 seconds
const POLL_INTERVAL = 15000;
let pollTimer = null;

// DOM elements
const eventsList = document.getElementById('events-list');
const noEventsMsg = document.getElementById('no-events');
const loadingMsg = document.getElementById('loading');
const errorMsg = document.getElementById('error');
const totalEventsEl = document.getElementById('total-events');
const lastUpdateEl = document.getElementById('last-update');
const refreshBtn = document.getElementById('refresh-btn');
const clearBtn = document.getElementById('clear-btn');

// Fetch and display events
async function fetchEvents() {
    try {
        loadingMsg.style.display = 'block';
        errorMsg.style.display = 'none';

        const response = await fetch('/api/events');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const events = await response.json();
        
        displayEvents(events);
        updateStats(events.length);
        
        loadingMsg.style.display = 'none';

    } catch (error) {
        console.error('Error fetching events:', error);
        showError('Failed to fetch events: ' + error.message);
        loadingMsg.style.display = 'none';
    }
}

// Display events in the UI
function displayEvents(events) {
    if (events.length === 0) {
        eventsList.innerHTML = '';
        noEventsMsg.style.display = 'block';
        return;
    }

    noEventsMsg.style.display = 'none';
    eventsList.innerHTML = '';

    events.forEach(event => {
        const eventCard = createEventCard(event);
        eventsList.appendChild(eventCard);
    });
}

// Create event card element
function createEventCard(event) {
    const card = document.createElement('div');
    card.className = 'event-card';

    const eventTime = formatTimestamp(event.timestamp);
    
    // Format message based on action type
    let message = '';
    if (event.action === 'PUSH') {
        message = `${event.author} pushed to ${event.to_branch} on ${eventTime}`;
    } else if (event.action === 'PULL_REQUEST') {
        message = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${eventTime}`;
    } else if (event.action === 'MERGE') {
        message = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${eventTime}`;
    }
    
    card.innerHTML = `
        <div class="event-header">
            <span class="event-type">${event.action || 'unknown'}</span>
            <span class="event-time">${eventTime}</span>
        </div>
        <div class="event-details">
            <div class="event-message">${message}</div>
            <div class="event-detail"><strong>Request ID:</strong> <span>${event.request_id || 'N/A'}</span></div>
        </div>
    `;

    return card;
}

// Format timestamp
function formatTimestamp(timestamp) {
    if (!timestamp) return 'Unknown time';
    
    const date = new Date(timestamp);
    
    // Format: "1st April 2021 - 9:30 PM UTC"
    const day = date.getUTCDate();
    const suffix = getDaySuffix(day);
    const month = date.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
    const year = date.getUTCFullYear();
    const time = date.toLocaleString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit', 
        hour12: true,
        timeZone: 'UTC'
    });
    
    return `${day}${suffix} ${month} ${year} - ${time} UTC`;
}

function getDaySuffix(day) {
    if (day > 3 && day < 21) return 'th';
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

// Update statistics
function updateStats(count) {
    totalEventsEl.textContent = count;
    lastUpdateEl.textContent = new Date().toLocaleTimeString();
}

// Show error message
function showError(message) {
    errorMsg.textContent = message;
    errorMsg.style.display = 'block';
}

// Start polling
function startPolling() {
    // Fetch immediately
    fetchEvents();
    
    // Then poll every 15 seconds
    pollTimer = setInterval(fetchEvents, POLL_INTERVAL);
}

// Stop polling
function stopPolling() {
    if (pollTimer) {
        clearInterval(pollTimer);
        pollTimer = null;
    }
}

// Event listeners
refreshBtn.addEventListener('click', () => {
    fetchEvents();
});

clearBtn.addEventListener('click', () => {
    eventsList.innerHTML = '';
    noEventsMsg.style.display = 'block';
    totalEventsEl.textContent = '0';
});

// Handle visibility change to pause/resume polling
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopPolling();
    } else {
        startPolling();
    }
});

// Start polling when page loads
startPolling();
