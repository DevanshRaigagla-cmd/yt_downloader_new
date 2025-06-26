document.getElementById('downloadForm').onsubmit = async function(e) {
    e.preventDefault();

    const url = document.getElementById('youtube_url').value;
    const format = document.getElementById('format').value;
    const quality = document.getElementById('quality').value;

    const form = new FormData();
    form.append('youtube_url', url);
    form.append('format', format);
    form.append('quality', quality);

    const response = await fetch('/download', { method: 'POST', body: form });

    if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = (format === 'mp3' ? 'audio.mp3' : 'video.mp4');
        link.click();
    } else {
        const result = await response.json();
        document.getElementById('error').innerText = result.error || 'Failed to download.';
    }
};
