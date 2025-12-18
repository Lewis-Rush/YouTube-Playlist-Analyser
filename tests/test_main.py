from src.main import main
from unittest.mock import Mock, patch


class TestMain:
    """
    Class to test the main function
    """

    def test_main_gets_api_key(self, monkeypatch):
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: "0" if "videos watched" in prompt else "https://test.com",
        )

        mock_api_key = "test_key"
        monkeypatch.setattr("src.main.get_api_key", lambda: mock_api_key)

        with patch("src.main.get_playlist") as mock_get_playlist, patch(
            "src.main.no_videos_watched"
        ) as mock_no_videos, patch(
            "src.main.has_watched_videos"
        ) as mock_has_watched, patch(
            "src.main.build"
        ) as mock_build:

            mock_get_playlist.return_value = {"pageInfo": {"totalResults": 10}}

            main()

            mock_build.assert_called_once_with(
                "youtube", "v3", developerKey=mock_api_key
            )

    def test_main_gets_user_input_correctly(self, monkeypatch):
        """
        Testing that the main function correctly gets the user's input for both the
        playlist_url and videos watched
        """
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: "0" if "videos watched" in prompt else "https://test.com",
        )

        mock_api_key = "test_key"
        monkeypatch.setattr("src.main.get_api_key", lambda: mock_api_key)

        with patch("src.main.get_playlist") as mock_get_playlist, patch(
            "src.main.no_videos_watched"
        ) as mock_no_videos, patch(
            "src.main.has_watched_videos"
        ) as mock_has_watched, patch(
            "src.main.build"
        ) as mock_build:

            mock_youtube_client = Mock()
            mock_build.return_value = mock_youtube_client

            mock_get_playlist.return_value = {"pageInfo": {"totalResults": 10}}

            main()

        mock_build.assert_called_once_with("youtube", "v3", developerKey=mock_api_key)

        mock_get_playlist.assert_called_once_with(
            "https://test.com", mock_youtube_client
        )

    def test_has_watched_videos_isnt_called(self, monkeypatch):
        """
        Testing that has_watched_videos isnt called and has_watched is called
        when the user has watched videos
        """
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: "0" if "videos watched" in prompt else "https://test.com",
        )

        mock_api_key = "test_key"
        monkeypatch.setattr("src.main.get_api_key", lambda: mock_api_key)

        with patch("src.main.get_playlist") as mock_get_playlist, patch(
            "src.main.no_videos_watched"
        ) as mock_no_videos, patch(
            "src.main.has_watched_videos"
        ) as mock_has_watched, patch(
            "src.main.build"
        ) as mock_build:

            mock_youtube_client = Mock()
            mock_build.return_value = mock_youtube_client

            mock_get_playlist.return_value = {"pageInfo": {"totalResults": 10}}

            main()

        mock_build.assert_called_once_with("youtube", "v3", developerKey=mock_api_key)

        mock_get_playlist.assert_called_once_with(
            "https://test.com", mock_youtube_client
        )

        mock_no_videos.assert_called_once_with(
            {"pageInfo": {"totalResults": 10}}, 10, mock_youtube_client
        )

        mock_has_watched.assert_not_called()

    def test_has_watched_videos_is_called(self, monkeypatch):
        """
        Testing that has_watched_videos is called and has_watched isnt called
        when the user hasnt watched videos
        """
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: "1" if "videos watched" in prompt else "https://test.com",
        )

        mock_api_key = "test_key"
        monkeypatch.setattr("src.main.get_api_key", lambda: mock_api_key)

        with patch("src.main.get_playlist") as mock_get_playlist, patch(
            "src.main.no_videos_watched"
        ) as mock_no_videos, patch(
            "src.main.has_watched_videos"
        ) as mock_has_watched, patch(
            "src.main.build"
        ) as mock_build:

            mock_youtube_client = Mock()
            mock_build.return_value = mock_youtube_client

            mock_get_playlist.return_value = {"pageInfo": {"totalResults": 10}}

            main()

        mock_build.assert_called_once_with("youtube", "v3", developerKey=mock_api_key)

        mock_get_playlist.assert_called_once_with(
            "https://test.com", mock_youtube_client
        )

        mock_has_watched.assert_called_once_with(
            {"pageInfo": {"totalResults": 10}}, 9, mock_youtube_client, 1
        )

        mock_no_videos.assert_not_called()
