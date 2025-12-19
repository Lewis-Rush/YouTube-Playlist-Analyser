from googleapiclient.discovery import build
from src.utils import get_api_key, get_playlist, no_videos_watched, has_watched_videos


def main():
    """
    The main function that will be called when the program is ran. It calls the
    util functions in the correct order to give the user information about a
    given playlist
    """
    API_KEY = get_api_key()

    youtube = build("youtube", "v3", developerKey=API_KEY)

    playlist_url = input("Enter playlist URL: ")

    videos_watched = int(input("Enter amount of videos watched: \n"))

    playlist = get_playlist(playlist_url, youtube)

    playlist_length = playlist["pageInfo"]["totalResults"]

    if not videos_watched:
        no_videos_watched(playlist, playlist_length, youtube)

    else:
        playlist_length = playlist_length - videos_watched
        has_watched_videos(playlist, playlist_length, youtube, videos_watched)


if __name__ == "__main__":
    main()
