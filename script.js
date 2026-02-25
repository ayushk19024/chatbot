// Configuration - Now using Python backend
const API_URL = 'http://localhost:5000/api';
const chatbotConfig = {
    name: 'MyBot',
    version: '2.0.0',
    developer: 'Ayush Kumar'
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
    isRecording: false
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    initializeEventListeners();
    setupTheme();
    addWelcomeMessage();
    checkBackendHealth();
    initializeNewFeatures();
});

// Initialize New Features
function initializeNewFeatures() {
    // Developer Info Panel
    const devFloatBtn = document.getElementById('devFloatBtn');
    const developerInfo = document.getElementById('developerInfo');
    const devClose = document.getElementById('devClose');

    if (devFloatBtn && developerInfo) {
        devFloatBtn.addEventListener('click', () => {
            developerInfo.classList.add('active');
            devFloatBtn.classList.add('hidden');
        });
    }

    if (devClose && developerInfo) {
        devClose.addEventListener('click', () => {
            developerInfo.classList.remove('active');
            if (devFloatBtn) devFloatBtn.classList.remove('hidden');
        });
    }

    // Keyboard Shortcuts Modal
    const shortcutsModal = document.getElementById('shortcutsModal');
    const shortcutsClose = document.getElementById('shortcutsClose');

    if (shortcutsClose && shortcutsModal) {
        shortcutsClose.addEventListener('click', () => {
            shortcutsModal.classList.remove('active');
        });

        shortcutsModal.addEventListener('click', (e) => {
            if (e.target === shortcutsModal) {
                shortcutsModal.classList.remove('active');
            }
        });
    }

    // Emoji Picker
    const emojiPicker = document.getElementById('emojiPicker');
    const emojiClose = document.getElementById('emojiClose');

    if (emojiClose && emojiPicker) {
        emojiClose.addEventListener('click', () => {
            emojiPicker.classList.remove('active');
        });
    }

    // Add emoji buttons functionality
    document.querySelectorAll('.emoji-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const emoji = btn.textContent;
            const input = document.getElementById('messageInput');
            input.value += emoji;
            input.focus();
            if (emojiPicker) emojiPicker.classList.remove('active');
        });
    });

    // Add Quick Replies
    addQuickReplies();

    // Header Contact Buttons - Open Developer Info
    const headerContactBtn = document.getElementById('headerContactBtn');
    const settingsContactBtn = document.getElementById('settingsContactBtn');

    if (headerContactBtn) {
        headerContactBtn.addEventListener('click', () => {
            if (developerInfo) developerInfo.classList.add('active');
            if (devFloatBtn) devFloatBtn.classList.add('hidden');
        });
    }

    if (settingsContactBtn) {
        settingsContactBtn.addEventListener('click', () => {
            if (developerInfo) developerInfo.classList.add('active');
            if (devFloatBtn) devFloatBtn.classList.add('hidden');
        });
    }
}

// Add Quick Replies to chat
function addQuickReplies() {
    const chatSection = document.getElementById('chatSection');
    if (!chatSection) return;

    let quickRepliesDiv = document.querySelector('.quick-replies');
    if (quickRepliesDiv) return;

    quickRepliesDiv = document.createElement('div');
    quickRepliesDiv.className = 'quick-replies';
    quickRepliesDiv.innerHTML = `
        <button class="quick-reply-btn" data-message="Hello! How are you?">👋 Hello</button>
        <button class="quick-reply-btn" data-message="Tell me about Python">🐍 Python</button>
        <button class="quick-reply-btn" data-message="What can you do?">✨ Features</button>
        <button class="quick-reply-btn" data-message="Help me with JavaScript">💻 JS Help</button>
        <button class="quick-reply-btn" data-message="Explain Machine Learning">🤖 ML</button>
    `;

    chatSection.appendChild(quickRepliesDiv);

    // Add click handlers
    quickRepliesDiv.querySelectorAll('.quick-reply-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.dataset.message;
            document.getElementById('messageInput').value = message;
            sendMessage();
        });
    });
}

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
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }

    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportConversations);
    }
}

// Navigation Handler
function handleNavigation(e) {
    const mode = e.currentTarget.dataset.mode;

    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    // Update sections
    document.querySelectorAll('.chat-section, .personality-section, .settings-section').forEach(section => {
        section.classList.remove('active');
    });

    const targetSection = document.getElementById(`${mode}Section`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// Send Message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    input.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                tone: chatState.currentTone,
                length: chatState.responseLength,
                knowledge: chatState.knowledgeLevel,
                emoji: chatState.emojiUsage
            })
        });

        const data = await response.json();
        removeTypingIndicator();
        addMessage(data.response, 'bot');

        if (chatState.soundEnabled) {
            playNotificationSound();
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage("Sorry, I'm having trouble connecting. Please try again!", 'bot');
    }
}

// Add Message to Chat
function addMessage(text, sender) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <div class="message-avatar">${sender === 'bot' ? '🤖' : '👤'}</div>
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
            <span class="message-timestamp">${timestamp}</span>
            ${sender === 'user' ? '<span class="message-status sent"></span>' : ''}
        </div>
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;

    // Save to history
    chatState.conversationHistory.push({ sender, text, timestamp });
    if (chatState.autoSave) {
        saveSettings();
    }
}

// Show Typing Indicator
function showTypingIndicator() {
    const container = document.getElementById('messagesContainer');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
}

// Remove Typing Indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Settings Functions
function updateTone(e) {
    chatState.currentTone = e.target.value;
    saveSettings();
}

function updateLength(e) {
    chatState.responseLength = e.target.value;
    saveSettings();
}

function updateLevel(e) {
    chatState.knowledgeLevel = e.target.value;
    saveSettings();
}

function updateEmoji(e) {
    chatState.emojiUsage = e.target.value;
    saveSettings();
}

function toggleDarkMode(e) {
    chatState.darkMode = e.target.checked;
    document.body.classList.toggle('dark-mode', chatState.darkMode);
    saveSettings();
}

function setupTheme() {
    if (chatState.darkMode) {
        document.body.classList.add('dark-mode');
        document.getElementById('darkModeToggle').checked = true;
    }
}

// Save & Load Settings
function saveSettings() {
    localStorage.setItem('chatbotSettings', JSON.stringify(chatState));
}

function loadSettings() {
    const saved = localStorage.getItem('chatbotSettings');
    if (saved) {
        const parsed = JSON.parse(saved);
        Object.assign(chatState, parsed);

        // Update UI
        document.getElementById('toneSelect').value = chatState.currentTone;
        document.getElementById('lengthSelect').value = chatState.responseLength;
        document.getElementById('levelSelect').value = chatState.knowledgeLevel;
        document.getElementById('emojiSelect').value = chatState.emojiUsage;
        document.getElementById('soundToggle').checked = chatState.soundEnabled;
        document.getElementById('autoSaveToggle').checked = chatState.autoSave;
        document.getElementById('animationToggle').checked = chatState.animationEnabled;
    }
}

// Clear History
function clearHistory() {
    if (confirm('Are you sure you want to clear all conversations?')) {
        const container = document.getElementById('messagesContainer');
        container.innerHTML = '';
        chatState.conversationHistory = [];
        localStorage.removeItem('chatbotSettings');
        addWelcomeMessage();
    }
}

// Export Conversations
function exportConversations() {
    const data = {
        conversations: chatState.conversationHistory,
        exportedAt: new Date().toISOString(),
        settings: chatState
    };
    const dataBlob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
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

    // Ctrl/Cmd + / to show shortcuts
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        const shortcutsModal = document.getElementById('shortcutsModal');
        if (shortcutsModal) shortcutsModal.classList.add('active');
    }

    // Ctrl/Cmd + L to clear chat
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        clearHistory();
    }

    // Escape to close modals
    if (e.key === 'Escape') {
        const shortcutsModal = document.getElementById('shortcutsModal');
        const developerInfo = document.getElementById('developerInfo');
        const emojiPicker = document.getElementById('emojiPicker');
        
        if (shortcutsModal) shortcutsModal.classList.remove('active');
        if (developerInfo) developerInfo.classList.remove('active');
        if (emojiPicker) emojiPicker.classList.remove('active');
    }
});
