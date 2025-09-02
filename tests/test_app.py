from unittest.mock import patch
from app import create_app

@patch('service.create_report.create_report')
def test_app(mock_create_report):
    mock_create_report.return_value = "mocked report"
    app = create_app()
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b"mocked report"

