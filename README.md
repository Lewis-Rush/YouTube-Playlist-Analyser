# YouTube Playlist Analyser

This is a command line tool that uses the Google api to get information about a given YouTube playlist, such as the total playlist runtime or the average runtime of a video. You can also enter the amount of videos you've watched and get the time remaining on the playlist

## Instructions
### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/Lewis-Rush/YouTube-Playlist-Analyser.git YouTube-Playlist-Analyser
  ```
2. Navigate to the project folder:
  ```bash
  cd YouTube-Playlist-Analyser
  ```
3. Create venv:
  ```bash
  make env-setup
  ```
4. Activate venv:
  ```bash
  source venv/bin/activate
  ```
5. Export Google API key
  ```bash
  make api-setup
  ```
  Enter API key when prompted

### Usage
1. Activate venv
  ```bash
  source venv/bin/activate
  ```

2. Run the program
  ```bash
  make run-analyser
  ```

3. Enter playlist URL when prompted

4. Enter the number of videos watched when prompted

## Tests
-Venv must be active
1. Run tests
  ```bash
  make run-tests
  ```

## Author
- [@lewis-rush](https://www.github.com/lewis-rush)