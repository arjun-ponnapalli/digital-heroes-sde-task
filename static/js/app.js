document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyze-form');
    const urlInput = document.getElementById('url-input');
    const submitBtn = document.getElementById('analyze-btn');
    
    // UI Sections
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const resultsDashboard = document.getElementById('results-dashboard');
    
    // Result Elements
    const resultUrl = document.getElementById('result-url');
    const valStatus = document.getElementById('val-status');
    const valTime = document.getElementById('val-time');
    const valH1 = document.getElementById('val-h1');
    const valAlt = document.getElementById('val-alt');
    const valWords = document.getElementById('val-words');
    const valTitle = document.getElementById('val-title');
    const valDescription = document.getElementById('val-description');
    
    // Error Elements
    const errorMessage = document.getElementById('error-message');
    
    // Get CSRF Token from cookies (standard Django setup)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    function hideAllSections() {
        loadingState.classList.add('hidden');
        errorState.classList.add('hidden');
        resultsDashboard.classList.add('hidden');
    }
    
    function showError(message) {
        hideAllSections();
        errorMessage.textContent = message;
        errorState.classList.remove('hidden');
    }
    
    function updateDashboard(data, targetUrl) {
        resultUrl.textContent = `Analyzed: ${targetUrl}`;
        
        // Update metric values
        valStatus.textContent = data.http_status_code;
        valTime.textContent = `${data.response_time_ms} ms`;
        valH1.textContent = data.h1_count;
        valAlt.textContent = data.missing_alt_count;
        valWords.textContent = data.word_count.toLocaleString(); // Format with commas
        
        // Text metrics
        valTitle.textContent = data.page_title;
        valDescription.textContent = data.meta_description;
        
        // Color code status
        if (data.http_status_code >= 200 && data.http_status_code < 300) {
            valStatus.style.color = 'var(--success-text)';
        } else {
            valStatus.style.color = 'var(--error-text)';
        }
        
        hideAllSections();
        resultsDashboard.classList.remove('hidden');
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const targetUrl = urlInput.value.trim();
        if (!targetUrl) return;
        
        // UI Loading State
        hideAllSections();
        loadingState.classList.remove('hidden');
        submitBtn.disabled = true;
        
        try {
            const csrfToken = getCookie('csrftoken') || '';
            
            const response = await fetch('/api/analyze/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ url: targetUrl })
            });
            
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const result = await response.json();
                
                if (response.ok && result.success) {
                    updateDashboard(result.data, targetUrl);
                } else {
                    const msg = result.message || 'An unknown error occurred while analyzing the URL.';
                    showError(msg);
                }
            } else {
                const text = await response.text();
                console.error("Non-JSON response:", text);
                showError("Server returned an unexpected response (not JSON). Please check the server logs.");
            }
            
        } catch (error) {
            console.error('Fetch error:', error);
            showError('Network error: ' + error.message);
        } finally {
            submitBtn.disabled = false;
        }
    });
});
