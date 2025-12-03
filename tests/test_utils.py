import pytest
from src.utils import get_api_key

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

