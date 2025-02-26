// Initialize progress tracking
document.addEventListener('DOMContentLoaded', function() {
    updateWeeklyProgress();
});

// Update progress when form is submitted
document.getElementById('calorie-tracker').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        user_id: 1, // Replace with actual user ID management
        calories: parseInt(document.getElementById('calorie-intake').value),
        activity_level: document.getElementById('activity-level').value,
        water_intake: parseFloat(document.getElementById('water-intake').value),
        weight: parseFloat(document.getElementById('weight').value)
    };
    
    try {
        await logDailyProgress(formData);
        updateWeeklyProgress();
    } catch (error) {
        console.error('Error logging progress:', error);
    }
});

async function logDailyProgress(data) {
    const response = await fetch('/weekly-progress/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error('Failed to log progress');
    }
    
    return response.json();
}

async function updateWeeklyProgress() {
    try {
        const response = await fetch('/weekly-progress/1'); // Replace with actual user ID
        const data = await response.json();
        
        // Update progress boxes
        const boxes = document.querySelectorAll('.progress-box');
        data.daily_records.forEach((record, index) => {
            if (record.calories <= document.getElementById('calories-goal').value) {
                boxes[index].classList.add('filled');
            } else {
                boxes[index].classList.remove('filled');
            }
        });
        
        // Update statistics
        document.getElementById('avg-calories').textContent = 
            Math.round(data.avg_calories);
        document.getElementById('days-on-track').textContent = 
            data.daily_records.filter(r => r.calories <= document.getElementById('calories-goal').value).length;
    } catch (error) {
        console.error('Error updating progress:', error);
    }
} 