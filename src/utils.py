import os
import re
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

def convert_times(times):
    converted_list = []

    for time in times:
        pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
        hours, minutes, seconds = re.match(pattern, time).groups()

        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0

        converted_list.append(hours * 3600 + minutes * 60 + seconds)

    return converted_list

def get_playlist_runtime(playlist, youtube):
    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist["items"]]

    videos = get_videos(video_ids, youtube)

    videos_response = videos.execute()

    playlist_times = [item["contentDetails"]["duration"]for item in videos_response["items"]]

    runtime = convert_times(playlist_times)

    return sum(runtime)