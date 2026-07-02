const API_URL = "http://localhost:8000";

// Centralized request wrapper
async function makeRequest(endpoint, method = "GET", body = null, isMultipart = false) {
    const token = localStorage.getItem("access_token");
    const headers = {};

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    if (!isMultipart) {
        headers["Content-Type"] = "application/json";
    }

    const config = {
        method,
        headers
    };

    if (body) {
        if (isMultipart) {
            config.body = body;
        } else {
            config.body = JSON.stringify(body);
        }
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        
        // Handle token expiration
        if (response.status === 401) {
            localStorage.clear();
            if (!window.location.pathname.endsWith("login.html")) {
                window.location.href = "login.html";
            }
            throw new Error("Session expired. Please login again.");
        }
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }
        return data;
    } catch (error) {
        console.error("API request error:", error);
        throw error;
    }
}

// Global Auth checks
function checkAuth() {
    const token = localStorage.getItem("access_token");
    if (!token && !window.location.pathname.endsWith("login.html") && !window.location.pathname.endsWith("index.html")) {
        window.location.href = "login.html";
    }
}

document.addEventListener("DOMContentLoaded", checkAuth);
