# 🎵 AI Music Recommendation System with Weather Integration

An intelligent music recommendation system that combines machine learning with real-time weather data to suggest the perfect soundtrack for any moment. Built as a 5th Semester AIML Mini Project.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🧠 AI-Powered Recommendations
- **Content-Based Filtering**: Uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
- **Cosine Similarity**: Analyzes song features, lyrics, genres, and moods
- **High Accuracy**: Provides personalized recommendations based on song characteristics

### 🌤️ Weather-Based Music Discovery (Standout Feature)
- **Automatic Location Detection**: Uses browser geolocation
- **Real-Time Weather Analysis**: Integrates with OpenWeatherMap API
- **Mood Mapping**: Matches weather conditions to music moods
- **Smart Playlist Generation**: Creates weather-appropriate playlists

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Beautiful glass-effect cards
- **Responsive Layout**: Works on all devices
- **Smooth Animations**: Engaging user interactions
- **Dark Theme**: Eye-friendly interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- OpenWeatherMap API key (free tier available)

### Installation

1. **Clone or download the repository**
```bash
cd "d:\Mini Project 5th sem"
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Get OpenWeatherMap API Key** (Optional but recommended)
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key
   - Open `weather_recommendation.py` and replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual key

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
   - Navigate to `http://127.0.0.1:5000`
   - Grant location permission for weather-based recommendations

## 📁 Project Structure

```
Mini Project 5th sem/
├── app.py                          # Flask application (main entry point)
├── recommendation.py               # Music recommendation engine (TF-IDF + Cosine Similarity)
├── weather_recommendation.py       # Weather-based recommendation system
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── music_data.csv             # Music dataset (songs, artists, genres, moods, lyrics)
├── templates/
│   └── index.html                 # Main HTML template
└── static/
    ├── css/
    │   └── style.css              # Modern styling with animations
    └── js/
        └── script.js              # Frontend JavaScript logic
```

## 🔧 How It Works

### Music Recommendation Engine

1. **Data Processing**
   - Loads music dataset with songs, artists, genres, moods, and lyrics
   - Combines features into a unified text representation
   - Cleans and preprocesses text data

2. **TF-IDF Vectorization**
   - Converts text features into numerical vectors
   - Weighs terms by importance (TF-IDF scores)
   - Creates a feature matrix for all songs

3. **Cosine Similarity**
   - Computes similarity between song vectors
   - Finds songs with similar characteristics
   - Ranks recommendations by similarity score

### Weather-Based Recommendations

1. **Location Detection**
   - Captures user's GPS coordinates via browser
   - Falls back to IP-based location if needed

2. **Weather Retrieval**
   - Fetches current weather from OpenWeatherMap API
   - Extracts temperature, conditions, humidity, etc.

3. **Mood Mapping**
   - Maps weather conditions to music moods:
     - ☀️ Clear → Happy, Energetic
     - 🌧️ Rain → Melancholic, Jazz, Blues
     - ⛈️ Thunderstorm → Energetic, Rock
     - ❄️ Snow → Peaceful, Classical
     - ☁️ Cloudy → Calm, Indie

4. **Playlist Generation**
   - Filters songs by mood and genre
   - Returns curated playlist for the weather

## 🎯 Usage

### Song-Based Recommendations
1. Type a song name in the search box
2. Select from autocomplete suggestions
3. Click "Get Recommendations"
4. View personalized song recommendations

### Weather-Based Recommendations
1. Click "Discover Weather Music"
2. Allow location access when prompted
3. View current weather and mood
4. Explore weather-matched playlist

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations
- **Scikit-learn**: Machine learning (TF-IDF, Cosine Similarity)
- **Requests**: HTTP requests for weather API

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling (Glassmorphism, animations)
- **JavaScript**: Interactivity and API calls
- **Font Awesome**: Icons

### APIs
- **OpenWeatherMap API**: Weather data

## 📊 Dataset

The `music_data.csv` contains 90+ popular songs with:
- **Song Name**: Title of the song
- **Artist**: Performer/band
- **Genre**: Musical genre (pop, rock, jazz, etc.)
- **Mood**: Emotional tone (happy, sad, energetic, etc.)
- **Lyrics**: Key lyrics/themes for TF-IDF analysis

You can expand the dataset by adding more rows with the same format.

## 🎨 Customization

### Adding More Songs
Edit `data/music_data.csv` and add rows in this format:
```csv
song,artist,genre,mood,lyrics
Your Song,Your Artist,pop,happy,"lyrics keywords themes"
```

### Changing Weather Mappings
Edit `weather_recommendation.py`:
```python
self.weather_mood_map = {
    'Clear': 'your_custom_mood',
    # Add more mappings
}
```

### Styling
Modify `static/css/style.css` to change colors, animations, etc.

## 🔐 API Key Configuration

To enable weather features:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Open `weather_recommendation.py`
3. Replace this line:
   ```python
   self.api_key = api_key or "YOUR_OPENWEATHERMAP_API_KEY"
   ```
   With:
   ```python
   self.api_key = api_key or "your_actual_api_key_here"
   ```

## 🐛 Troubleshooting

### Dataset Not Found
- Ensure `data/music_data.csv` exists
- Check file path in `app.py`

### Weather Not Working
- Verify API key is correct
- Check internet connection
- Allow location permissions in browser

### Import Errors
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📈 Future Enhancements

- 🎵 Spotify API integration for real playback
- 🔐 User authentication and profiles
- 💾 Save favorite playlists
- 📊 Listening history and analytics
- 🤖 Deep learning models (Neural Collaborative Filtering)
- 🌍 Multi-language support
- 📱 Mobile app version

## 👥 Contributing

This is a student project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of a 5th Semester AIML Mini Project.

## 🙏 Acknowledgments

- Inspired by [harteij19/music-recommendation-app-python](https://github.com/harteij19/music-recommendation-app-python)
- OpenWeatherMap for weather API
- Scikit-learn for ML algorithms
- Flask community for excellent documentation

## 📧 Contact

For questions or feedback about this project, please create an issue in the repository.

---

**Built with ❤️ for 5th Semester AIML Mini Project**

*Combining Machine Learning with Real-World Data for Intelligent Music Discovery*
