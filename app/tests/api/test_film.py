
def test_get_film(auth_client,mock_film_service):

    result = auth_client.get("/api/v1/films/1")
    assert result.status_code == 200, result.json()