// Lyrics Generator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const lyricsForm = document.getElementById('lyricsForm');
    
    if (lyricsForm) {
        lyricsForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            await generateLyrics();
        });
    }
});

async function generateLyrics() {
    const theme = document.getElementById('lyricsTheme').value.trim();
    const genre = document.getElementById('lyricsGenre').value;
    const mood = document.getElementById('lyricsMood').value;
    
    if (!theme) {
        alert('Please enter a theme for your song');
        return;
    }
    
    // Show loading, hide output
    const loadingDiv = document.getElementById('loadingLyrics');
    const outputDiv = document.getElementById('lyricsOutput');
    
    loadingDiv.style.display = 'block';
    outputDiv.style.display = 'none';
    
    try {
        const response = await fetch('/generate-lyrics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                theme: theme,
                genre: genre,
                mood: mood
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('generatedLyrics').textContent = data.lyrics;
            loadingDiv.style.display = 'none';
            outputDiv.style.display = 'block';
            
            // Scroll to output
            outputDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            throw new Error(data.error || 'Failed to generate lyrics');
        }
    } catch (error) {
        console.error('Error generating lyrics:', error);
        loadingDiv.style.display = 'none';
        alert('Error generating lyrics. Please try again.');
    }
}

function copyLyrics() {
    const lyricsText = document.getElementById('generatedLyrics').textContent;
    
    navigator.clipboard.writeText(lyricsText).then(() => {
        // Show success feedback
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
        
        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-primary');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy lyrics:', err);
        alert('Failed to copy lyrics. Please try again.');
    });
}

function downloadLyrics() {
    const lyricsText = document.getElementById('generatedLyrics').textContent;
    const theme = document.getElementById('lyricsTheme').value;
    const genre = document.getElementById('lyricsGenre').value;
    
    // Create filename
    const filename = `lyrics-${theme.toLowerCase().replace(/\s+/g, '-')}-${genre}.txt`;
    
    // Create blob and download
    const blob = new Blob([lyricsText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    // Show success feedback
    const btn = event.target.closest('button');
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Downloaded!';
    btn.classList.remove('btn-outline-success');
    btn.classList.add('btn-success');
    
    setTimeout(() => {
        btn.innerHTML = originalHTML;
        btn.classList.remove('btn-success');
        btn.classList.add('btn-outline-success');
    }, 2000);
}

function generateNewLyrics() {
    // Hide output and scroll to form
    document.getElementById('lyricsOutput').style.display = 'none';
    document.getElementById('lyricsForm').scrollIntoView({ behavior: 'smooth' });
    
    // Optionally clear the form
    // document.getElementById('lyricsTheme').value = '';
}
