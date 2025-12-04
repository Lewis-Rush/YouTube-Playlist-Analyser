import pytest
from unittest.mock import Mock
from googleapiclient.errors import HttpError
from src.utils import get_api_key, extract_playlist_id, get_playlist

class TestGetApiKey:
    '''
    Class to test the get_api_key function
    '''
    def test_get_api_key_returns_string(self):
        '''
        Testing the return of get_api_key is a string
        '''
        api_key = get_api_key()

        assert type(api_key) == str

    def test_returns_expected_api_key(self, monkeypatch):
        '''
        Testing that get_api_key returns the api key we expect
        '''
        monkeypatch.setenv("API_KEY", "test-value")

        api_key = get_api_key()

        expected_key = "test-value"

        assert api_key == expected_key

    def test_no_api_key_raises_exception(self, monkeypatch):
        '''
        Testing that get_api_key raises an exception when no key is found
        '''
        monkeypatch.delenv("API_KEY", raising=False)

        with pytest.raises(Exception) as excinfo:
            get_api_key()

        assert "No api key found" in str(excinfo.value)

class TestExtractPlaylistID:
    '''
    Class to test the extract_playlist_id function
    '''
    def test_extract_playlist_id_returns_string(self):
        '''
        Testing that extract_playlist_id returns a string when a valid
        url is given
        '''
        url = "https://www.youtube.com/list=test"

        result = extract_playlist_id(url)

        assert type(result) == str

    def test_invalid_url_returns_error(self):
        '''
        Testing that giving extract_playlist_id an invalid url returns the
        expected error
        '''
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
        '''
        Testing that giving extract_playlist_id a non-playlist YouTube link
        returns the expected error
        '''

        url1 = "https://youtube.com/invalid"
        url2 = "https://youtu.be/invalid"

        with pytest.raises(Exception) as excinfo1:
            extract_playlist_id(url1)

        with pytest.raises(Exception) as excinfo2:
            extract_playlist_id(url2)

        assert "URL not a playlist" in str(excinfo1.value)
        assert "URL not a playlist" in str(excinfo2.value)

    def test_playlist_id_extracted(self):
        '''
        Testing that extract_playlist_id extracts the expected playlist ID
        '''
        url1 = "https://youtube.com/list=playlist-id"
        url2 = "https://youtu.be/list=playlist-id"

        result1 = extract_playlist_id(url1)
        result2 = extract_playlist_id(url2)

        assert result1 == "playlist-id"
        assert result2 == "playlist-id"

    def test_only_playlist_id_extracted(self):
        '''
        Testing that extract_playlist_id extracts only the playlist ID
        and nothing that comes afterwards
        '''
        url1 = "https://youtube.com/list=playlist-id&not-the-id"
        url2 = "https://youtu.be/list=playlist-id&not-the-id"

        result1 = extract_playlist_id(url1)
        result2 = extract_playlist_id(url2)

        assert result1 == "playlist-id"
        assert result2 == "playlist-id"

class TestGetPlaylist:
    '''
    Class to test the get_playlist function
    '''
    def test_HTTP_error_raised(self):
        '''
        Testing that when a HTTP error is returned get_playlist raises the correct
        error
        '''
        url = "https://youtube.com/list=playlist-id&not-the-id"

        mock_youtube = Mock()
        mock_request = mock_youtube.playlistItems().list.return_value
        
        mock_request.execute.side_effect = HttpError(
            resp=Mock(status=400),
            content=b"Test"
        )

        with pytest.raises(Exception) as excinfo:
            get_playlist(url, mock_youtube)

        assert "Error getting playlist" in str(excinfo.value)

    def test_expected_playlist_returned(self):
        '''
        Testing that get_playlist returns the expected playlist
        '''
        url = "https://youtube.com/list=playlist-id&not-the-id"

        mock_youtube = Mock()
        mock_request = mock_youtube.playlistItems().list.return_value

        expected = {"items" : [{"Video1" : "Test"}, {"Video2" : "Test"}]}

        mock_request.execute.return_value = expected

        result = get_playlist(url, mock_youtube)

        assert result == expected