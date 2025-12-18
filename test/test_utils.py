import pytest
import datetime
from unittest.mock import Mock, patch
from googleapiclient.errors import HttpError
from src.utils import (
    get_api_key,
    extract_playlist_id,
    get_playlist,
    get_videos,
    get_playlist_runtime,
    convert_times,
    get_average_video_runtime,
    no_videos_watched,
    has_watched_videos,
)


class TestGetApiKey:
    """
    Class to test the get_api_key function
    """

    def test_get_api_key_returns_string(self):
        """
        Testing the return of get_api_key is a string
        """
        api_key = get_api_key()

        assert type(api_key) == str

    def test_returns_expected_api_key(self, monkeypatch):
        """
        Testing that get_api_key returns the api key we expect
        """
        monkeypatch.setenv("API_KEY", "test-value")

        api_key = get_api_key()

        expected_key = "test-value"

        assert api_key == expected_key

    def test_no_api_key_raises_exception(self, monkeypatch):
        """
        Testing that get_api_key raises an exception when no key is found
        """
        monkeypatch.delenv("API_KEY", raising=False)

        with pytest.raises(Exception) as excinfo:
            get_api_key()

        assert "No api key found" in str(excinfo.value)


class TestExtractPlaylistID:
    """
    Class to test the extract_playlist_id function
    """

    def test_extract_playlist_id_returns_string(self):
        """
        Testing that extract_playlist_id returns a string when a valid
        url is given
        """
        url = "https://www.youtube.com/list=test"

        result = extract_playlist_id(url)

        assert type(result) == str

    def test_invalid_url_returns_error(self):
        """
        Testing that giving extract_playlist_id an invalid url returns the
        expected error
        """
        url1 = "https://not-a-valid_url.com"
        url2 = "invalid_string"
        url3 = "https://yooutuube.com"

        with pytest.raises(Exception) as excinfo1:
            extract_playlist_id(url1)

        with pytest.raises(Exception) as excinfo2:
            extract_playlist_id(url2)

        with pytest.raises(Exception) as excinfo3:
            extract_playlist_id(url3)

        assert "Invalid URL" in str(excinfo1.value)
        assert "Invalid URL" in str(excinfo2.value)
        assert "Invalid URL" in str(excinfo3.value)

    def test_non_playlist_url_returns_error(self):
        """
        Testing that giving extract_playlist_id a non-playlist YouTube link
        returns the expected error
        """

        url1 = "https://youtube.com/invalid"
        url2 = "https://youtu.be/invalid"

        with pytest.raises(Exception) as excinfo1:
            extract_playlist_id(url1)

        with pytest.raises(Exception) as excinfo2:
            extract_playlist_id(url2)

        assert "URL not a playlist" in str(excinfo1.value)
        assert "URL not a playlist" in str(excinfo2.value)

    def test_playlist_id_extracted(self):
        """
        Testing that extract_playlist_id extracts the expected playlist ID
        """
        url1 = "https://youtube.com/list=playlist-id"
        url2 = "https://youtu.be/list=playlist-id"

        result1 = extract_playlist_id(url1)
        result2 = extract_playlist_id(url2)

        assert result1 == "playlist-id"
        assert result2 == "playlist-id"

    def test_only_playlist_id_extracted(self):
        """
        Testing that extract_playlist_id extracts only the playlist ID
        and nothing that comes afterwards
        """
        url1 = "https://youtube.com/list=playlist-id&not-the-id"
        url2 = "https://youtu.be/list=playlist-id&not-the-id"

        result1 = extract_playlist_id(url1)
        result2 = extract_playlist_id(url2)

        assert result1 == "playlist-id"
        assert result2 == "playlist-id"


class TestGetPlaylist:
    """
    Class to test the get_playlist function
    """

    def test_HTTP_error_raised(self):
        """
        Testing that when a HTTP error is returned get_playlist raises the correct
        error
        """
        url = "https://youtube.com/list=playlist-id&not-the-id"

        mock_youtube = Mock()
        mock_request = mock_youtube.playlistItems().list.return_value

        mock_request.execute.side_effect = HttpError(
            resp=Mock(status=400), content=b"Test"
        )

        with pytest.raises(Exception) as excinfo:
            get_playlist(url, mock_youtube)

        assert "Error getting playlist" in str(excinfo.value)

    def test_expected_playlist_returned(self):
        """
        Testing that get_playlist returns the expected playlist
        """
        url = "https://youtube.com/list=playlist-id&not-the-id"

        mock_youtube = Mock()
        mock_request = mock_youtube.playlistItems().list.return_value

        expected = {"items": [{"Video1": "Test"}, {"Video2": "Test"}]}

        mock_request.execute.return_value = expected

        result = get_playlist(url, mock_youtube)

        assert result == expected


class TestGetVideos:
    """
    Class to test the get_videos function
    """

    def test_request_called_correctly(self):
        """
        Testing that the request is called properly
        """
        mock_youtube = Mock()
        mock_videos = mock_youtube.videos.return_value
        mock_list = mock_videos.list.return_value

        video_ids = ["Test1", "Test2"]

        result = get_videos(video_ids, mock_youtube)

        mock_videos.list.assert_called_once_with(part="contentDetails", id=video_ids)

        assert result == mock_list


class TestConvertTimes:
    """
    Class to test the convert_times function
    """

    def test_convert_times_returns_list(self):
        """
        Testing that the convert_times function returns a list
        """
        times = ["PT1H1M1S", "PT1H1M", "PT1S"]

        result = convert_times(times)

        assert type(result) == list

    def test_convert_times_returns_int_list(self):
        """
        Testing that the convert_times function returns a list of ints
        """
        times = ["PT1H1M1S", "PT1H1M", "PT1S"]

        result = convert_times(times)

        for time in result:
            assert type(time) == int

    def test_time_converted_correctly(self):
        """
        Testing that convert_times converts each time as expected
        """
        times = ["PT1H1M1S", "PT1H1M", "PT1S", "PT4H15S", "PT250M10S"]

        result = convert_times(times)

        expected = [3661, 3660, 1, 14415, 15010]

        assert result == expected


class TestGetPlaylistRuntime:
    """
    Class to test the get_playlist_runtime function
    """

    def test_get_playlist_runtime_returns_int(self):
        """
        Testing that the get_playlist_runtime function returns an int
        """
        pass


class TestGetAverageVideoRuntime:
    """
    Class to test the get_average_video_runtime function
    """

    def test_get_average_video_runtime_string(self):
        """
        Testing that the get_average_video_runtime function returns a string
        """
        runtime = 600
        video_count = 10

        result = get_average_video_runtime(runtime, video_count)

        assert type(result) == str

    def test_get_average_video_runtime_returns_expected(self):
        """
        Testing that the get_average_video_runtime function returns the expected result
        """
        runtime1 = 600
        runtime2 = 300

        video_count1 = 10
        video_count2 = 20

        result1 = get_average_video_runtime(runtime1, video_count1)
        result2 = get_average_video_runtime(runtime2, video_count2)

        expected1 = "0:01:00"
        expected2 = "0:00:15"

        assert result1 == expected1
        assert result2 == expected2


class TestNoVideosWatched:
    """
    Class to test the no_videos_watched function
    """

    def test_no_videos_watched_prints_correctly(self, capsys):
        """
        Testing that the no_videos_watched function prints the expected values
        """
        mock_youtube = Mock()
        mock_playlist = {"items": []}
        mock_playlist_runtime = 1000
        mock_average_runtime = 100
        playlist_length = 10

        with patch(
            "src.utils.get_playlist_runtime", return_value=mock_playlist_runtime
        ), patch(
            "src.utils.get_average_video_runtime", return_value=mock_average_runtime
        ):

            no_videos_watched(mock_playlist, playlist_length, mock_youtube)

        captured = capsys.readouterr()
        output = captured.out

        expected_runtime_str = str(datetime.timedelta(seconds=mock_playlist_runtime))

        assert "No videos watched" in output
        assert f"Total playlist runtime:  {expected_runtime_str}" in output
        assert f"Average video runtime:  {mock_average_runtime}" in output
        assert f"Playlist length:  {playlist_length}" in output


class TestHasWatchedVideos:
    """
    Class to test the has_watched_videos function
    """

    def test_has_watched_videos_prints_correctly(self, capsys):
        """
        Testing that the no_videos_watched function prints the expected values
        """
        mock_youtube = Mock()
        mock_playlist = {"items": [1, 2, 3, 4, 5]}
        mock_playlist_runtime = 900
        mock_average_runtime = 90
        videos_watched = 1
        playlist_length = 5

        with patch(
            "src.utils.get_playlist_runtime", return_value=mock_playlist_runtime
        ), patch(
            "src.utils.get_average_video_runtime", return_value=mock_average_runtime
        ):

            has_watched_videos(
                mock_playlist, playlist_length, mock_youtube, videos_watched
            )

        captured = capsys.readouterr()
        output = captured.out

        expected_runtime_str = str(datetime.timedelta(seconds=mock_playlist_runtime))

        assert f"Playlist time left:  {expected_runtime_str}" in output
        assert f"Average runtime of videos left:  {mock_average_runtime}" in output
        assert f"Videos left:  {playlist_length - videos_watched}" in output
