from utils import *

API_KEY = get_api_key()

youtube = build("youtube", "v3", developerKey=API_KEY)

playlist = get_playlist("PLW-ubDuosu7UKDXI6KF7XIMdzaStaVEIL", youtube)

print(playlist)