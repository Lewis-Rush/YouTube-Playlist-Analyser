import pprint
from utils import *

def main():

    API_KEY = get_api_key()

    playlist_url = input("Enter playlist URL: ")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    playlist = get_playlist(playlist_url, youtube)

    playlist_length = playlist['pageInfo']['totalResults']

    playlist_runtime = get_playlist_runtime(playlist, youtube)

    print("Total playlist runtime: ", str(datetime.timedelta(seconds=playlist_runtime)))

    print(playlist_runtime)

    print(playlist_length)


main()