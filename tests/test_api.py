from unittest.mock import Mock, patch

from app.api import get_fruit_data


@patch("app.api.requests.get")
def test_get_fruit_data(mock_get):

    mock_response = Mock()

    mock_response.json.return_value = {
        "name": "banana",
        "nutritions": {
            "calories": 96,
            "sugar": 17.2,
        },
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_fruit_data("banana")

    assert result["name"] == "banana"

    mock_get.assert_called_once()