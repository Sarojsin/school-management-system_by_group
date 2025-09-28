// School Management Portal JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // Search functionality for tables
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const tableId = this.getAttribute('data-search');
            const table = document.getElementById(tableId);
            
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    });

    // Confirmation dialogs for delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-refresh dashboard data every 5 minutes
    if (window.location.pathname.includes('dashboard')) {
        setInterval(function() {
            // Only refresh if the page is visible
            if (!document.hidden) {
                refreshDashboardStats();
            }
        }, 300000); // 5 minutes
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            form.classList.add('was-validated');
        });
    });

    // Dynamic grade calculation for marks form
    const marksForm = document.querySelector('form[action*="add-marks"]');
    if (marksForm) {
        const marksObtained = marksForm.querySelector('#marks_obtained');
        const totalMarks = marksForm.querySelector('#total_marks');
        const gradeSelect = marksForm.querySelector('#grade');
        
        if (marksObtained && totalMarks && gradeSelect) {
            function calculateGrade() {
                const obtained = parseFloat(marksObtained.value);
                const total = parseFloat(totalMarks.value);
                
                if (obtained && total && total > 0) {
                    const percentage = (obtained / total) * 100;
                    let grade = 'F';
                    
                    if (percentage >= 90) grade = 'A+';
                    else if (percentage >= 85) grade = 'A';
                    else if (percentage >= 75) grade = 'B+';
                    else if (percentage >= 65) grade = 'B';
                    else if (percentage >= 55) grade = 'C+';
                    else if (percentage >= 45) grade = 'C';
                    else if (percentage >= 35) grade = 'D';
                    
                    gradeSelect.value = grade;
                    
                    // Add visual feedback
                    const percentageDisplay = document.getElementById('percentage-display');
                    if (percentageDisplay) {
                        percentageDisplay.textContent = percentage.toFixed(1) + '%';
                        percentageDisplay.className = 'badge ' + getGradeBadgeClass(grade);
                    }
                }
            }
            
            marksObtained.addEventListener('input', calculateGrade);
            totalMarks.addEventListener('input', calculateGrade);
        }
    }

    // Notice priority color coding
    updateNoticePriority();
});

// Helper functions
function refreshDashboardStats() {
    // This would typically make an AJAX call to refresh dashboard statistics
    console.log('Refreshing dashboard stats...');
}

function getGradeBadgeClass(grade) {
    const gradeClasses = {
        'A+': 'bg-success',
        'A': 'bg-success',
        'B+': 'bg-info',
        'B': 'bg-info',
        'C+': 'bg-warning',
        'C': 'bg-warning',
        'D': 'bg-secondary',
        'F': 'bg-danger'
    };
    return gradeClasses[grade] || 'bg-secondary';
}

function updateNoticePriority() {
    const priorityElements = document.querySelectorAll('[data-priority]');
    priorityElements.forEach(function(element) {
        const priority = element.getAttribute('data-priority');
        const classes = {
            'high': 'border-danger',
            'medium': 'border-warning',
            'low': 'border-info'
        };
        
        if (classes[priority]) {
            element.classList.add(classes[priority]);
        }
    });
}

// Chart initialization (if Chart.js is available)
function initializeCharts() {
    // Attendance Chart
    const attendanceCtx = document.getElementById('attendanceChart');
    if (attendanceCtx && typeof Chart !== 'undefined') {
        new Chart(attendanceCtx, {
            type: 'doughnut',
            data: {
                labels: ['Present', 'Absent', 'Late'],
                datasets: [{
                    data: [85, 10, 5],
                    backgroundColor: ['#198754', '#dc3545', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Performance Chart
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceCtx && typeof Chart !== 'undefined') {
        new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Average Score',
                    data: [78, 82, 85, 88, 86, 90],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
}

// Data export functionality
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = Array.from(table.querySelectorAll('tr'));
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => `"${cell.textContent.trim()}"`).join(',');
    }).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename || 'export.csv';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Print functionality
function printSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Print</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    @media print {
                        .no-print { display: none; }
                        body { margin: 0; padding: 20px; }
                    }
                </style>
            </head>
            <body>
                ${section.innerHTML}
                <script>window.print(); window.close();</script>
            </body>
        </html>
    `);
    printWindow.document.close();
}

// Theme switcher (for future dark mode implementation)
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.body.setAttribute('data-theme', savedTheme);
}