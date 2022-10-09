"""gets album cover images from a specific playlist"""
import spotipy
import requests
import shutil
import os
from spotipy.oauth2 import SpotifyOAuth

# In terminal (use 'set' on Windows):
#  export SPOTIPY_CLIENT_ID=""
#  export SPOTIPY_CLIENT_SECRET=""
#  export SPOTIPY_REDIRECT_URI=""

SCOPE  = "user-library-read"
SP = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

def get_album_covers(playlist_id):

    playlist = SP.playlist(playlist_id)
    playlist_total_tracks = playlist['tracks']['total']
    album_cover_links = []

    for i in range(0, playlist_total_tracks + 1, 100):
        tracks = SP.playlist_tracks(playlist_id, offset=i)

        for idx, item in enumerate(tracks['items']):
            track = item['track']
            album_cover_links.append(track['album']['images'][0]['url'])
            #  print(idx + i + 1, track['artists'][0]['name'], " - ", track['name'], ": ", track["album"]["images"][0]["url"])
    return album_cover_links

def remove_duplicate_links(links):
    seen = set()
    sorted_links = []
    for link in sorted(links):
        if link not in seen:
            sorted_links.append(link)
            seen.add(link)

    return sorted_links

def download_images(links, download_dir):

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for link in links:
        filename = link.split("/")[-1]
        dest = download_dir + "/" + filename + ".png"
        
        r = requests.get(link, stream = True)

        if r.status_code == 200:
            r.raw.decode_content = True
            # This needs to be set or else file size will be 0

            with open(dest, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print(f"Image \"{filename}.png\" was successfully downloaded {links.index(link) + 1}/{len(links)}")
        else:
            print(f"Error: \"{filename}\" could not be downloaded.")


def get_playlist_id():
    try:
        playlist_link = input("Spotify playlist link:\n")
        playlist_id = playlist_link.split("/")[-1]
        return playlist_id

    except:
        print("Error: invalid link")
        return False


if __name__ == "__main__":
    DOWNLOAD_DIR = "./covers"

    PLAYLIST_ID = get_playlist_id()

    if not PLAYLIST_ID:
        exit()

    album_cover_links = get_album_covers(PLAYLIST_ID)
    sorted_links = remove_duplicate_links(album_cover_links)

    print(f"Playlist with {len(album_cover_links)} has {len(sorted_links)} albums.")
    print(f"Downloading album covers in {DOWNLOAD_DIR}")

    download_images(sorted_links, DOWNLOAD_DIR)


