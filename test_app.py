from unittest.mock import patch, Mock
from app import app

@patch('infra.client.get')
def test_app(mock_get):
    mock_get.return_value.text = 'response'
    mock_response1 = Mock()
    mock_response1.text = 'urlTitle":"my-fake-url'
    mock_response2 = Mock()
    mock_response2.text = "dou content"
    mock_get.side_effect = [mock_response1, mock_response2]
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

