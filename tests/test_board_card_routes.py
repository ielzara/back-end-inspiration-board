def test_get_board_with_no_card_records(client, one_saved_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["cards"] == []


def test_get_number_of_cards_for_board(client, multiple_boards_with_cards):
    board = multiple_boards_with_cards[0]

    # Act
    response = client.get(f"/boards/{board.id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body["cards"]) == 2
    assert response_body["title"] == "Board 1"


def test_get_all_cards_from_specific_board(client, multiple_boards_with_cards):
    board = multiple_boards_with_cards[0]

    # Act
    response = client.get(f"/boards/{board.id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body["cards"]) == 2
    assert response_body["cards"][0]["message"] == "Card 1 for Board 1"
    assert response_body["cards"][1]["message"] == "Card 2 for Board 1"


def test_create_card_for_board(client, one_saved_board):
    # Arrange
    new_card = {"message": "New card message", "likes": 0}

    # Act
    response = client.post(f"/boards/{one_saved_board.id}/cards", json=new_card)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["message"] == "New card message"
    assert response_body["likes"] == 0

def test_delete_card(client, multiple_boards_with_cards):
    board = multiple_boards_with_cards[0]
    card = board.cards[0]

    # Act
    response = client.delete(f"/cards/{card.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": f'Card {card.id} "{card.message}" successfully deleted'
    }

    # Check that the card was deleted
    response = client.get(f"/cards/{card.id}")
    assert response.status_code == 404
