import os
import pandas as pd
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
from PIL import Image
import requests
from io import BytesIO

# Function to download YouTube video as MP3
def download_song_youtube(track_name, artist_name, output_folder):
    search_query = f"{track_name} {artist_name}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, f"{track_name} - {artist_name}.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=True)['entries'][0]
            return os.path.join(output_folder, f"{track_name} - {artist_name}.mp3"), info['thumbnail']
        except Exception as e:
            print(f"Error downloading {track_name} by {artist_name}: {e}")
            return None, None

# Function to add metadata to MP3
def add_metadata(mp3_file, track_name, artist_name, thumbnail_url):
    try:
        # Load the MP3 file
        audio = MP3(mp3_file, ID3=ID3)

        if audio.tags is None:
            audio.add_tags()

        # Add track name and artist name as metadata
        audio.tags.add(TIT2(encoding=3, text=track_name))  # Title
        audio.tags.add(TPE1(encoding=3, text=artist_name))  # Artist

        # Download thumbnail image and add as album art
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                img_byte_array = BytesIO()
                img.save(img_byte_array, format='JPEG')
                audio.tags.add(APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',  # Image MIME type
                    type=3,  # Album cover
                    desc='Cover',
                    data=img_byte_array.getvalue()
                ))
            except Exception as e:
                print(f"Error adding album art: {e}")

        # Save the updated metadata
        audio.save()
        print(f"Metadata added to {mp3_file}")
    except Exception as e:
        print(f"Error adding metadata to {mp3_file}: {e}")

# Main script
def main():
    # Provide a list of Excel files you want to process
    excel_files = [
        'YourExcelFile.xlsx',
        'YourExcelFile2.xlsx',
    ]  # Replace with your Excel file path

    for excel_file in excel_files:
        print(f"\nProcessing Excel file: {excel_file}")
        output_folder = excel_file.replace(".xlsx", "")
        os.makedirs(output_folder, exist_ok=True)

        # Read the Excel file
        data = pd.read_excel(excel_file, engine='openpyxl')

        # Ensure required columns are present
        if 'Track name' not in data.columns or 'Artist name' not in data.columns:
            raise ValueError("The Excel file must have 'Track name' and 'Artist name' columns.")

        # Loop through each row
        for index, row in data.iterrows():
            track_name = row['Track name']
            artist_name = row['Artist name']

            print(f"  → {track_name} by {artist_name}")

            # Download song
            mp3_file, thumbnail_url = download_song_youtube(track_name, artist_name, output_folder)

            if mp3_file:
                # Add metadata
                add_metadata(mp3_file, track_name, artist_name, thumbnail_url)

    print("\nAll songs from all Excel files processed!")

if __name__ == "__main__":
    main()