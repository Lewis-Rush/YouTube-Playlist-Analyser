import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

def get_api_key():
    api_key = os.environ.get("API_KEY")

    if not api_key:
        raise Exception("No api key found")

    return api_key

def extract_playlist_id(playlist_url):
    if "youtube.com" not in playlist_url and "youtu.be" not in playlist_url:
        raise Exception("Invalid URL")
    
    if "list=" not in playlist_url:
        raise Exception("URL not a playlist")
    
    list_location = playlist_url.find("list=")

    playlist_id = playlist_url[(list_location + 5):]

    if "&" in playlist_id:
        playlist_id = playlist_id[: playlist_id.find("&")]

    return playlist_id

def get_playlist(playlist_url, youtube):

    playlist_id = extract_playlist_id(playlist_url)
    
    try:
        request = youtube.playlistItems().list(
        part="snippet",
        playlistId=f"{playlist_id}",
        maxResults=50
        )

        response = request.execute()

    except HttpError:
        raise Exception("Error getting playlist")
      
    return response

def get_videos(video_ids, youtube):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_ids
    )
    
    return request


def get_playlist_runtime(playlist):
    video_ids = [item['id'] for item in playlist['items']]

    return video_ids