// Handles Login and Sign Up submissions
async function handleLogin(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Login failed");
        }
        
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user_role", data.role);
        localStorage.setItem("user_name", data.name);
        
        // Redirect based on role
        if (data.role === "doctor") {
            window.location.href = "dashboard.html";
        } else {
            window.location.href = "dashboard.html";
        }
    } catch (error) {
        alert(error.message);
    }
}

async function handleRegister(name, email, password, phone, role, state, district) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, password, phone, role, state, district })
        });
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Registration failed");
        }
        
        alert("Registration successful! Please login.");
        // Switch to login form tab
        document.getElementById("login-tab").click();
    } catch (error) {
        alert(error.message);
    }
}

function handleLogout() {
    localStorage.clear();
    window.location.href = "index.html";
}

// Update navbar elements based on Auth State
function updateNavbar() {
    const token = localStorage.getItem("access_token");
    const name = localStorage.getItem("user_name");
    const profileLink = document.getElementById("profileLink");
    const profileDropdown = document.getElementById("profileDropdown");
    
    if (token && profileLink && profileDropdown) {
        profileLink.textContent = name ? name.toUpperCase() : "DASHBOARD";
        profileLink.href = "dashboard.html";
        
        // Populate profile dropdown with logout option
        profileDropdown.innerHTML = `
            <a href="dashboard.html" style="padding: 10px; display: block;">Dashboard</a>
            <a href="chatbot.html" style="padding: 10px; display: block;">AI Chatbot</a>
            <a href="report-analyzer.html" style="padding: 10px; display: block;">Report Analyzer</a>
            <a href="predict.html" style="padding: 10px; display: block;">Symptom Checker</a>
            <a href="hospital-finder.html" style="padding: 10px; display: block;">Hospital Finder</a>
            <a href="#" onclick="handleLogout()" style="padding: 10px; display: block; color: #ff5252;">Logout</a>
        `;
    }
}

document.addEventListener("DOMContentLoaded", updateNavbar);
