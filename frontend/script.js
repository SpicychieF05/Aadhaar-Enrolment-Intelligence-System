// Dashboard Logic for AEIS

const API_BASE_URL = 'http://localhost:5000/api';

// Check authentication
if (!sessionStorage.getItem('authenticated')) {
    window.location.href = 'auth.html';
}

let currentData = null;
let currentFilters = {};

// Accessibility Features
let fontSize = 16;

document.getElementById('fontIncrease')?.addEventListener('click', () => {
    fontSize += 2;
    document.body.style.fontSize = fontSize + 'px';
});

document.getElementById('fontDecrease')?.addEventListener('click', () => {
    if (fontSize > 12) {
        fontSize -= 2;
        document.body.style.fontSize = fontSize + 'px';
    }
});

document.getElementById('highContrast')?.addEventListener('click', () => {
    document.body.classList.toggle('high-contrast');
});

document.getElementById('printMode')?.addEventListener('click', () => {
    window.print();
});

// Data Loading
document.getElementById('loadDefaultData')?.addEventListener('click', async () => {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/load-default-data`, {
            method: 'POST'
        });
        const result = await response.json();

        if (result.success) {
            displayDataInfo(result.data_info);
            showSection('filtersSection');
            showSection('analyticsSection');
            showSection('anomalySection');
            showSection('exportSection');

            // Load initial analysis
            await loadAnalysis();
        } else {
            alert('Error loading data: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to backend. Please ensure the server is running.');
    } finally {
        showLoading(false);
    }
});

document.getElementById('uploadBtn')?.addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('uploadFilename').textContent = file.name;
        document.getElementById('processData').style.display = 'block';
    }
});

document.getElementById('processData')?.addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file first');
        return;
    }

    showLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload-data`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.success) {
            displayDataInfo(result.data_info);
            showSection('filtersSection');
            showSection('analyticsSection');
            showSection('anomalySection');
            showSection('exportSection');

            await loadAnalysis();
        } else {
            alert('Error processing file: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to upload file');
    } finally {
        showLoading(false);
    }
});

// Filters
document.getElementById('applyFilters')?.addEventListener('click', async () => {
    const pincodeValue = document.getElementById('pincodeFilter').value;
    currentFilters = {
        start_date: document.getElementById('startDate').value || undefined,
        end_date: document.getElementById('endDate').value || undefined,
        pincodes: pincodeValue ? [parseInt(pincodeValue)] : undefined,
        color_theme: document.getElementById('colorTheme').value,
        include_anomalies: false
    };

    await loadAnalysis();
});

document.getElementById('resetFilters')?.addEventListener('click', async () => {
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('pincodeFilter').selectedIndex = 0;
    document.getElementById('colorTheme').value = 'default';
    currentFilters = {};
    await loadAnalysis();
});

// Load Analysis
async function loadAnalysis() {
    showLoading(true);

    try {
        // Clean up filters - remove undefined values
        const cleanFilters = {};
        if (currentFilters.start_date) cleanFilters.start_date = currentFilters.start_date;
        if (currentFilters.end_date) cleanFilters.end_date = currentFilters.end_date;
        if (currentFilters.pincodes && currentFilters.pincodes.length > 0) {
            cleanFilters.pincodes = currentFilters.pincodes;
        }
        if (currentFilters.color_theme) cleanFilters.color_theme = currentFilters.color_theme;

        // Load analysis data
        const analysisResponse = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cleanFilters)
        });
        const analysisResult = await analysisResponse.json();

        if (analysisResult.success) {
            displaySummaryStats(analysisResult.analysis.summary);

            // Load visualizations
            const vizFilters = { ...cleanFilters, include_anomalies: false };
            const vizResponse = await fetch(`${API_BASE_URL}/visualizations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vizFilters)
            });
            const vizResult = await vizResponse.json();

            if (vizResult.success) {
                displayVisualizations(vizResult.visualizations);
            }

            // Load filter options
            await loadFilterOptions();
        } else {
            alert('Error loading analysis: ' + analysisResult.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load analysis');
    } finally {
        showLoading(false);
    }
}

// Display Functions
function displayDataInfo(info) {
    const container = document.getElementById('dataInfoContent');
    container.innerHTML = `
        <p><strong>Total Records:</strong> ${info.total_records}</p>
        <p><strong>Date Range:</strong> ${info.date_range.start} to ${info.date_range.end}</p>
        <p><strong>Districts:</strong> ${info.districts.join(', ')}</p>
        <p><strong>Unique Pincodes:</strong> ${info.pincodes_count}</p>
    `;
    document.getElementById('dataInfo').style.display = 'block';
}

function displaySummaryStats(summary) {
    document.getElementById('totalEnrolments').textContent = summary.total_enrolments.toLocaleString();
    document.getElementById('uniquePincodes').textContent = summary.unique_pincodes;
    document.getElementById('dateRange').textContent =
        `${summary.date_range.start} to ${summary.date_range.end}`;
    document.getElementById('dailyAverage').textContent =
        Math.round(summary.daily_statistics.mean).toLocaleString();
}

function displayVisualizations(viz) {
    document.getElementById('dailyEnrolmentsChart').src = viz.daily_enrolments;
    document.getElementById('ageDistributionChart').src = viz.age_distribution;
    document.getElementById('topPincodesChart').src = viz.top_pincodes;
    document.getElementById('monthlyTrendChart').src = viz.monthly_trend;
    document.getElementById('dayOfWeekChart').src = viz.day_of_week;
    document.getElementById('ageOverTimeChart').src = viz.age_over_time;
}

async function loadFilterOptions() {
    try {
        // Load pincodes
        const pincodesResponse = await fetch(`${API_BASE_URL}/filters/pincodes`);
        const pincodesResult = await pincodesResponse.json();

        if (pincodesResult.success) {
            const select = document.getElementById('pincodeFilter');
            select.innerHTML = '<option value="">All Pincodes</option>';
            pincodesResult.pincodes.forEach(pincode => {
                const option = document.createElement('option');
                option.value = pincode;
                option.textContent = pincode;
                select.appendChild(option);
            });
        }

        // Load date range
        const dateResponse = await fetch(`${API_BASE_URL}/filters/date-range`);
        const dateResult = await dateResponse.json();

        if (dateResult.success) {
            document.getElementById('startDate').min = dateResult.date_range.min;
            document.getElementById('startDate').max = dateResult.date_range.max;
            document.getElementById('endDate').min = dateResult.date_range.min;
            document.getElementById('endDate').max = dateResult.date_range.max;
        }
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

// Anomaly Detection
document.getElementById('runAnomalyDetection')?.addEventListener('click', async () => {
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/detect-anomalies`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentFilters)
        });
        const result = await response.json();

        if (result.success) {
            displayAnomalyResults(result.anomalies);

            // Generate anomaly visualization
            const vizFilters = { ...currentFilters, include_anomalies: true };
            const vizResponse = await fetch(`${API_BASE_URL}/visualizations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vizFilters)
            });
            const vizResult = await vizResponse.json();

            if (vizResult.success && vizResult.visualizations.anomalies) {
                document.getElementById('anomalyChart').src = vizResult.visualizations.anomalies;
            }
        } else {
            alert('Error detecting anomalies: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to detect anomalies');
    } finally {
        showLoading(false);
    }
});

function displayAnomalyResults(anomalies) {
    const summaryDiv = document.getElementById('anomalySummary');
    summaryDiv.innerHTML = `
        <h3>Anomaly Detection Summary</h3>
        <p><strong>Z-Score Anomalies Detected:</strong> ${anomalies.zscore_analysis.anomalies_found}</p>
        <p><strong>Rolling Window Anomalies:</strong> ${anomalies.rolling_analysis.anomalies_found}</p>
        <p><strong>Methodology:</strong> ${anomalies.methodology.description}</p>
    `;

    const explanationsDiv = document.getElementById('anomalyExplanations');
    explanationsDiv.innerHTML = '<h3>Top Anomalies Explained</h3>';

    anomalies.explanations.forEach(exp => {
        const item = document.createElement('div');
        item.className = 'anomaly-item';
        item.innerHTML = `
            <p><strong>Date:</strong> ${exp.date}</p>
            <p><strong>Enrolments:</strong> ${exp.enrolments}</p>
            <p>${exp.explanation}</p>
        `;
        explanationsDiv.appendChild(item);
    });

    document.getElementById('anomalyResults').style.display = 'block';
}

// Export Functions
document.getElementById('exportFullCSV')?.addEventListener('click', async () => {
    await exportData('full');
});

document.getElementById('exportSummaryCSV')?.addEventListener('click', async () => {
    await exportData('summary');
});

document.getElementById('exportAllCharts')?.addEventListener('click', async () => {
    await exportAllCharts();
});

async function exportAllCharts() {
    try {
        showLoading(true);

        // Get all chart images
        const charts = [
            { id: 'dailyEnrolmentsChart', name: 'daily_enrolments.png' },
            { id: 'ageDistributionChart', name: 'age_distribution.png' },
            { id: 'topPincodesChart', name: 'top_pincodes.png' },
            { id: 'monthlyTrendChart', name: 'monthly_trend.png' },
            { id: 'dayOfWeekChart', name: 'day_of_week.png' },
            { id: 'ageOverTimeChart', name: 'age_over_time.png' }
        ];

        let downloadCount = 0;
        for (const chart of charts) {
            const img = document.getElementById(chart.id);
            if (img && img.src && img.src.startsWith('data:image')) {
                const link = document.createElement('a');
                link.href = img.src;
                link.download = `aeis_${chart.name}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                downloadCount++;
                // Small delay between downloads
                await new Promise(resolve => setTimeout(resolve, 200));
            }
        }

        alert(`Successfully downloaded ${downloadCount} charts`);
    } catch (error) {
        console.error('Error exporting charts:', error);
        alert('Failed to export charts');
    } finally {
        showLoading(false);
    }
}

async function exportData(type) {
    try {
        const response = await fetch(`${API_BASE_URL}/export/csv`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type })
        });
        const result = await response.json();

        if (result.success) {
            const blob = new Blob([result.csv_data], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = result.filename;
            a.click();
        }
    } catch (error) {
        console.error('Error exporting:', error);
        alert('Failed to export data');
    }
}

// Export chart as PNG (delegate to handle dynamically loaded buttons)
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('export-btn')) {
        const chartType = e.target.dataset.chart;
        // Map chart type to image ID
        const chartIdMap = {
            'daily_enrolments': 'dailyEnrolmentsChart',
            'age_distribution': 'ageDistributionChart',
            'top_pincodes': 'topPincodesChart',
            'monthly_trend': 'monthlyTrendChart',
            'day_of_week': 'dayOfWeekChart',
            'age_over_time': 'ageOverTimeChart'
        };
        const imgId = chartIdMap[chartType];
        const img = document.getElementById(imgId);
        if (img && img.src && img.src.startsWith('data:image')) {
            // Convert base64 to blob for download
            const link = document.createElement('a');
            link.href = img.src;
            link.download = `aeis_${chartType}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert('Chart not yet loaded');
        }
    }
});

// Explanation toggles
document.querySelectorAll('.explanation-toggle').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const content = e.target.nextElementSibling;
        if (content.style.display === 'none' || !content.style.display) {
            content.style.display = 'block';
            e.target.textContent = '▼ Hide explanation';
        } else {
            content.style.display = 'none';
            e.target.textContent = 'ℹ️ How to interpret';
        }
    });
});

// Utility Functions
function showSection(sectionId) {
    document.getElementById(sectionId).style.display = 'block';
}

function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'p') {
        e.preventDefault();
        window.print();
    }
});
