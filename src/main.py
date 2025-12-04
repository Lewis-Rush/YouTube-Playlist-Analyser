import pprint
from utils import *

def main():

    API_KEY = get_api_key()

    playlist_url = input("Enter playlist URL: ")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    playlist = get_playlist(playlist_url, youtube)

    playlist_length = playlist['pageInfo']['totalResults']

    print(playlist_length)


main()