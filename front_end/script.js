// ⚠️ CHANGE THIS TO YOUR BACKEND URL
const API_BASE_URL = 'http://127.0.0.1:8080';

// Global variables
let trips = [];
let hourlyChart, weekdayChart;

// Toggle filters panel
function toggleFilters() {
    const panel = document.getElementById('filterPanel');
    panel.classList.toggle('hidden');
}

// Fetch overall statistics
async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const stats = await response.json();
        
        // Update stats cards
        document.getElementById('totalTrips').textContent = stats.total_trips.toLocaleString();
        document.getElementById('avgDistance').textContent = stats.avg_trip_distance_km + ' km';
        document.getElementById('avgSpeed').textContent = stats.avg_trip_speed_kmh + ' km/h';
        document.getElementById('avgDuration').textContent = Math.round(stats.avg_trip_duration_sec / 60) + ' min';
        
    } catch (error) {
        console.error('Error fetching stats:', error);
        alert('Failed to connect to backend. Make sure your API is running at ' + API_BASE_URL);
    }
}

// Fetch trips with filters
async function fetchTrips() {
    // Show loading state
    document.getElementById('loadingDiv').classList.remove('hidden');
    document.getElementById('tableDiv').classList.add('hidden');

    try {
        const params = new URLSearchParams();
        
        // Get all filter values
        const filterIds = [
            'limit', 
            'pickup_hour', 
            'pickup_weekday', 
            'time_of_day', 
            'min_speed', 
            'max_speed', 
            'min_distance', 
            'max_distance'
        ];
        
        filterIds.forEach(filterId => {
            const value = document.getElementById(filterId).value;
            if (value !== '' && value !== null) {
                params.append(filterId, value);
            }
        });

        const response = await fetch(`${API_BASE_URL}/api/trips?${params}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        trips = await response.json();
        
        // Display results
        displayTrips();
        updateCharts();
        
        // Hide loading, show table
        document.getElementById('loadingDiv').classList.add('hidden');
        document.getElementById('tableDiv').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error fetching trips:', error);
        alert('Failed to fetch trips. Check console for details and make sure backend is running.');
        document.getElementById('loadingDiv').classList.add('hidden');
    }
}

// Display trips in table
function displayTrips() {
    const tbody = document.getElementById('tripsTableBody');
    tbody.innerHTML = '';
    
    // Update count
    document.getElementById('tripCount').textContent = trips.length;

    // Populate table rows
    trips.forEach(trip => {
        const row = tbody.insertRow();
        
        const pickupDate = new Date(trip.pickup_datetime);
        const formattedDate = pickupDate.toLocaleString();
        
        row.innerHTML = `
            <td>${formattedDate}</td>
            <td>${Math.round(trip.trip_duration / 60)} min</td>
            <td>${trip.trip_distance_km?.toFixed(2)} km</td>
            <td>${trip.trip_speed_kmh?.toFixed(1)} km/h</td>
            <td>${trip.passenger_count}</td>
            <td><span class="badge">${trip.time_of_day || 'N/A'}</span></td>
        `;
    });
}

// Update charts with current trip data
function updateCharts() {
    updateHourlyChart();
    updateWeekdayChart();
}

// Update hourly distribution chart
function updateHourlyChart() {
    // Count trips by hour
    const hourCounts = {};
    trips.forEach(trip => {
        const hour = trip.pickup_hour;
        if (hour !== null && hour !== undefined) {
            hourCounts[hour] = (hourCounts[hour] || 0) + 1;
        }
    });

    // Prepare data for chart
    const sortedHours = Object.keys(hourCounts).sort((a, b) => a - b);
    const hourLabels = sortedHours.map(h => `${h}:00`);
    const hourData = sortedHours.map(h => hourCounts[h]);

    // Destroy existing chart if it exists
    if (hourlyChart) {
        hourlyChart.destroy();
    }

    // Create new chart
    const ctx = document.getElementById('hourlyChart').getContext('2d');
    hourlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourLabels,
            datasets: [{
                label: 'Number of Trips',
                data: hourData,
                backgroundColor: '#8b5cf6',
                borderRadius: 8,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { 
                    display: false 
                },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#e2e8f0',
                    bodyColor: '#cbd5e1',
                    borderColor: '#475569',
                    borderWidth: 1
                }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: { 
                        color: '#94a3b8',
                        font: { size: 12 }
                    },
                    grid: { 
                        color: '#475569',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: { 
                        color: '#94a3b8',
                        font: { size: 12 }
                    },
                    grid: { 
                        color: '#475569',
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// Update weekday distribution chart
function updateWeekdayChart() {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const dayCounts = [0, 0, 0, 0, 0, 0, 0];
    
    // Count trips by weekday
    trips.forEach(trip => {
        if (trip.pickup_weekday !== null && trip.pickup_weekday !== undefined) {
            dayCounts[trip.pickup_weekday]++;
        }
    });

    // Destroy existing chart if it exists
    if (weekdayChart) {
        weekdayChart.destroy();
    }

    // Create new chart
    const ctx = document.getElementById('weekdayChart').getContext('2d');
    weekdayChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: days,
            datasets: [{
                label: 'Number of Trips',
                data: dayCounts,
                backgroundColor: '#3b82f6',
                borderRadius: 8,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { 
                    display: false 
                },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#e2e8f0',
                    bodyColor: '#cbd5e1',
                    borderColor: '#475569',
                    borderWidth: 1
                }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: { 
                        color: '#94a3b8',
                        font: { size: 12 }
                    },
                    grid: { 
                        color: '#475569',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: { 
                        color: '#94a3b8',
                        font: { size: 12 }
                    },
                    grid: { 
                        color: '#475569',
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// Apply filters button handler
function applyFilters() {
    fetchTrips();
}

// Reset filters button handler
function resetFilters() {
    document.getElementById('limit').value = '100';
    document.getElementById('pickup_hour').value = '';
    document.getElementById('pickup_weekday').value = '';
    document.getElementById('time_of_day').value = '';
    document.getElementById('min_speed').value = '';
    document.getElementById('max_speed').value = '';
    document.getElementById('min_distance').value = '';
    document.getElementById('max_distance').value = '';
    
    // Fetch trips with reset filters
    fetchTrips();
}

// Initialize dashboard when page loads
window.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized. Connecting to:', API_BASE_URL);
    fetchStats();
    fetchTrips();
});