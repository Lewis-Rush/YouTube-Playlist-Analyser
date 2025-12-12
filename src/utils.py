import os
import re
import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


def get_api_key():
    """
    A function to get the api key from the .env file

    input:
    None

    Output:
    if no key - An error is raised

    if a key exists - Returns the api key - string
    """
    api_key = os.environ.get("API_KEY")

    if not api_key:
        raise Exception("No api key found")

    return api_key


def extract_playlist_id(playlist_url):
    """
    A function to extract the playlist id from a given YouTube url

    input:
    A YouTube url - string

    output:
    A YouTube playlist id - string
    """
    if "youtube.com" not in playlist_url and "youtu.be" not in playlist_url:
        raise Exception("Invalid URL")

    if "list=" not in playlist_url:
        raise Exception("URL not a playlist")

    list_location = playlist_url.find("list=")

    playlist_id = playlist_url[(list_location + 5) :]

    if "&" in playlist_id:
        playlist_id = playlist_id[: playlist_id.find("&")]

    return playlist_id


def get_playlist(playlist_url, youtube):
    """
    A function to make a request to the YouTube api and return a dictionary
    of videos from a given playlist

    input:
    A YouTube playlist url - string
    A build object for the YouTube api

    output:
    If theres an error retrieving the playlist - an error will be raised
    If the request is successful - A dictionary of videos and information about them - dict
    """
    playlist_id = extract_playlist_id(playlist_url)

    try:
        request = youtube.playlistItems().list(
            part="snippet", playlistId=f"{playlist_id}", maxResults=50
        )

        response = request.execute()

    except HttpError:
        raise Exception("Error getting playlist")

    return response


def get_videos(video_ids, youtube):
    """
    A function that will request information about a given list of videos from the YouTube api

    input:
    A list of video ids - List of strings
    A build object for the YouTube api

    output:
    A dictionary of videos and information about them
    """
    request = youtube.videos().list(part="contentDetails", id=video_ids)

    return request


def convert_times(times):
    """
    A function to convert a list of times from the YouTube formatted times to
    a list of seconds

    input:
    A list of YouTube formatted times - list of strings

    output:
    A list of times converted into seconds - list of ints
    """
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
    """
    A function to take a given playlist and find out the total runtime of all the
    videos in that playlist

    input:
    A YouTube playlist - A dictionary of playlist videos
    A build object for the YouTube api

    output:
    The total time of all the videos given in seconds - int
    """
    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist["items"]]

    videos = get_videos(video_ids, youtube)

    videos_response = videos.execute()

    playlist_times = [
        item["contentDetails"]["duration"] for item in videos_response["items"]
    ]

    converted_times = convert_times(playlist_times)

    return sum(converted_times)


def get_average_video_runtime(runtime, video_count):
    """
    A function to get the average runtime of a video in a given playlist

    input:
    The runtime of a playlist in seconds - int
    The number of items in the playlist - int

    output:
    the average runtime of a video in the playlist - datetime
    """
    average_video_runtime = runtime / video_count

    return str(datetime.timedelta(seconds=average_video_runtime))


def no_videos_watched(playlist, playlist_length, youtube):
    """
    A function for if the user hasn't watched any of the videos in the
    playlist

    input:
    A YouTube playlist - A dictionary of playlist videos
    The number of items in the playlist - int
    A build object for the YouTube

    output:
    prints to the screen information about the playlist
    """
    playlist_runtime = get_playlist_runtime(playlist, youtube)

    average_video_runtime = get_average_video_runtime(playlist_runtime, playlist_length)

    print("No videos watched")

    print("Total playlist runtime: ", str(datetime.timedelta(seconds=playlist_runtime)))

    print("Average video runtime: ", average_video_runtime)

    print("Playlist length: ", playlist_length)


def has_watched_videos(playlist, playlist_length, youtube, videos_watched):
    """
    A function for if the user has watched videos in the
    playlist

    input:
    A YouTube playlist - A dictionary of playlist videos
    The number of items in the playlist - int
    A build object for the YouTube
    The amount of videos watched - int

    output:
    prints to the screen information about the playlist
    """
    remaining_items = playlist["items"][videos_watched:]

    updated_playlist = {
        **playlist,
        "items": remaining_items
    }

    playlist_length = len(remaining_items)

    playlist_runtime = get_playlist_runtime(updated_playlist, youtube)
    average_video_runtime = get_average_video_runtime(
        playlist_runtime,
        playlist_length
    )

    print("Playlist time left: ", str(datetime.timedelta(seconds=playlist_runtime)))
    print("Average runtime of videos left: ", average_video_runtime)
    print("Videos left: ", playlist_length)
