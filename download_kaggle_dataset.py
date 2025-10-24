"""
Download and integrate Spotify Indian Languages Dataset from Kaggle
"""
import kagglehub
import pandas as pd
import os
import shutil

def download_indian_dataset():
    """Download Spotify Indian Languages dataset from Kaggle"""
    try:
        print("=" * 60)
        print("📥 DOWNLOADING SPOTIFY INDIAN LANGUAGES DATASET")
        print("=" * 60)
        
        # Download latest version
        print("\n🔄 Downloading from Kaggle...")
        path = kagglehub.dataset_download("gayathripullakhandam/spotify-indian-languages-datasets")
        
        print(f"✓ Downloaded to: {path}")
        
        # List files in downloaded path
        print("\n📁 Files in dataset:")
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                print(f"  - {file} ({file_size:.2f} MB)")
        
        return path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        import traceback
        traceback.print_exc()
        return None

def integrate_dataset(dataset_path):
    """Integrate the downloaded dataset into the project"""
    try:
        print("\n" + "=" * 60)
        print("🔧 INTEGRATING DATASET INTO PROJECT")
        print("=" * 60)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Find CSV files in the downloaded path
        csv_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
        
        if not csv_files:
            print("❌ No CSV files found in downloaded dataset")
            return False
        
        print(f"\n📊 Found {len(csv_files)} CSV file(s)")
        
        # Load and combine all CSV files
        all_data = []
        for csv_file in csv_files:
            print(f"\n🔄 Loading: {os.path.basename(csv_file)}")
            df = pd.read_csv(csv_file)
            print(f"  - Shape: {df.shape}")
            print(f"  - Columns: {list(df.columns)}")
            all_data.append(df)
        
        # Combine all dataframes
        if len(all_data) > 1:
            combined_df = pd.concat(all_data, ignore_index=True)
            print(f"\n✓ Combined all datasets")
        else:
            combined_df = all_data[0]
        
        print(f"\n📊 Final Dataset Statistics:")
        print(f"  - Total Songs: {len(combined_df)}")
        print(f"  - Columns: {list(combined_df.columns)}")
        
        # Save to project data folder
        output_path = 'data/spotify_indian_languages.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"\n✓ Saved to: {output_path}")
        
        # Show sample data
        print("\n📋 Sample Data (first 3 rows):")
        print(combined_df.head(3))
        
        return True
        
    except Exception as e:
        print(f"❌ Error integrating dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎵 SPOTIFY INDIAN LANGUAGES DATASET DOWNLOADER")
    print("=" * 60)
    
    # Download dataset
    dataset_path = download_indian_dataset()
    
    if dataset_path:
        # Integrate into project
        success = integrate_dataset(dataset_path)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ DATASET SUCCESSFULLY INTEGRATED!")
            print("=" * 60)
            print("\n📝 Next Steps:")
            print("  1. Check data/spotify_indian_languages.csv")
            print("  2. Update app.py to use this dataset")
            print("  3. Restart your Flask server")
            print("\n🎵 Ready to use Indian Languages dataset!")
        else:
            print("\n❌ Failed to integrate dataset")
    else:
        print("\n❌ Failed to download dataset")
