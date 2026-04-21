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
const suggestionChips = document.querySelectorAll(".suggestion-chip");

// Variables pour l'indicateur de frappe
let typingIndicatorDiv = null;

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

// Affiche l'indicateur "bot écrit..."
function showTypingIndicator() {
    if (!typingIndicatorDiv) {
        typingIndicatorDiv = document.createElement("div");
        typingIndicatorDiv.className = "message bot typing";
        typingIndicatorDiv.innerHTML = `
            <div class="avatar bot-avatar">
                <i data-lucide="bot" size="24"></i>
            </div>
            <div class="bubble typing-bubble">
                <span></span><span></span><span></span>
            </div>
        `;
    }
    if (!typingIndicatorDiv.parentNode) {
        chatMessages.appendChild(typingIndicatorDiv);
        lucide.createIcons();
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function hideTypingIndicator() {
    if (typingIndicatorDiv && typingIndicatorDiv.parentNode) {
        typingIndicatorDiv.remove();
    }
}

async function sendMessage(message) {
    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error(`API error: ${response.statusText}`);

        const data = await response.json();

        hideTypingIndicator();
        addMessage(data.response, "bot");
    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        addMessage("Désolé, une erreur s'est produite. Veuillez réessayer.", "bot");
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    await sendMessage(message);
});

suggestionChips.forEach((chip) => {
    chip.addEventListener("click", async () => {
        const question = chip.getAttribute("data-question");
        if (question) {
            await sendMessage(question);
            if (window.innerWidth <= 768) {
                sidebar.classList.remove("active");
                overlay.classList.remove("active");
            }
        }
    });
});

function addMessage(content, role) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatarDiv = document.createElement("div");
    avatarDiv.className = `avatar ${role === "bot" ? "bot-avatar" : ""}`;
    avatarDiv.innerHTML = role === "bot" ? '<i data-lucide="bot" size="24"></i>' : '<i data-lucide="user" size="24"></i>';

    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "bubble";

    if (role === "bot") {
        let formatted = content
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        bubbleDiv.innerHTML = formatted;
    } else {
        bubbleDiv.textContent = content;
    }

    if (role === "bot") {
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);
    } else {
        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(avatarDiv);
    }

    chatMessages.appendChild(messageDiv);
    lucide.createIcons();
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

userInput.focus();