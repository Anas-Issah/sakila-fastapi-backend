
def test_get_customer(auth_client, mock_customer_service):

    response = auth_client.get("/api/v1/customers/1")
    assert response.status_code == 200

    customer = response.json()
    assert customer["customer_id"] == 1