from fastapi.testclient import TestClient

from where_my_money.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_spend_today_shape():
    r = client.get('/spend/today')
    assert r.status_code == 200
    body = r.json()
    assert 'total' in body
    assert isinstance(body['by_card'], list)
    assert isinstance(body['by_category'], list)


def test_cards_alias_update():
    r = client.patch('/cards/card_hyundai/alias', json={'alias': '테스트카드'})
    assert r.status_code == 200
    assert r.json()['alias'] == '테스트카드'


def test_cards_alias_update_missing_alias_error():
    r = client.patch('/cards/card_hyundai/alias', json={})
    assert r.status_code == 400
    body = r.json()
    assert body['error']['code'] == 'http_400'


def test_unknown_card_returns_not_found_error():
    r = client.patch('/cards/not_exists/active', json={'is_active': True})
    assert r.status_code == 404
    body = r.json()
    assert body['error']['code'] == 'not_found'


def test_billing_upcoming_has_items():
    r = client.get('/billing/upcoming')
    assert r.status_code == 200
    body = r.json()
    assert 'items' in body
    assert len(body['items']) >= 1
