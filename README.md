# Music Downloader From Deezer 🐀


Originally this project was made by me to get out of the Deezer ecosystem and stop paying money every month because why not ? 🐀

Because the deezer API does not allow any creation of Token to access account playlists and bypassing by creating app does not work anymore as well.
[Source 1](https://www.reddit.com/r/deezer/comments/1bizi0k/i_cant_get_api_key_for_some_reason/)
[Source 2](https://developers.deezer.com/api/search)

## How to use ?

### Preparing the Excel File

The deezer playlist where extracted from [tunemymusic](https://www.tunemymusic.com/) for free by linking Deezer Account.
Exporting the CSV and changing the format to UTF-8 using ```.xlsx``` to include all the languages in the correct format and separating the columns of the ```.xlsx```.

After that this script is used to download music from youtube and add metadata of the song in the ```.mp3``` downloaded.

Create an Excel file (e.g., songs.xlsx) with the following structure:

| Track name |	Artist name |
| ------------- | ------------- |
| Shape of You |	Ed Sheeran |
| Blinding Lights |	The Weeknd |


### Installing Dependencies from requirements.txt :
Once you've created the requirements.txt file, you can install all the required packages using the following command:
```pip install -r requirements.txt```

### Usage :

Changing the Excel File Path If your Excel file is named differently or located in another directory, modify the excel_file variable in the script:

```excel_file = 'YourExcelFile.xlsx'  # Replace with your Excel file path```

Changing the Output Folder By default, the output folder is named after the Excel file (without the .xlsx extension). To change it, modify the output_folder variable:
```output_folder = 'YourDesiredOutputFolder'```

Adjusting Filename Format The script uses the format {Track name} - {Artist name}.mp3. To customize, edit the outtmpl parameter in the download_song_youtube function:
```'outtmpl': os.path.join(output_folder, f"{track_name} - {artist_name}.%(ext)s"),```
