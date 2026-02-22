const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

const API_URL = 'http://localhost:8000';

// Add message to UI
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(role === 'user' ? 'user-message' : 'ai-message');
    messageDiv.textContent = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Fetch history on load
async function loadHistory() {
    try {
        const res = await fetch(`${API_URL}/history`);
        const history = await res.json();
        history.forEach(msg => {
            addMessage(msg.role, msg.content);
        });
    } catch (err) {
        console.error('Failed to load history', err);
    }
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // Add user msg to UI
    addMessage('user', text);
    userInput.value = '';

    try {
        const res = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: text })
        });
        const data = await res.json();
        addMessage('ai', data.content);
    } catch (err) {
        console.error('Failed to send message', err);
        addMessage('ai', 'خطأ في الاتصال بالخادم. تأكد من تشغيل الباك-اند.');
    }
});

loadHistory();
