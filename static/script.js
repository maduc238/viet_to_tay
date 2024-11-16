document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');

    let lastMessageCount = 0;

    function fetchMessages() {
        fetch('/messages')
            .then(response => response.json())
            .then(data => {
                if (data.length > lastMessageCount) {
                    const newMessages = data.slice(lastMessageCount);
                    newMessages.forEach(msg => {
                        const messageDiv = document.createElement('div');
                        messageDiv.classList.add(msg.user === 'User' ? 'user-message' : 'bot-message');
                        messageDiv.textContent = `${msg.user}: ${msg.text}`;
                        chatBox.appendChild(messageDiv);
                    });

                    // Cuộn xuống cuối
                    chatBox.scrollTop = chatBox.scrollHeight;

                    // Cập nhật số lượng tin nhắn
                    lastMessageCount = data.length;
                }
            });
    }

    sendBtn.addEventListener('click', () => {
        const message = messageInput.value;
        if (message.trim()) {
            fetch('/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            }).then(() => {
                messageInput.value = '';
                fetchMessages();
            });
        }
    });

    setInterval(fetchMessages, 1000);
});
