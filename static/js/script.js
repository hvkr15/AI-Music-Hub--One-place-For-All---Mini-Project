// ===================================
// Global Variables
// ===================================
let selectedSong = '';
let searchTimeout = null;

// ===================================
// Utility Functions
// ===================================
function showLoading() {
    document.getElementById('loading-spinner').classList.add('active');
}

function hideLoading() {
    document.getElementById('loading-spinner').classList.remove('active');
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function showError(message, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--error);">
            <i class="fas fa-exclamation-circle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
            <p style="font-size: 1.125rem;">${message}</p>
        </div>
    `;
}

// ===================================
// Song Search Functionality
// ===================================
const searchInput = document.getElementById('song-search');
const searchResults = document.getElementById('search-results');

if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value;
        
        // Clear previous timeout
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        // Hide results if query is empty
        if (query.length === 0) {
            searchResults.classList.remove('active');
            return;
        }
        
        // Debounce search
        searchTimeout = setTimeout(() => {
            searchSongs(query);
        }, 300);
    });

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.remove('active');
        }
    });
}

async function searchSongs(query) {
    try {
        const response = await fetch(`/search-songs?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.songs.length > 0) {
            displaySearchResults(data.songs);
        } else {
            searchResults.innerHTML = '<div class="search-result-item">No songs found</div>';
            searchResults.classList.add('active');
        }
    } catch (error) {
        console.error('Error searching songs:', error);
    }
}

function displaySearchResults(songs) {
    searchResults.innerHTML = songs.map(song => `
        <div class="search-result-item" onclick="selectSong('${song.replace(/'/g, "\\'")}')">
            <i class="fas fa-music"></i> ${song}
        </div>
    `).join('');
    searchResults.classList.add('active');
}

function selectSong(song) {
    selectedSong = song;
    searchInput.value = song;
    searchResults.classList.remove('active');
}

// ===================================
// Get Song Recommendations
// ===================================
async function getRecommendations() {
    const songName = searchInput.value.trim();
    
    if (!songName) {
        alert('Please enter or select a song name');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song_name: songName })
        });
        
        const data = await response.json();
        
        if (data.success && data.recommendations) {
            displaySongRecommendations(data.recommendations, songName);
        } else {
            showError(data.error || 'Unable to get recommendations', 'song-recommendations');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.', 'song-recommendations');
    } finally {
        hideLoading();
    }
}

function displaySongRecommendations(recommendations, baseSong) {
    const container = document.getElementById('song-recommendations');
    
    if (!recommendations || recommendations.length === 0) {
        showError('No recommendations found', 'song-recommendations');
        return;
    }
    
    container.innerHTML = `
        <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-medium); border-radius: 12px;">
            <h3 style="color: var(--primary-color); margin-bottom: 0.5rem;">
                <i class="fas fa-star"></i> Recommendations based on: "${baseSong}"
            </h3>
            <p style="color: var(--text-secondary);">Found ${recommendations.length} similar songs you might love</p>
        </div>
        <div class="recommendations-grid">
            ${recommendations.map((song, index) => createSongCard(song, index)).join('')}
        </div>
    `;
    
    // Animate cards
    animateCards();
}

// ===================================
// Weather-Based Recommendations
// ===================================
async function getWeatherRecommendations() {
    showLoading();
    
    // Check if geolocation is available
    if (!navigator.geolocation) {
        hideLoading();
        showError('Geolocation is not supported by your browser', 'weather-recommendations');
        return;
    }
    
    // Get user's location
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            
            try {
                const response = await fetch('/weather-recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ latitude, longitude })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayWeatherInfo(data.weather, data.mood);
                    displayWeatherRecommendations(data.recommendations, data.weather);
                } else {
                    showError(data.error || 'Unable to get weather recommendations', 'weather-recommendations');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('An error occurred. Please try again.', 'weather-recommendations');
            } finally {
                hideLoading();
            }
        },
        (error) => {
            hideLoading();
            console.error('Geolocation error:', error);
            showError('Unable to access your location. Please enable location services.', 'weather-recommendations');
        }
    );
}

function displayWeatherInfo(weather, mood) {
    const container = document.getElementById('weather-info');
    
    const weatherIcon = getWeatherIcon(weather.condition);
    
    container.innerHTML = `
        <div class="weather-display">
            <div class="weather-icon-large">
                ${weatherIcon}
            </div>
            <div class="weather-details">
                <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <i class="fas fa-map-marker-alt" style="color: var(--primary-color);"></i>
                    <h3 style="margin: 0;">${weather.city}</h3>
                </div>
                <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 1rem;">
                    <i class="fas fa-location-arrow"></i> Your current location
                </p>
                <div class="weather-temp">${Math.round(weather.temperature)}°C</div>
                <p style="color: var(--text-secondary); text-transform: capitalize;">
                    ${weather.description}
                </p>
                <div class="weather-meta">
                    <div class="weather-meta-item">
                        <i class="fas fa-temperature-high"></i>
                        <span>Feels like ${Math.round(weather.feels_like)}°C</span>
                    </div>
                    <div class="weather-meta-item">
                        <i class="fas fa-tint"></i>
                        <span>${weather.humidity}% Humidity</span>
                    </div>
                </div>
                <div class="mood-indicator">
                    <i class="fas fa-smile"></i> Perfect mood for: ${mood}
                </div>
            </div>
        </div>
    `;
}

function displayWeatherRecommendations(recommendations, weather) {
    const container = document.getElementById('weather-recommendations');
    
    if (!recommendations || recommendations.length === 0) {
        showError('No recommendations found', 'weather-recommendations');
        return;
    }
    
    container.innerHTML = `
        <div style="text-align: center; margin: 2rem 0 2rem; padding: 1.5rem; background: var(--bg-medium); border-radius: 12px;">
            <h3 style="color: var(--primary-color); margin-bottom: 0.5rem;">
                <i class="fas fa-cloud-sun"></i> Weather-Matched Playlist
            </h3>
            <p style="color: var(--text-secondary);">
                ${recommendations.length} songs curated for ${weather.condition.toLowerCase()} weather in <strong>${weather.city}</strong>
            </p>
        </div>
        <div class="recommendations-grid">
            ${recommendations.map((song, index) => createSongCard(song, index)).join('')}
        </div>
    `;
    
    // Animate cards
    animateCards();
}

// ===================================
// Create Song Card
// ===================================
function createSongCard(song, index) {
    const artist = song.artist || 'Unknown Artist';
    const genre = song.genre || 'Various';
    const mood = song.mood || 'Neutral';
    const similarity = song.similarity_score ? `${(song.similarity_score * 100).toFixed(0)}% match` : '';
    
    return `
        <div class="song-card" style="animation-delay: ${index * 0.1}s;">
            <div class="song-card-header">
                <div class="song-icon">
                    <i class="fas fa-music"></i>
                </div>
                <div class="song-info">
                    <h3>${song.song}</h3>
                    <div class="song-artist">${artist}</div>
                </div>
            </div>
            <div class="song-details">
                ${genre ? `<span class="song-tag"><i class="fas fa-guitar"></i> ${genre}</span>` : ''}
                ${mood ? `<span class="song-tag"><i class="fas fa-heart"></i> ${mood}</span>` : ''}
                ${similarity ? `<span class="song-tag" style="background: linear-gradient(135deg, var(--primary-color), var(--accent-color)); color: white; border: none;"><i class="fas fa-star"></i> ${similarity}</span>` : ''}
            </div>
            <div class="play-buttons">
                <button class="play-btn spotify-btn" onclick="openSpotify('${encodeURIComponent(song.song)}', '${encodeURIComponent(artist)}')">
                    <i class="fab fa-spotify"></i> Spotify
                </button>
                <button class="play-btn youtube-btn" onclick="openYouTubeMusic('${encodeURIComponent(song.song)}', '${encodeURIComponent(artist)}')">
                    <i class="fab fa-youtube"></i> YouTube Music
                </button>
            </div>
        </div>
    `;
}

// ===================================
// Helper Functions
// ===================================
function getWeatherIcon(condition) {
    const icons = {
        'Clear': '<i class="fas fa-sun" style="color: #fbbf24;"></i>',
        'Clouds': '<i class="fas fa-cloud" style="color: #94a3b8;"></i>',
        'Rain': '<i class="fas fa-cloud-rain" style="color: #3b82f6;"></i>',
        'Drizzle': '<i class="fas fa-cloud-rain" style="color: #60a5fa;"></i>',
        'Thunderstorm': '<i class="fas fa-bolt" style="color: #f59e0b;"></i>',
        'Snow': '<i class="fas fa-snowflake" style="color: #e0f2fe;"></i>',
        'Mist': '<i class="fas fa-smog" style="color: #cbd5e1;"></i>',
        'Fog': '<i class="fas fa-smog" style="color: #cbd5e1;"></i>'
    };
    
    return icons[condition] || '<i class="fas fa-cloud" style="color: #94a3b8;"></i>';
}

function animateCards() {
    const cards = document.querySelectorAll('.song-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// ===================================
// Navigation Active State
// ===================================
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === current) {
            link.classList.add('active');
        }
    });
});

// ===================================
// Enter Key Support for Search
// ===================================
if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            getRecommendations();
        }
    });
}

// ===================================
// Page Load Animation
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎵 Music Recommendation System Loaded');
    
    // Add fade-in animation to sections
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'all 0.8s ease';
        observer.observe(section);
    });
});

// ===================================
// Open Music Streaming Platforms
// ===================================
function openSpotify(songName, artistName) {
    // Decode the encoded parameters
    const song = decodeURIComponent(songName);
    const artist = decodeURIComponent(artistName);
    
    // Create search query for Spotify
    const query = encodeURIComponent(`${song} ${artist}`);
    const spotifySearchUrl = `https://open.spotify.com/search/${query}`;
    
    // Open in new tab
    window.open(spotifySearchUrl, '_blank');
}

function openYouTubeMusic(songName, artistName) {
    // Decode the encoded parameters
    const song = decodeURIComponent(songName);
    const artist = decodeURIComponent(artistName);
    
    // Create search query for YouTube Music
    const query = encodeURIComponent(`${song} ${artist}`);
    const youtubeSearchUrl = `https://music.youtube.com/search?q=${query}`;
    
    // Open in new tab
    window.open(youtubeSearchUrl, '_blank');
}
