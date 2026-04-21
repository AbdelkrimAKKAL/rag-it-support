// Initialize Lucide icons
lucide.createIcons();

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const chatForm = document.getElementById("chat-form");
const sendBtn = document.getElementById("send-btn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const toggleSidebarBtn = document.getElementById("toggle-sidebar");
const closeSidebarBtn = document.getElementById("close-sidebar");
const newChatBtn = document.getElementById("new-chat-btn");
const topicBtns = document.querySelectorAll(".topic-btn");

// Toggle sidebar on mobile
toggleSidebarBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
});

closeSidebarBtn.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
});

overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
});

// Handle topic selection
topicBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        topicBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    });
});

// New chat
newChatBtn.addEventListener("click", () => {
    chatMessages.innerHTML = `
        <div class="message bot">
            <div class="avatar bot-avatar">
                <i data-lucide="bot" size="24"></i>
            </div>
            <div class="bubble">
                Bonjour! Je suis votre assistant IT Support. Je peux vous aider avec des questions sur le réseau, Active Directory, les imprimantes, et bien plus. Comment puis-je vous aider aujourd'hui?
            </div>
        </div>
    `;
    lucide.createIcons();
});

// Send message
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, "user");
    userInput.value = "";
    
    // Show loading state
    sendBtn.disabled = true;
    
    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Add bot response to chat
        addMessage(data.response, "bot", data.sources);
        
    } catch (error) {
        console.error("Error:", error);
        addMessage(
            "Désolé, une erreur s'est produite. Veuillez réessayer.",
            "bot"
        );
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
});

function addMessage(content, role, sources = []) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    
    const avatarDiv = document.createElement("div");
    avatarDiv.className = `avatar ${role === "bot" ? "bot-avatar" : ""}`;
    
    if (role === "bot") {
        avatarDiv.innerHTML = '<i data-lucide="bot" size="24"></i>';
    } else {
        avatarDiv.innerHTML = '<i data-lucide="user" size="24"></i>';
    }
    
    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "bubble";
    bubbleDiv.textContent = content;
    
    if (role === "bot") {
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);
        
        if (sources.length > 0) {
            const sourcesDiv = document.createElement("div");
            sourcesDiv.className = "message-sources";
            sourcesDiv.textContent = `Sources: ${sources.slice(0, 2).join(", ")}`;
            bubbleDiv.appendChild(sourcesDiv);
        }
    } else {
        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(avatarDiv);
    }
    
    chatMessages.appendChild(messageDiv);
    lucide.createIcons();
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Auto-focus input on page load
userInput.focus();
