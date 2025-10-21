# 🎓 Project Documentation
## AI Music Recommendation System with Weather Integration

### 5th Semester AIML Mini Project

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Architecture](#technical-architecture)
3. [Machine Learning Implementation](#machine-learning-implementation)
4. [Weather Integration](#weather-integration)
5. [System Features](#system-features)
6. [File Structure](#file-structure)
7. [API Documentation](#api-documentation)
8. [Testing Guide](#testing-guide)

---

## 📖 Project Overview

### Objective
Develop an intelligent music recommendation system that combines content-based filtering using machine learning with real-time weather data to provide personalized music suggestions.

### Problem Statement
Traditional music recommendation systems lack context awareness. This project solves this by:
- Analyzing song content (lyrics, genre, mood)
- Incorporating environmental factors (weather, location)
- Providing context-aware recommendations

### Key Innovation
**Weather-Based Music Recommendation**: A unique feature that detects user location, analyzes current weather conditions, and suggests music that matches the mood of the moment.

---

## 🏗️ Technical Architecture

### System Architecture
```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │ Flask Server │ ◄─────► │  ML Engine  │
│  (Frontend) │         │   (Backend)  │         │   (TF-IDF)  │
└─────────────┘         └──────────────┘         └─────────────┘
       │                       │                         │
       │                       │                         │
       ▼                       ▼                         ▼
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│ Geolocation │         │ Weather API  │         │   Dataset   │
│     API     │         │(OpenWeather) │         │  (CSV File) │
└─────────────┘         └──────────────┘         └─────────────┘
```

### Technology Stack

#### Backend
- **Python 3.12**: Core programming language
- **Flask 3.0.0**: Web framework for API and routing
- **Pandas 2.1.3**: Data manipulation and analysis
- **NumPy 1.26.2**: Numerical computations
- **Scikit-learn 1.3.2**: Machine learning algorithms
- **Requests 2.31.0**: HTTP requests for weather API

#### Frontend
- **HTML5**: Structure and semantics
- **CSS3**: Styling with modern effects (glassmorphism, gradients)
- **JavaScript (ES6+)**: Dynamic interactions and API calls
- **Font Awesome**: Icon library

#### APIs
- **OpenWeatherMap API**: Real-time weather data
- **Geolocation API**: Browser-based location detection

---

## 🤖 Machine Learning Implementation

### Algorithm: Content-Based Filtering

#### Step 1: Feature Engineering
```python
# Combine multiple features
features = ['lyrics', 'genre', 'mood', 'artist']
combined_features = df[features].apply(lambda x: ' '.join(x.astype(str)), axis=1)
```

#### Step 2: TF-IDF Vectorization
- **Term Frequency (TF)**: How often a term appears in a document
- **Inverse Document Frequency (IDF)**: How rare a term is across documents
- **TF-IDF Score**: TF × IDF (importance of term in document)

```python
tfidf = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
tfidf_matrix = tfidf.fit_transform(combined_features)
```

**Parameters:**
- `max_features=5000`: Top 5000 most important features
- `stop_words='english'`: Remove common words (the, is, at)
- `ngram_range=(1, 2)`: Consider single words and word pairs

#### Step 3: Cosine Similarity
Measures similarity between two vectors using the cosine of the angle between them.

**Formula:**
```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- A, B are TF-IDF vectors
- · is dot product
- || || is magnitude

**Value Range:** 0 (completely different) to 1 (identical)

```python
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
```

#### Step 4: Generate Recommendations
```python
# Get similarity scores for input song
similarity_scores = list(enumerate(similarity_matrix[song_idx]))

# Sort by similarity (descending)
similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

# Return top N recommendations (excluding input song)
recommendations = similarity_scores[1:n+1]
```

### Why Content-Based Filtering?

**Advantages:**
- ✅ No cold start problem (works with new users)
- ✅ Transparent recommendations (explainable)
- ✅ Captures niche preferences
- ✅ No user data required (privacy-friendly)

**Limitations:**
- ⚠️ Limited serendipity (similar suggestions only)
- ⚠️ Requires good content features
- ⚠️ Can't recommend across different genres easily

---

## 🌤️ Weather Integration

### Weather-to-Mood Mapping

#### Weather Conditions → Music Moods
| Weather | Temperature | Suggested Mood | Genres |
|---------|------------|----------------|---------|
| ☀️ Clear | Warm | Happy, Energetic | Pop, Dance, Reggae |
| 🌧️ Rain | Any | Melancholic, Reflective | Jazz, Blues, Soul |
| ⛈️ Thunderstorm | Any | Energetic, Intense | Rock, Metal, Electronic |
| ❄️ Snow | Cold | Peaceful, Cozy | Classical, Ambient |
| ☁️ Cloudy | Mild | Calm, Relaxed | Indie, Folk, Acoustic |
| 🌫️ Fog/Mist | Cool | Atmospheric, Chill | Ambient, Lo-fi |

### Implementation Flow

1. **Get User Location**
   ```javascript
   navigator.geolocation.getCurrentPosition(position => {
       const lat = position.coords.latitude;
       const lon = position.coords.longitude;
   });
   ```

2. **Fetch Weather Data**
   ```python
   url = f"https://api.openweathermap.org/data/2.5/weather"
   params = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
   response = requests.get(url, params=params)
   ```

3. **Determine Mood**
   ```python
   condition = weather_data['condition']  # e.g., "Rain"
   temperature = weather_data['temperature']  # e.g., 15°C
   
   base_mood = weather_mood_map[condition]  # "melancholic"
   temp_mood = get_temp_mood(temperature)   # "calm"
   
   final_mood = f"{base_mood} {temp_mood}"
   ```

4. **Filter Songs**
   ```python
   # Filter by mood
   mood_songs = df[df['mood'].str.contains(final_mood)]
   
   # Filter by preferred genres
   genre_songs = mood_songs[mood_songs['genre'].isin(preferred_genres)]
   
   return genre_songs.sample(n=15)
   ```

---

## ⚙️ System Features

### 1. Song-Based Recommendations
- **Input**: Song name
- **Process**: TF-IDF + Cosine Similarity
- **Output**: 10 similar songs with match percentage

### 2. Weather-Based Recommendations
- **Input**: User location (automatic)
- **Process**: Weather API + Mood mapping + Filtering
- **Output**: 15 weather-appropriate songs

### 3. Autocomplete Search
- **Real-time search**: Debounced with 300ms delay
- **Fuzzy matching**: Partial string matching
- **Responsive**: Shows top 50 results

### 4. Responsive Design
- **Desktop**: Full-width layout with cards
- **Tablet**: Adaptive grid layout
- **Mobile**: Single-column stacked view

### 5. Visual Effects
- **Glassmorphism**: Frosted glass effect on cards
- **Gradient backgrounds**: Modern color schemes
- **Smooth animations**: Fade-in, slide-up effects
- **Interactive hover**: Scale transforms on cards

---

## 📁 File Structure

```
Mini Project 5th sem/
│
├── app.py                      # Main Flask application
│   ├── Routes: /, /recommend, /weather-recommend
│   ├── Data loading and initialization
│   └── Error handling
│
├── recommendation.py           # ML recommendation engine
│   ├── Class: MusicRecommender
│   ├── TF-IDF vectorization
│   ├── Cosine similarity computation
│   └── Recommendation generation
│
├── weather_recommendation.py   # Weather-based system
│   ├── Class: WeatherMusicRecommender
│   ├── Weather API integration
│   ├── Mood mapping logic
│   └── Filtering algorithms
│
├── data/
│   └── music_data.csv         # Dataset (84 songs)
│       ├── Columns: song, artist, genre, mood, lyrics
│       └── Sample: pop, rock, jazz, classical songs
│
├── templates/
│   └── index.html             # Main HTML template
│       ├── Hero section
│       ├── Features showcase
│       ├── Search interface
│       └── Results display
│
├── static/
│   ├── css/
│   │   └── style.css          # Styling (1200+ lines)
│   │       ├── CSS variables
│   │       ├── Glassmorphism effects
│   │       ├── Animations
│   │       └── Responsive design
│   │
│   └── js/
│       └── script.js          # Frontend logic (400+ lines)
│           ├── Search functionality
│           ├── API calls
│           ├── DOM manipulation
│           └── Event handlers
│
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
├── QUICKSTART.md             # Quick setup guide
├── PROJECT_DOCUMENTATION.md  # This file
├── .gitignore               # Git ignore rules
├── config.example.py        # Configuration template
└── start.bat                # Windows launcher
```

---

## 🔌 API Documentation

### 1. GET /
**Description**: Serve main HTML page

**Response**: HTML page

---

### 2. POST /recommend
**Description**: Get song-based recommendations

**Request Body**:
```json
{
    "song_name": "Shape of You"
}
```

**Response**:
```json
{
    "success": true,
    "recommendations": [
        {
            "song": "Blinding Lights",
            "artist": "The Weeknd",
            "genre": "pop",
            "mood": "energetic",
            "similarity_score": 0.87
        },
        ...
    ]
}
```

**Error Response**:
```json
{
    "error": "Song not found or no recommendations available"
}
```

---

### 3. POST /weather-recommend
**Description**: Get weather-based recommendations

**Request Body**:
```json
{
    "latitude": 40.7128,
    "longitude": -74.0060
}
```

**Response**:
```json
{
    "success": true,
    "weather": {
        "condition": "Clear",
        "description": "clear sky",
        "temperature": 25,
        "feels_like": 24,
        "humidity": 60,
        "city": "New York",
        "icon": "01d"
    },
    "mood": "happy energetic",
    "recommendations": [...]
}
```

---

### 4. GET /search-songs?q={query}
**Description**: Search songs by name

**Parameters**:
- `q`: Search query (string)

**Response**:
```json
{
    "success": true,
    "songs": ["Shape of You", "Shallow", "Stay With Me", ...]
}
```

---

## 🧪 Testing Guide

### Manual Testing

#### Test 1: Song Recommendations
1. Open http://127.0.0.1:5000
2. Type "Shape of You" in search box
3. Click "Get Recommendations"
4. **Expected**: 10 similar pop/dance songs with match percentages

#### Test 2: Weather Recommendations
1. Click "Discover Weather Music"
2. Allow location access
3. **Expected**: Weather info + 15 mood-matched songs

#### Test 3: Search Functionality
1. Type "love" in search box
2. **Expected**: Autocomplete dropdown with matching songs
3. Select a song and get recommendations

### API Testing (Using curl or Postman)

```bash
# Test song recommendations
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"song_name": "Happy"}'

# Test weather recommendations
curl -X POST http://127.0.0.1:5000/weather-recommend \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.7041, "longitude": 77.1025}'

# Test search
curl http://127.0.0.1:5000/search-songs?q=love
```

### Performance Testing

**Recommendation Speed**: < 500ms for 10 recommendations
**Dataset Size**: 84 songs (scalable to thousands)
**TF-IDF Matrix**: 84 × 1517 features
**Memory Usage**: ~50MB with current dataset

---

## 📊 Dataset Information

### Current Dataset: 84 Songs

**Genre Distribution**:
- Pop: 35 songs (42%)
- Rock: 18 songs (21%)
- Ballad: 12 songs (14%)
- Alternative: 8 songs (10%)
- Jazz: 6 songs (7%)
- Others: 5 songs (6%)

**Mood Distribution**:
- Happy: 20 songs (24%)
- Melancholic: 18 songs (21%)
- Energetic: 15 songs (18%)
- Romantic: 14 songs (17%)
- Calm: 10 songs (12%)
- Others: 7 songs (8%)

### Expanding the Dataset

To add more songs, edit `data/music_data.csv`:

```csv
song,artist,genre,mood,lyrics
New Song,Artist Name,genre,mood,"key lyrics words themes"
```

**Tips for better recommendations**:
- Add diverse genres and moods
- Include meaningful lyrics keywords
- Maintain consistent formatting
- Add at least 50+ songs per genre for better clustering

---

## 🚀 Deployment Considerations

### Local Development
- Already configured with Flask development server
- Debug mode enabled for hot reloading
- Running on http://127.0.0.1:5000

### Production Deployment

**Option 1: Heroku**
```bash
# Add Procfile
web: gunicorn app:app

# Requirements
pip install gunicorn
```

**Option 2: AWS/Azure**
- Use WSGI server (Gunicorn/uWSGI)
- Set up reverse proxy (Nginx)
- Enable HTTPS
- Use environment variables for API keys

**Option 3: Docker**
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 🔒 Security Considerations

1. **API Keys**: Store in environment variables
2. **CORS**: Configure allowed origins
3. **Rate Limiting**: Implement to prevent abuse
4. **Input Validation**: Sanitize user inputs
5. **HTTPS**: Use SSL in production

---

## 📈 Future Enhancements

### Planned Features
1. **User Authentication**: Login/signup system
2. **Playlist Saving**: Save favorite recommendations
3. **Spotify Integration**: Play songs directly
4. **Deep Learning**: Neural collaborative filtering
5. **Social Features**: Share playlists
6. **Analytics Dashboard**: Listening statistics
7. **Mobile App**: React Native/Flutter
8. **Voice Search**: Speech recognition

### Scaling Considerations
- **Database**: Migrate from CSV to PostgreSQL/MongoDB
- **Caching**: Redis for faster recommendations
- **CDN**: Static assets delivery
- **Microservices**: Separate recommendation engine
- **Load Balancing**: Handle multiple requests

---

## 👨‍💻 Development Notes

### Adding New Features

1. **Backend**: Add route in `app.py`
2. **ML Logic**: Extend `recommendation.py`
3. **Frontend**: Update `templates/index.html`
4. **Styling**: Modify `static/css/style.css`
5. **Interactivity**: Add JS in `static/js/script.js`

### Code Style
- **Python**: PEP 8 guidelines
- **JavaScript**: ES6+ features
- **HTML**: Semantic tags
- **CSS**: BEM-like naming

---

## 📝 Project Report Outline

### For Academic Submission

1. **Introduction**
   - Problem statement
   - Objectives
   - Scope and limitations

2. **Literature Review**
   - Existing recommendation systems
   - TF-IDF algorithm
   - Content-based filtering

3. **System Design**
   - Architecture diagram
   - Data flow diagram
   - ER diagram (if using database)

4. **Implementation**
   - Technology stack
   - Algorithm implementation
   - Code snippets

5. **Results and Testing**
   - Test cases
   - Performance metrics
   - Screenshots

6. **Conclusion**
   - Achievements
   - Limitations
   - Future scope

7. **References**
   - Research papers
   - Documentation
   - Online resources

---

## 🙏 Acknowledgments

- Scikit-learn documentation
- Flask documentation
- OpenWeatherMap API
- Stack Overflow community
- GitHub open-source projects

---

**Document Version**: 1.0
**Last Updated**: October 21, 2025
**Project Status**: Complete and Running

---

For questions or issues, refer to README.md or create an issue in the repository.
