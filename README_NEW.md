# 🎵 AI Music Hub - Complete Music Intelligence Platform

**Your All-in-One AI-Powered Music Ecosystem**

A comprehensive music intelligence platform combining machine learning recommendations, AI-powered lyrics generation, intelligent song description creation, and real-time weather-based playlists - powered by **57,000+ songs** from the Spotify Million Song Dataset. Built as a 5th Semester AIML Mini Project.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)
![Dataset](https://img.shields.io/badge/Dataset-57K+_Songs-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-TF--IDF-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🌟 What Makes This Special?

**AI Music Hub** is a next-generation music platform that goes beyond simple recommendations:
- 🎯 **57,000+ Songs**: Powered by Spotify Million Song Dataset via Kaggle
- 🌍 **Multilingual**: AI lyrics in 10 languages (English + 9 Indian languages)
- 🎼 **Integrated AI Tools**: No external redirects - everything built-in
- 🌤️ **Weather Intelligence**: Music that matches your environment
- ⚡ **Optimized Performance**: On-demand similarity computation for instant results
- 🎨 **Modern UI**: Bootstrap 5 with glassmorphism and light theme

**Truly ONE PLACE FOR ALL your music needs!**

---

## ✨ Complete Feature Set

### 🧠 AI-Powered Music Recommendations
- **Massive Dataset**: 57,648 songs with full lyrics from Spotify Million Song Dataset
- **Advanced TF-IDF**: 10,000 feature matrix for precise recommendations
- **On-Demand Similarity**: Efficient computation for instant results
- **643 Unique Artists**: Diverse music catalog
- **Smart Search**: Autocomplete with song and artist search
- **Similarity Scoring**: Visual match percentage for each recommendation
- **Artist Weighting**: Prioritizes artist similarity for better matches

### 🌍 Multilingual AI Lyrics Generator (Built-in)
- **10 Languages Supported**:
  - English (Global)
  - Hindi (हिंदी)
  - Kannada (ಕನ್ನಡ)
  - Tamil (தமிழ்)
  - Telugu (తెలుగు)
  - Malayalam (മലയാളം)
  - Marathi (मराठी)
  - Bengali (বাংলা)
  - Punjabi (ਪੰਜਾਬੀ)
  - Gujarati (ગુજરાતી)

- **Features**:
  - Custom theme/topic input
  - 8+ genre options (Pop, Rock, Jazz, Hip-Hop, etc.)
  - 6 mood selections (Happy, Sad, Romantic, etc.)
  - Verse-Chorus-Bridge structure
  - Copy to clipboard functionality
  - Download as .txt file
  - Native script display

### 🎼 AI Song Description Generator (Built-in)
- **Intelligent Analysis**:
  - Automatic genre detection from prompt
  - Mood/emotion extraction
  - Instrument identification
  - Tempo and BPM recommendations

- **Customization Options**:
  - Duration settings (Short/Medium/Long)
  - Tempo control (Slow/Medium/Fast with BPM)
  - Vocal options (Male/Female/Mixed/Instrumental)

- **Comprehensive Output**:
  - Detailed song specifications
  - Musical elements breakdown
  - Song structure recommendations
  - Production style guidance
  - Ready-to-use prompts for AI music platforms (Suno AI, Udio, MusicLM)

### 🌤️ Weather-Based Music Discovery
- **Automatic Location Detection**: GPS-based geolocation
- **Real-Time Weather**: OpenWeatherMap API integration
- **Smart Mood Mapping**: Weather conditions to music moods
- **Dynamic Playlists**: Adaptive song selection based on weather
- **Location Display**: City name and country information
- **Weather Details**: Temperature, humidity, conditions

### 🎵 Music Platform Integration
- **Spotify Integration**: Direct playback links
- **YouTube Music Integration**: Instant access
- **One-Click Streaming**: Opens in new tab
- **Smart Searching**: Song + artist combination
- **Non-Disruptive**: Background playback support

### 🎨 Modern UI/UX Experience (Bootstrap 5)
- **Light Theme**: Eye-friendly gradient background (Indigo → Pink)
- **Bootstrap 5.3.2**: Modern, responsive design
- **Glassmorphism Effects**: Beautiful frosted glass cards
- **Gradient Animations**: Smooth color transitions
- **Fully Responsive**: Mobile, tablet, desktop optimized
- **Loading States**: Professional indicators
- **Interactive Elements**: Hover effects and smooth transitions
- **Separate Pages**: Dedicated pages for each AI tool

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser
- Internet connection
- ~100MB free disk space (for dataset)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project.git
cd "AI-and-weather-Based-Music-Recommendation-System---Mini-Project"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download Spotify Dataset** (Automatic)
```bash
python download_dataset.py
```
This will:
- Download 57,650 songs from Kaggle
- Process and clean the data
- Save to `data/spotify_million_songs.csv`
- Display dataset statistics

**Note**: First-time Kaggle users need to set up API credentials:
1. Go to https://www.kaggle.com/settings
2. Click "Create New Token" under API section
3. Place `kaggle.json` in:
   - Windows: `C:\Users\<username>\.kaggle\`
   - Linux/Mac: `~/.kaggle/`

4. **Run the application**
```bash
python app.py
```

5. **Access the platform**
```
Open your browser and visit: http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
AI-Music-Hub/
├── app.py                          # Main Flask application
├── recommendation.py               # Original recommender (84 songs)
├── spotify_recommender.py          # Spotify dataset recommender (57K songs)
├── weather_recommendation.py       # Weather-based recommendations
├── download_dataset.py             # Kaggle dataset downloader
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── data/
│   ├── music_data.csv             # Original dataset (84 songs)
│   └── spotify_million_songs.csv  # Kaggle dataset (57,650 songs)
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom styles + Bootstrap overrides
│   └── js/
│       ├── script.js              # Main application logic
│       ├── lyrics.js              # Lyrics generator functionality
│       └── song-generator.js      # Song description generator
│
└── templates/
    ├── index.html                 # Homepage
    ├── lyrics_generator.html      # Dedicated lyrics page
    ├── song_generator.html        # Dedicated song generator page
    └── song_creator.html          # Suno AI information page
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **ML Library**: Scikit-learn 1.3.2
- **Data Processing**: Pandas 2.1.3, NumPy 1.26.2
- **API Integration**: Requests 2.31.0
- **Dataset**: Kagglehub 0.3.13

### Frontend
- **Framework**: Bootstrap 5.3.2
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JS (ES6+)
- **Styling**: Custom CSS with Bootstrap overrides

### Machine Learning
- **Algorithm**: TF-IDF Vectorization + Cosine Similarity
- **Features**: 10,000 TF-IDF features
- **Matrix**: 57,648 × 10,000 sparse matrix
- **Optimization**: On-demand similarity computation

### APIs
- **Weather**: OpenWeatherMap API
- **Dataset**: Kaggle API

---

## 🎯 Use Cases

### For Music Lovers
- Discover new songs similar to favorites
- Find music matching current weather
- Generate custom lyrics in native language
- Create song concepts for AI platforms

### For Content Creators
- Generate song ideas and descriptions
- Create lyrics for original compositions
- Find inspiration from AI-generated content
- Access diverse music catalog

### For Developers
- Learn Flask application structure
- Understand ML recommendation systems
- Study TF-IDF implementation at scale
- Explore API integrations

### For Students
- Complete AIML mini project reference
- Machine learning practical implementation
- Full-stack development example
- Dataset integration techniques

---

## 📊 Dataset Information

### Spotify Million Song Dataset
- **Source**: Kaggle (notshrirang/spotify-million-song-dataset)
- **Total Songs**: 57,650
- **Unique Artists**: 643
- **Columns**: artist, song, link, text (lyrics)
- **Size**: ~82 MB
- **Features**: Full song lyrics for accurate recommendations

### Original Dataset
- **Total Songs**: 84
- **Columns**: song, artist, genre, mood, lyrics
- **Used As**: Fallback if Spotify dataset unavailable

---

## 🔑 Key Features Explained

### 1. On-Demand Similarity Computation
Instead of pre-computing a 57K × 57K similarity matrix (requiring 13GB+ memory), we:
- Store only the TF-IDF matrix (sparse)
- Compute similarities when requested
- Process one song at a time
- Deliver instant results with minimal memory

### 2. Multilingual Lyrics Generation
- Template-based generation for consistency
- Language-specific structures and expressions
- Native script support
- Cultural appropriateness in lyrics

### 3. Intelligent Song Analysis
- NLP-based prompt analysis
- Keyword extraction for genre/mood/instruments
- Smart mapping to musical elements
- Platform-ready output formatting

---

## 🌐 API Integration

### OpenWeatherMap API
```python
API_KEY = "782e98aa47114ab48de111603252110"
Endpoint: https://api.openweathermap.org/data/2.5/weather
Rate Limit: 1,000 calls/day (free tier)
```

### Kaggle API
```bash
Dataset: notshrirang/spotify-million-song-dataset
Authentication: kaggle.json credentials
Auto-download: Via kagglehub library
```

---

## 📱 Screenshots & Demo

### Homepage
- Music recommendations with search
- Weather-based discovery
- AI tools overview

### Lyrics Generator
- 10 language options
- Genre and mood selection
- Instant generation with copy/download

### Song Generator
- Detailed prompt input
- Customization options
- Comprehensive AI analysis output

---

## 🚧 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save favorite songs and playlists
- [ ] More languages for lyrics (50+ total)
- [ ] Advanced song generation with actual audio
- [ ] Social sharing features
- [ ] Playlist export to Spotify/YouTube
- [ ] Voice input for song descriptions
- [ ] Collaborative playlist creation
- [ ] Mobile app development

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Harshavardhan K R**
- GitHub: [@hvkr15](https://github.com/hvkr15)
- Repository: [AI-Music-Hub](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project)

---

## 🙏 Acknowledgments

- **Kaggle** - For the Spotify Million Song Dataset
- **OpenWeatherMap** - Weather API service
- **Bootstrap Team** - UI framework
- **Font Awesome** - Icon library
- **Flask Community** - Web framework
- **Scikit-learn** - Machine learning library

---

## 📞 Support

For support, issues, or feature requests:
- Open an issue on GitHub
- Star ⭐ the repository if you find it useful
- Share with fellow developers and music enthusiasts!

---

<div align="center">

**Made with ❤️ for Music and AI**

🎵 **AI Music Hub** - One Place for All 🎵

</div>
