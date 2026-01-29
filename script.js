// Configuration - Now using Python backend
const API_URL = 'http://localhost:5000/api';
const chatbotConfig = {
    name: 'MyBot',
    version: '2.0',
};

// State Management
let chatState = {
    currentTone: 'friendly',
    responseLength: 'medium',
    knowledgeLevel: 'intermediate',
    emojiUsage: 'some',
    darkMode: false,
    soundEnabled: true,
    autoSave: true,
    animationEnabled: true,
    conversationHistory: [],
    currentUser: 'User',
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    initializeEventListeners();
    setupTheme();
    addWelcomeMessage();
    checkBackendHealth();
});

// Check if backend is running
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected!');
        }
    } catch (error) {
        console.warn('⚠️ Backend not running. Using offline mode.');
    }
}

// Event Listeners
function initializeEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', handleNavigation);
    });

    // Chat
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    document.getElementById('sendBtn').addEventListener('click', sendMessage);

    // Personality Settings
    document.getElementById('toneSelect').addEventListener('change', updateTone);
    document.getElementById('lengthSelect').addEventListener('change', updateLength);
    document.getElementById('levelSelect').addEventListener('change', updateLevel);
    document.getElementById('emojiSelect').addEventListener('change', updateEmoji);

    // General Settings
    document.getElementById('darkModeToggle').addEventListener('change', toggleDarkMode);
    document.getElementById('soundToggle').addEventListener('change', (e) => {
        chatState.soundEnabled = e.target.checked;
        saveSettings();
    });
    document.getElementById('autoSaveToggle').addEventListener('change', (e) => {
        chatState.autoSave = e.target.checked;
        saveSettings();
    });
    document.getElementById('animationToggle').addEventListener('change', (e) => {
        chatState.animationEnabled = e.target.checked;
        saveSettings();
    });

    // Action Buttons
    document.getElementById('clearHistoryBtn').addEventListener('click', clearHistory);
    document.getElementById('exportBtn').addEventListener('click', exportConversations);
}

// Navigation Handler
function handleNavigation(e) {
    const mode = e.currentTarget.dataset.mode;
    
    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    // Update active section
    document.querySelectorAll('main > section').forEach(section => {
        section.classList.remove('active');
    });

    if (mode === 'chat') {
        document.getElementById('chatSection').classList.add('active');
        scrollToBottom();
    } else if (mode === 'personality') {
        document.getElementById('personalitySection').classList.add('active');
    } else if (mode === 'settings') {
        document.getElementById('settingsSection').classList.add('active');
    }
}

// Message Handling - Updated to use backend
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const messageText = input.value.trim();

    if (!messageText) return;

    addMessage(messageText, 'user');
    input.value = '';
    input.focus();

    if (chatState.autoSave) {
        chatState.conversationHistory.push({
            role: 'user',
            content: messageText,
            timestamp: new Date().toISOString()
        });
    }

    showTypingIndicator();

    try {
        // Call Python backend API
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: messageText,
                personality: chatState.currentTone
            })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.success) {
            const botResponse = data.response;
            addMessage(botResponse, 'bot');

            if (chatState.autoSave) {
                chatState.conversationHistory.push({
                    role: 'bot',
                    content: botResponse,
                    timestamp: data.timestamp
                });
                saveSettings();
            }

            if (chatState.soundEnabled) {
                playNotificationSound();
            }
        } else {
            addMessage('Sorry, kuch error hua! 😅', 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        // Fallback to offline response
        const fallbackResponse = generateOfflineResponse(messageText);
        addMessage(fallbackResponse, 'bot');
    }
}

function addMessage(text, sender) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === 'bot' 
        ? '🤖'
        : '<img src="my.JPG" alt="User" class="avatar-img">';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
    `;

    container.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const container = document.getElementById('messagesContainer');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-message';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    container.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typing = document.querySelector('.typing-message');
    if (typing) typing.remove();
}

function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

// Response Generation - REMOVED (using Python backend now)

// Offline Response Generator (fallback)
function generateOfflineResponse(userMessage) {
    const responses = [
        'Ye question interesting hai! 🤔',
        'Acha sawal hai! Python, JavaScript, ya ML ke baare mein poochte ho toh mujhe acha lagta hai! 💻',
        'Mujhe ye samajhne mein thoda time chahiye... Aur detail doge to acha hoga! 📚',
        'Great question! Kya tum kisi specific topic ke baare mein poochna chahte ho? 🚀'
    ];
    return responses[Math.floor(Math.random() * responses.length)];
}

// Personality Settings
function updateTone(e) {
    chatState.currentTone = e.target.value;
    updatePreview();
    saveSettings();
}

function updateLength(e) {
    chatState.responseLength = e.target.value;
    updatePreview();
    saveSettings();
}

function updateLevel(e) {
    chatState.knowledgeLevel = e.target.value;
    updatePreview();
    saveSettings();
}

function updateEmoji(e) {
    chatState.emojiUsage = e.target.value;
    updatePreview();
    saveSettings();
}

function updatePreview() {
    const toneMap = {
        friendly: 'Friendly & Casual',
        professional: 'Professional',
        creative: 'Creative & Playful',
        formal: 'Formal & Respectful',
    };

    const preview = document.getElementById('previewBox');
    preview.innerHTML = `
        <p>Your bot will respond in: <strong>${toneMap[chatState.currentTone]}</strong> tone</p>
        <p>Response length: <strong>${chatState.responseLength}</strong></p>
        <p>Knowledge level: <strong>${chatState.knowledgeLevel}</strong></p>
        <p>Emoji usage: <strong>${chatState.emojiUsage}</strong></p>
    `;
}

// Theme Management
function toggleDarkMode(e) {
    chatState.darkMode = e.target.checked;
    setupTheme();
    saveSettings();
}

function setupTheme() {
    if (chatState.darkMode) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

// Settings Management
function saveSettings() {
    localStorage.setItem('chatbotSettings', JSON.stringify(chatState));
}

function loadSettings() {
    const saved = localStorage.getItem('chatbotSettings');
    if (saved) {
        chatState = JSON.parse(saved);
        applyLoadedSettings();
    }
}

function applyLoadedSettings() {
    // Apply personality settings
    document.getElementById('toneSelect').value = chatState.currentTone;
    document.getElementById('lengthSelect').value = chatState.responseLength;
    document.getElementById('levelSelect').value = chatState.knowledgeLevel;
    document.getElementById('emojiSelect').value = chatState.emojiUsage;

    // Apply general settings
    document.getElementById('darkModeToggle').checked = chatState.darkMode;
    document.getElementById('soundToggle').checked = chatState.soundEnabled;
    document.getElementById('autoSaveToggle').checked = chatState.autoSave;
    document.getElementById('animationToggle').checked = chatState.animationEnabled;

    // Apply theme
    setupTheme();
    updatePreview();
}

// History Management
function clearHistory() {
    if (confirm('Are you sure you want to clear all conversations?')) {
        chatState.conversationHistory = [];
        document.getElementById('messagesContainer').innerHTML = '';
        addWelcomeMessage();
        saveSettings();
        alert('History cleared!');
    }
}

function exportConversations() {
    if (chatState.conversationHistory.length === 0) {
        alert('No conversations to export!');
        return;
    }

    const dataStr = JSON.stringify(chatState.conversationHistory, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chatbot-conversations-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    alert('Conversation exported successfully!');
}

// Utility Functions
function addWelcomeMessage() {
    const container = document.getElementById('messagesContainer');
    const hour = new Date().getHours();
    let greeting = 'Hello';

    if (hour < 12) greeting = 'Good morning';
    else if (hour < 18) greeting = 'Good afternoon';
    else greeting = 'Good evening';

    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message bot-message';
    welcomeDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <p>${greeting}! 👋 Mein aapka AI assistant hoon. Python, JavaScript, Machine Learning, Web Development - kisi bhi tech topic ke baare mein pooch sakte ho! 💻</p>
        </div>
    `;
    container.appendChild(welcomeDiv);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function playNotificationSound() {
    // Create a simple beep using Web Audio API
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.frequency.value = 800;
        oscillator.type = 'sine';

        gain.gain.setValueAtTime(0.3, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        console.log('Sound notification not available');
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('messageInput').focus();
    }

    // Ctrl/Cmd + D to toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        document.getElementById('darkModeToggle').click();
    }
});
