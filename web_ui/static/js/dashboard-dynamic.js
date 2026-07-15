// Portfolio Dashboard - Dynamic JavaScript
// Handles WebSocket updates, real-time filtering, and interactive features

const socket = io();
let currentPortfolioData = null;
let lobChart = null;
let geoChart = null;
let autoRefreshInterval = null;

// ============ INITIALIZATION ============

document.addEventListener('DOMContentLoaded', function() {
    initializeWebSocket();
    loadInitialData();
    setupAutoRefresh();
    setupFileUpload();
    loadFilterOptions();
});

// ============ WEBSOCKET SETUP ============

function initializeWebSocket() {
    socket.on('connect', function() {
        console.log('Connected to Portfolio Agent (WebSocket)');
        showToast('✅ Connected to Portfolio Agent', 'success');
        socket.emit('request_portfolio_update');
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from Portfolio Agent');
        showToast('⚠️ Disconnected from server', 'error');
    });

    socket.on('portfolio_data', function(data) {
        console.log('Received portfolio data:', data);
        updateDashboard(data);
    });

    socket.on('portfolio_updated', function(data) {
        console.log('Portfolio updated via upload:', data);
        showToast('📤 Portfolio data updated successfully!', 'success');
        loadInitialData();
    });

    socket.on('filter_updated', function(data) {
        console.log('Filters applied:', data);
        updateDashboard(data);
        showToast(`📊 Filters applied - ${data.treaty_count} treaties shown`, 'info');
    });

    socket.on('scenario_completed', function(data) {
        console.log('Scenario completed:', data);
        showToast(`✅ ${data.scenario_type} simulation completed!`, 'success');
    });

    socket.on('scenario_error', function(data) {
        console.log('Scenario error:', data);
        showToast(`❌ Simulation error: ${data.error}`, 'error');
    });
}

// ============ DATA LOADING ============

function loadInitialData() {
    fetch('/api/portfolio/summary')
        .then(response => response.json())
        .then(data => {
            console.log('Portfolio summary loaded:', data);
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error loading portfolio:', error);
            showToast('❌ Error loading portfolio data', 'error');
        });
}

function loadFilterOptions() {
    fetch('/api/portfolio')
        .then(response => response.json())
        .then(data => {
            // Populate LOB filter
            const lobSelect = document.getElementById('filterLob');
            data.lob_list.forEach(lob => {
                const option = document.createElement('option');
                option.value = lob;
                option.textContent = lob;
                lobSelect.appendChild(option);
            });

            // Populate Geography filter
            const geoSelect = document.getElementById('filterGeo');
            data.geography_list.forEach(geo => {
                const option = document.createElement('option');
                option.value = geo;
                option.textContent = geo;
                geoSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading filter options:', error));
}

// ============ DASHBOARD UPDATE ============

function updateDashboard(data) {
    // Update metrics
    const portfolioValue = data.portfolio_value || 0;
    const capitalUtil = data.capital_utilization || 0;
    const avgRorac = data.average_rorac || 0;
    const diversScore = data.diversification_score || 0;

    document.getElementById('portfolioValue').textContent = `$${(portfolioValue / 1000000).toFixed(1)}M`;
    document.getElementById('capitalUtil').textContent = `${capitalUtil.toFixed(1)}%`;
    document.getElementById('avgRorac').textContent = `${avgRorac.toFixed(1)}%`;
    document.getElementById('diversScore').textContent = diversScore.toFixed(2);

    // Update timestamp
    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();

    // Update charts if data contains LOB/Geography info
    if (data.by_lob) {
        updateLobChart(data.by_lob);
    }
    if (data.by_geography) {
        updateGeoChart(data.by_geography);
    }

    currentPortfolioData = data;
}

// ============ CHART MANAGEMENT ============

function updateLobChart(lobData) {
    const labels = Object.keys(lobData);
    const premiums = labels.map(lob => lobData[lob].premium);
    const roracs = labels.map(lob => lobData[lob].avg_rorac);

    const ctx = document.getElementById('lobChart');
    
    if (lobChart) {
        lobChart.destroy();
    }

    lobChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: premiums,
                backgroundColor: [
                    '#3498db',
                    '#2ecc71',
                    '#e74c3c',
                    '#f39c12',
                    '#9b59b6'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: { size: 11, weight: 'bold' }
                    }
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${percentage}%`;
                    },
                    color: '#fff',
                    font: { weight: 'bold' }
                }
            },
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    const lob = labels[elements[0].index];
                    document.getElementById('filterLob').value = lob;
                    applyDynamicFilter();
                }
            }
        }
    });
}

function updateGeoChart(geoData) {
    const labels = Object.keys(geoData);
    const premiums = labels.map(geo => geoData[geo].premium);

    const ctx = document.getElementById('geoChart');
    
    if (geoChart) {
        geoChart.destroy();
    }

    geoChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Premium ($)',
                data: premiums,
                backgroundColor: [
                    '#3498db',
                    '#2ecc71',
                    '#e74c3c',
                    '#f39c12',
                    '#9b59b6'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => `$${(value / 1000000).toFixed(1)}M`
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: { font: { weight: 'bold' } }
                }
            },
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    const geo = labels[elements[0].index];
                    document.getElementById('filterGeo').value = geo;
                    applyDynamicFilter();
                }
            }
        }
    });
}

// ============ DYNAMIC FILTERING ============

function applyDynamicFilter() {
    const lob = document.getElementById('filterLob').value;
    const geo = document.getElementById('filterGeo').value;
    const roacMin = parseFloat(document.getElementById('filterRoacMin').value) || null;
    const roacMax = parseFloat(document.getElementById('filterRoacMax').value) || null;

    const filterData = {
        lob: lob || null,
        geography: geo || null,
        rorac_min: roacMin,
        rorac_max: roacMax
    };

    // Send filter update via WebSocket for real-time broadcast
    socket.emit('request_live_filter', filterData);

    // Also send via API
    fetch('/api/filters/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filterData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Filter applied:', data);
        loadInitialData();
    })
    .catch(error => console.error('Error applying filters:', error));
}

function clearFilters() {
    document.getElementById('filterLob').value = '';
    document.getElementById('filterGeo').value = '';
    document.getElementById('filterRoacMin').value = '';
    document.getElementById('filterRoacMax').value = '';

    applyDynamicFilter();
    showToast('🔄 Filters cleared', 'info');
}

// ============ FILE UPLOAD ============

function openUploadModal() {
    const modal = new bootstrap.Modal(document.getElementById('uploadModal'));
    modal.show();
}

function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    uploadArea.addEventListener('click', () => fileInput.click());
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('uploadArea').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('uploadArea').classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('uploadArea').classList.remove('dragover');

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

function handleFileSelect(event) {
    if (event.target.files.length > 0) {
        uploadFile(event.target.files[0]);
    }
}

function uploadFile(file) {
    if (!file.name.endsWith('.csv')) {
        showToast('❌ Please upload a CSV file', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    showToast('📤 Uploading portfolio data...', 'info');

    fetch('/api/upload-portfolio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(`✅ ${data.message}`, 'success');
            bootstrap.Modal.getInstance(document.getElementById('uploadModal')).hide();
            setTimeout(loadInitialData, 1000);
        } else {
            showToast(`❌ ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        showToast('❌ Upload failed', 'error');
    });
}

// ============ REFRESH & AUTO-UPDATE ============

function refreshDashboard() {
    showToast('🔄 Refreshing dashboard...', 'info');
    loadInitialData();
    socket.emit('request_portfolio_update');
}

function setupAutoRefresh() {
    // Auto-refresh every 30 seconds
    autoRefreshInterval = setInterval(() => {
        socket.emit('request_portfolio_update');
    }, 30000);
}

// ============ NOTIFICATIONS ============

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-in-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ============ EXPORT HELPERS ============

function exportDashboardData() {
    if (!currentPortfolioData) {
        showToast('❌ No data to export', 'error');
        return;
    }

    const dataStr = JSON.stringify(currentPortfolioData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `portfolio-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}
