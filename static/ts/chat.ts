document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('chat-toggle') as HTMLButtonElement;
    const closeBtn = document.getElementById('chat-close') as HTMLButtonElement;
    const chatWindow = document.getElementById('chat-window') as HTMLDivElement;
    const chatBody = document.getElementById('chat-body') as HTMLDivElement;
    const chatInput = document.getElementById('chat-input') as HTMLInputElement;
    const sendBtn = document.getElementById('chat-send') as HTMLButtonElement;

    if (!toggleBtn || !chatWindow) return;

    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.add('open');
        toggleBtn.style.display = 'none';
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('open');
        toggleBtn.style.display = 'flex';
    });

    const sendMessage = () => {
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        chatInput.value = '';

        setTimeout(() => {
            addMessage('Спасибо за обращение! Наш специалист скоро свяжется с вами.', 'bot');
        }, 1000);
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(text: string, sender: 'bot' | 'user') {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${sender}`;
        msgDiv.textContent = text;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
});