import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class IndianLanguagesRecommender:
    """
    Content-based music recommendation system for Indian Languages Dataset
    Optimized for Spotify Indian Languages Dataset from Kaggle
    """
    
    def __init__(self, df):
        """
        Initialize the recommender with Indian Languages dataset
        
        Args:
            df: Pandas DataFrame with columns:
                'song_name', 'singer', 'language', 'danceability', 'energy', 
                'acousticness', 'valence', 'tempo', 'popularity', etc.
        """
        self.df = df.copy()
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.tfidf_vectorizer = None
        self._preprocess_data()
        self._build_recommendation_model()
    
    def _preprocess_data(self):
        """Preprocess the Indian Languages music data"""
        # Clean and prepare data
        self.df['song_name'] = self.df['song_name'].fillna('Unknown')
        self.df['singer'] = self.df['singer'].fillna('Unknown')
        self.df['language'] = self.df['language'].fillna('Unknown')
        
        # Fill numeric features
        numeric_features = ['danceability', 'acousticness', 'energy', 'liveness', 
                          'loudness', 'speechiness', 'tempo', 'Valence', 'popularity']
        for feature in numeric_features:
            if feature in self.df.columns:
                self.df[feature] = self.df[feature].fillna(self.df[feature].median())
        
        # Create combined features for text-based recommendation
        # Language (repeated 2x for weight) + Singer (repeated 3x) + Song name
        self.df['combined_features'] = (
            self.df['language'].astype(str) + ' ' +
            self.df['language'].astype(str) + ' ' +
            self.df['singer'].astype(str) + ' ' +
            self.df['singer'].astype(str) + ' ' +
            self.df['singer'].astype(str) + ' ' +
            self.df['song_name'].astype(str)
        )
        
        # Add audio features as text for better matching
        if 'danceability' in self.df.columns and 'energy' in self.df.columns:
            self.df['combined_features'] += ' ' + self.df.apply(
                lambda x: self._audio_features_to_text(x), axis=1
            )
        
        # Clean up the text
        self.df['combined_features'] = self.df['combined_features'].str.lower()
        
        # Remove duplicates
        self.df = self.df.drop_duplicates(subset=['song_name', 'singer'], keep='first')
        self.df = self.df.reset_index(drop=True)
        
        print(f"✓ Preprocessed {len(self.df)} unique songs")
    
    def _audio_features_to_text(self, row):
        """Convert audio features to descriptive text"""
        desc = []
        
        # Danceability
        if row['danceability'] > 0.7:
            desc.append('high_dance')
        elif row['danceability'] < 0.3:
            desc.append('low_dance')
        
        # Energy
        if row['energy'] > 0.7:
            desc.append('high_energy')
        elif row['energy'] < 0.3:
            desc.append('low_energy')
        
        # Acousticness
        if row['acousticness'] > 0.5:
            desc.append('acoustic')
        
        # Valence (mood)
        if row['Valence'] > 0.7:
            desc.append('happy')
        elif row['Valence'] < 0.3:
            desc.append('sad')
        
        return ' '.join(desc)
    
    def _build_recommendation_model(self):
        """Build TF-IDF model for content-based recommendations"""
        print("🔄 Building TF-IDF matrix for {} songs...".format(len(self.df)))
        
        # Create TF-IDF matrix with optimized parameters
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=1,
            max_df=0.8
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.df['combined_features']
        )
        
        print(f"✓ Recommendation model built successfully!")
        print(f"  - Dataset size: {len(self.df)} songs")
        print(f"  - Feature matrix shape: {self.tfidf_matrix.shape}")
        print(f"  - Languages: {self.df['language'].nunique()}")
        print(f"  - Unique singers: {self.df['singer'].nunique()}")
        print(f"  - Using on-demand similarity computation for efficiency")
    
    def get_recommendations(self, song_name, n_recommendations=10):
        """
        Get song recommendations based on a given song
        
        Args:
            song_name: Name of the song to base recommendations on
            n_recommendations: Number of recommendations to return
            
        Returns:
            DataFrame with recommended songs
        """
        try:
            # Find the song in the dataset (case-insensitive partial match)
            song_matches = self.df[
                self.df['song_name'].str.lower().str.contains(song_name.lower(), na=False)
            ]
            
            if len(song_matches) == 0:
                print(f"Song '{song_name}' not found in database")
                return None
            
            # Use the first match
            song_idx = song_matches.index[0]
            song_row = self.df.loc[song_idx]
            
            print(f"\n🎵 Base Song: {song_row['song_name']} by {song_row['singer']}")
            print(f"   Language: {song_row['language']}")
            
            # Compute similarity only for this song (memory efficient)
            song_vector = self.tfidf_matrix[song_idx]
            similarity_scores = cosine_similarity(song_vector, self.tfidf_matrix).flatten()
            
            # Get top N similar songs (excluding the input song itself)
            similar_indices = similarity_scores.argsort()[::-1][1:n_recommendations+1]
            
            # Return recommended songs with similarity scores
            recommendations = self.df.iloc[similar_indices].copy()
            recommendations['similarity_score'] = similarity_scores[similar_indices]
            recommendations['similarity_percentage'] = (
                recommendations['similarity_score'] * 100
            ).round(1)
            
            return recommendations[[
                'song_name', 'singer', 'language', 'popularity', 
                'danceability', 'energy', 'Valence', 
                'similarity_score', 'similarity_percentage'
            ]]
            
        except Exception as e:
            print(f"Error in recommendation: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def search_songs(self, query, limit=20):
        """
        Search for songs by name or singer
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            DataFrame with matching songs
        """
        query_lower = query.lower()
        
        # Search in song name and singer
        mask = (
            self.df['song_name'].str.lower().str.contains(query_lower, na=False) |
            self.df['singer'].str.lower().str.contains(query_lower, na=False)
        )
        
        results = self.df[mask].head(limit)
        
        return results[[
            'song_name', 'singer', 'language', 'popularity', 
            'danceability', 'energy', 'Valence'
        ]]
    
    def get_songs_by_language(self, language, limit=50):
        """Get songs in a specific language"""
        language_songs = self.df[
            self.df['language'].str.lower() == language.lower()
        ].head(limit)
        
        return language_songs[[
            'song_name', 'singer', 'language', 'popularity',
            'danceability', 'energy', 'Valence'
        ]]
    
    def get_dataset_info(self):
        """Get information about the dataset"""
        info = {
            'total_songs': len(self.df),
            'languages': sorted(self.df['language'].unique().tolist()),
            'language_counts': self.df['language'].value_counts().to_dict(),
            'total_singers': self.df['singer'].nunique(),
            'avg_popularity': self.df['popularity'].mean() if 'popularity' in self.df.columns else None
        }
        return info
