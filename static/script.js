// Function to show content with a fade effect
function showContent(url) {
    const contentDiv = document.getElementById('content');
    contentDiv.classList.add('opacity-0');
    setTimeout(() => {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                contentDiv.innerHTML = html;
                contentDiv.classList.remove('opacity-0');
            })
            .catch(error => {
                console.error('Error fetching content:', error);
                contentDiv.innerHTML = '<p>Error loading content. Please try again.</p>';
                contentDiv.classList.remove('opacity-0');
            });
    }, 300);
}

// Function to show data entry form
function showDataEntry() {
    showContent('/data_entry_form');
}

// Function to show data display
function showDataDisplay() {
    showContent('/data_display');
}

// Function to show matkul management
function showMatkulManagement() {
    showContent('/matkul_management');
}

// Function to submit data entry form
function submitDataEntry() {
    const form = document.getElementById('dataEntryForm');
    const formData = new FormData(form);

    fetch('/submit_data_entry', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        form.reset();
    })
    .catch(error => {
        console.error('Error submitting data:', error);
        alert('Error submitting data. Please try again.');
    });
}

// Function to submit new matkul
function submitMatkul() {
    const form = document.getElementById('matkulForm');
    const formData = new FormData(form);

    fetch('/submit_matkul', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        form.reset();
        showMatkulManagement();  // Refresh the matkul list
    })
    .catch(error => {
        console.error('Error submitting matkul:', error);
        alert('Error submitting mata kuliah. Please try again.');
    });
}

// Function to delete matkul
function deleteMatkul(matkulId) {
    if (confirm('Are you sure you want to delete this mata kuliah?')) {
        fetch(`/delete_matkul/${matkulId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            showMatkulManagement();  // Refresh the matkul list
        })
        .catch(error => {
            console.error('Error deleting matkul:', error);
            alert('Error deleting mata kuliah. Please try again.');
        });
    }
}

// Event listener for when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // You can add any initialization code here if needed
    console.log('DOM fully loaded and parsed');
});