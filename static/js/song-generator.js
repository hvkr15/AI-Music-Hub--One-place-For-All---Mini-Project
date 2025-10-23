// Song Generator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const songForm = document.getElementById('songForm');
    
    if (songForm) {
        songForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            await generateSong();
        });
    }
});

async function generateSong() {
    const prompt = document.getElementById('songPrompt').value.trim();
    const duration = document.getElementById('songDuration').value;
    const tempo = document.getElementById('songTempo').value;
    const vocals = document.getElementById('songVocals').value;
    
    if (!prompt) {
        alert('Please describe your song');
        return;
    }
    
    // Show loading, hide output
    const loadingDiv = document.getElementById('loadingSong');
    const outputDiv = document.getElementById('songOutput');
    
    loadingDiv.style.display = 'block';
    outputDiv.style.display = 'none';
    
    try {
        const response = await fetch('/generate-song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                duration: duration,
                tempo: tempo,
                vocals: vocals
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('generatedSong').textContent = data.song_description;
            loadingDiv.style.display = 'none';
            outputDiv.style.display = 'block';
            
            // Scroll to output
            outputDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            throw new Error(data.error || 'Failed to generate song description');
        }
    } catch (error) {
        console.error('Error generating song:', error);
        loadingDiv.style.display = 'none';
        alert('Error generating song description. Please try again.');
    }
}

function copySong() {
    const songText = document.getElementById('generatedSong').textContent;
    
    navigator.clipboard.writeText(songText).then(() => {
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
        console.error('Failed to copy song:', err);
        alert('Failed to copy. Please try again.');
    });
}

function downloadSong() {
    const songText = document.getElementById('generatedSong').textContent;
    const prompt = document.getElementById('songPrompt').value;
    
    // Create filename
    const filename = `song-description-${Date.now()}.txt`;
    
    // Create blob and download
    const blob = new Blob([songText], { type: 'text/plain' });
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

function generateNewSong() {
    // Hide output and scroll to form
    document.getElementById('songOutput').style.display = 'none';
    document.getElementById('songForm').scrollIntoView({ behavior: 'smooth' });
}
