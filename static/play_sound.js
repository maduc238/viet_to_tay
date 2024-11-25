let isPlaying = false; // Biến trạng thái để kiểm soát phát âm thanh

// Lấy nội dung từ thẻ <p> và phát âm thanh khi nhấn nút
document.getElementById('playButton').addEventListener('click', async () => {
    if (isPlaying) {
        alert('Âm thanh đang phát. Vui lòng đợi!');
        return;
    }

    const text = document.getElementById('translated-text').innerText.trim();
    if (!text) {
        alert('Không có nội dung để phát!');
        return;
    }

    try {
        // Gửi yêu cầu tới server
        const response = await fetch('/speak', {
            method: 'POST',
            body: new URLSearchParams({ text: text }),
        });

        if (response.ok) {
            isPlaying = true;

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);

            const audio = new Audio(audioUrl);
            audio.onended = () => {
                isPlaying = false;
            };

            audio.play();
        } else {
            alert('Đã xảy ra lỗi khi chuyển văn bản thành âm thanh.');
        }
    } catch (error) {
        console.error('Lỗi:', error);
        alert('Không thể kết nối tới server.');
    }
});
