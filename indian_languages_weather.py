import requests
import pandas as pd
from datetime import datetime
import numpy as np

class IndianLanguagesWeatherRecommender:
    """
    Weather-based music recommendation system for Indian Languages Dataset
    Suggests Indian language songs based on current weather conditions
    """
    
    def __init__(self, df, api_key=None):
        """
        Initialize weather-based recommender for Indian Languages
        
        Args:
            df: Pandas DataFrame with Indian Languages music data
            api_key: OpenWeatherMap API key
        """
        self.df = df
        self.api_key = api_key or "34dc98c68f184a59a5a5e93a2487fe58"
        
        # Define weather to audio feature mappings
        self.weather_audio_map = {
            'Clear': {
                'energy_range': (0.6, 1.0),
                'valence_range': (0.6, 1.0),  # Happy
                'danceability_range': (0.5, 1.0),
                'mood': 'happy'
            },
            'Clouds': {
                'energy_range': (0.3, 0.6),
                'valence_range': (0.4, 0.7),  # Calm
                'danceability_range': (0.3, 0.6),
                'mood': 'calm'
            },
            'Rain': {
                'energy_range': (0.2, 0.5),
                'valence_range': (0.2, 0.5),  # Melancholic
                'danceability_range': (0.2, 0.5),
                'mood': 'melancholic'
            },
            'Drizzle': {
                'energy_range': (0.3, 0.6),
                'valence_range': (0.3, 0.6),  # Relaxed
                'danceability_range': (0.3, 0.6),
                'mood': 'relaxed'
            },
            'Thunderstorm': {
                'energy_range': (0.7, 1.0),
                'valence_range': (0.5, 0.8),  # Energetic
                'danceability_range': (0.6, 1.0),
                'mood': 'energetic'
            },
            'Snow': {
                'energy_range': (0.2, 0.5),
                'valence_range': (0.5, 0.8),  # Peaceful
                'danceability_range': (0.2, 0.5),
                'mood': 'peaceful'
            },
            'Mist': {
                'energy_range': (0.3, 0.6),
                'valence_range': (0.4, 0.7),
                'danceability_range': (0.3, 0.6),
                'mood': 'calm'
            },
            'Fog': {
                'energy_range': (0.3, 0.6),
                'valence_range': (0.4, 0.7),
                'danceability_range': (0.3, 0.6),
                'mood': 'calm'
            },
            'Haze': {
                'energy_range': (0.4, 0.7),
                'valence_range': (0.4, 0.7),
                'danceability_range': (0.4, 0.7),
                'mood': 'relaxed'
            }
        }
        
        # Temperature-based adjustments
        self.temp_adjustments = {
            'very_cold': {'energy': -0.2, 'valence': -0.1},  # < 0°C
            'cold': {'energy': -0.1, 'valence': 0.0},        # 0-15°C
            'mild': {'energy': 0.0, 'valence': 0.1},         # 15-25°C
            'warm': {'energy': 0.1, 'valence': 0.2},         # 25-35°C
            'hot': {'energy': 0.2, 'valence': 0.1}           # > 35°C
        }
    
    def get_weather_data(self, latitude, longitude):
        """
        Fetch current weather data from OpenWeatherMap API
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            Dictionary with weather information
        """
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get city and country information
                city_name = data.get('name', 'Unknown Location')
                country_code = data.get('sys', {}).get('country', '')
                
                # Create full location name
                if country_code:
                    full_location = f"{city_name}, {country_code}"
                else:
                    full_location = city_name
                
                weather_info = {
                    'condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'city': full_location,
                    'icon': data['weather'][0]['icon']
                }
                
                return weather_info
            else:
                print(f"Weather API Error: {response.status_code}")
                return self._get_demo_weather()
                
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_demo_weather()
    
    def _get_demo_weather(self):
        """Return demo weather data for testing"""
        return {
            'condition': 'Clear',
            'description': 'clear sky',
            'temperature': 25,
            'feels_like': 24,
            'humidity': 60,
            'city': 'Demo City (API Key Required)',
            'icon': '01d'
        }
    
    def _get_temp_category(self, temperature):
        """Categorize temperature"""
        if temperature < 0:
            return 'very_cold'
        elif temperature < 15:
            return 'cold'
        elif temperature < 25:
            return 'mild'
        elif temperature < 35:
            return 'warm'
        else:
            return 'hot'
    
    def get_weather_based_recommendations(self, latitude, longitude, n_recommendations=15, language_preference=None):
        """
        Get Indian language song recommendations based on weather
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            n_recommendations: Number of songs to recommend
            language_preference: Preferred language (optional)
            
        Returns:
            Dictionary with weather info, mood, and recommendations
        """
        try:
            # Get current weather
            weather_info = self.get_weather_data(latitude, longitude)
            condition = weather_info['condition']
            temperature = weather_info['temperature']
            
            print(f"\n🌤️  Weather: {condition} - {weather_info['description']}")
            print(f"🌡️  Temperature: {temperature}°C")
            print(f"📍 Location: {weather_info['city']}")
            
            # Get audio feature ranges for this weather
            if condition not in self.weather_audio_map:
                condition = 'Clear'  # Default
            
            audio_ranges = self.weather_audio_map[condition]
            mood = audio_ranges['mood']
            
            # Get temperature adjustments
            temp_category = self._get_temp_category(temperature)
            temp_adj = self.temp_adjustments[temp_category]
            
            # Adjust ranges based on temperature
            energy_min = max(0, audio_ranges['energy_range'][0] + temp_adj['energy'])
            energy_max = min(1, audio_ranges['energy_range'][1] + temp_adj['energy'])
            valence_min = max(0, audio_ranges['valence_range'][0] + temp_adj['valence'])
            valence_max = min(1, audio_ranges['valence_range'][1] + temp_adj['valence'])
            dance_min = audio_ranges['danceability_range'][0]
            dance_max = audio_ranges['danceability_range'][1]
            
            print(f"🎭 Mood: {mood}")
            print(f"🎵 Looking for songs with:")
            print(f"   Energy: {energy_min:.1f} - {energy_max:.1f}")
            print(f"   Valence: {valence_min:.1f} - {valence_max:.1f}")
            print(f"   Danceability: {dance_min:.1f} - {dance_max:.1f}")
            
            # Filter songs based on audio features
            filtered_df = self.df[
                (self.df['energy'] >= energy_min) & (self.df['energy'] <= energy_max) &
                (self.df['Valence'] >= valence_min) & (self.df['Valence'] <= valence_max) &
                (self.df['danceability'] >= dance_min) & (self.df['danceability'] <= dance_max)
            ].copy()
            
            # If language preference is specified, filter by language
            if language_preference:
                lang_filtered = filtered_df[
                    filtered_df['language'].str.lower() == language_preference.lower()
                ]
                if len(lang_filtered) >= n_recommendations:
                    filtered_df = lang_filtered
                    print(f"   Language: {language_preference}")
            
            if len(filtered_df) == 0:
                print("⚠️  No exact matches found, relaxing criteria...")
                # Relax the criteria
                filtered_df = self.df[
                    (self.df['energy'] >= energy_min - 0.2) & (self.df['energy'] <= energy_max + 0.2)
                ].copy()
            
            # Calculate matching score
            filtered_df['weather_match_score'] = (
                (1 - abs(filtered_df['energy'] - (energy_min + energy_max) / 2)) * 0.4 +
                (1 - abs(filtered_df['Valence'] - (valence_min + valence_max) / 2)) * 0.4 +
                (1 - abs(filtered_df['danceability'] - (dance_min + dance_max) / 2)) * 0.2
            )
            
            # Sort by match score and popularity
            filtered_df['combined_score'] = (
                filtered_df['weather_match_score'] * 0.7 +
                (filtered_df['popularity'] / 100) * 0.3
            )
            
            # Get top recommendations
            recommendations = filtered_df.nlargest(n_recommendations, 'combined_score')
            
            print(f"✓ Found {len(recommendations)} matching songs")
            
            # Prepare result
            result = {
                'weather': weather_info,
                'mood': mood,
                'recommendations': recommendations[[
                    'song_name', 'singer', 'language', 'popularity',
                    'energy', 'danceability', 'Valence', 
                    'weather_match_score', 'combined_score'
                ]]
            }
            
            return result
            
        except Exception as e:
            print(f"Error in weather-based recommendations: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_recommendations_by_mood(self, mood, n_recommendations=15, language_preference=None):
        """
        Get recommendations based on mood (without weather API)
        
        Args:
            mood: Mood string (happy, sad, energetic, calm, relaxed)
            n_recommendations: Number of recommendations
            language_preference: Preferred language (optional)
            
        Returns:
            DataFrame with recommended songs
        """
        mood_map = {
            'happy': {'energy': (0.6, 1.0), 'valence': (0.6, 1.0), 'dance': (0.5, 1.0)},
            'sad': {'energy': (0.2, 0.5), 'valence': (0.0, 0.4), 'dance': (0.2, 0.5)},
            'energetic': {'energy': (0.7, 1.0), 'valence': (0.5, 1.0), 'dance': (0.6, 1.0)},
            'calm': {'energy': (0.3, 0.6), 'valence': (0.4, 0.7), 'dance': (0.3, 0.6)},
            'relaxed': {'energy': (0.3, 0.6), 'valence': (0.4, 0.7), 'dance': (0.3, 0.6)},
            'romantic': {'energy': (0.3, 0.6), 'valence': (0.5, 0.8), 'dance': (0.3, 0.6)},
            'party': {'energy': (0.7, 1.0), 'valence': (0.7, 1.0), 'dance': (0.7, 1.0)}
        }
        
        if mood.lower() not in mood_map:
            mood = 'happy'
        
        ranges = mood_map[mood.lower()]
        
        # Filter songs
        filtered_df = self.df[
            (self.df['energy'] >= ranges['energy'][0]) & 
            (self.df['energy'] <= ranges['energy'][1]) &
            (self.df['Valence'] >= ranges['valence'][0]) & 
            (self.df['Valence'] <= ranges['valence'][1]) &
            (self.df['danceability'] >= ranges['dance'][0]) & 
            (self.df['danceability'] <= ranges['dance'][1])
        ].copy()
        
        # Language preference
        if language_preference:
            lang_filtered = filtered_df[
                filtered_df['language'].str.lower() == language_preference.lower()
            ]
            if len(lang_filtered) >= n_recommendations:
                filtered_df = lang_filtered
        
        # Sort by popularity
        recommendations = filtered_df.nlargest(n_recommendations, 'popularity')
        
        return recommendations[[
            'song_name', 'singer', 'language', 'popularity',
            'energy', 'danceability', 'Valence'
        ]]
