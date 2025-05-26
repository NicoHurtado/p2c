/**
 * Simple course generation service for external API integration
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Generate a course using the external API
 * @param {Object} data - Course generation data
 * @param {string} data.prompt - The course topic/prompt
 * @param {string} data.experience_level - User's experience level
 * @param {string} data.personality - User's personality type
 * @param {string} data.learning_style - User's learning style
 * @param {string} data.intensity - Course intensity (optional, defaults to "medium")
 * @returns {Promise<Object>} Generated course data
 */
export async function generateCourse(data) {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/api/courses/generate-course`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            prompt: data.prompt,
            experience_level: data.experience_level,
            personality: data.personality,
            learning_style: data.learning_style,
            intensity: data.intensity || "medium"
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate course');
    }

    return await response.json();
}

/**
 * Example usage function
 */
export async function exampleUsage() {
    try {
        const courseData = {
            prompt: "Aprender Python para análisis de datos",
            experience_level: "beginner",
            personality: "analytical", 
            learning_style: "visual",
            intensity: "medium"
        };

        const course = await generateCourse(courseData);
        console.log('Generated course:', course);
        
        // Display course in UI
        // displayCourse(course);
        
    } catch (error) {
        console.error('Error generating course:', error.message);
        // Show error to user
        // showError(error.message);
    }
} 