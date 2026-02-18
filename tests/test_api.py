from fastapi.testclient import TestClient

from where_my_money.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_spend_today_shape_and_total_positive():
    r = client.get('/spend/today')
    assert r.status_code == 200
    body = r.json()
    assert 'total' in body
    assert body['total'] > 0
    assert isinstance(body['by_card'], list)
    assert isinstance(body['by_category'], list)


def test_cancelled_transaction_is_netted_out():
    r = client.get('/spend/today')
    body = r.json()
    # tx3(1550) cancelled by tx5(3000) -> net 0 for tx3 in today's spend
    # So 교통 카테고리는 집계에서 제외되거나 0이어야 함
    transport = [x for x in body['by_category'] if x['category'] == '교통']
    assert transport == [] or transport[0]['amount'] == 0


def test_installment_transaction_is_monthly_prorated_in_billing():
    r = client.get('/billing/upcoming')
    assert r.status_code == 200
    item = next(x for x in r.json()['items'] if x['card_id'] == 'card_kb')
    # tx4 = 120000 / 3개월 => 40000이 이번달 반영되어야 함
    assert item['expected_amount'] >= 40000


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


def test_create_and_soft_delete_card():
    create = client.post('/cards', json={
        'card_id': 'card_lotte',
        'issuer': 'Lotte',
        'alias': '쇼핑카드',
        'billing_day': 20,
    })
    assert create.status_code == 200

    delete = client.delete('/cards/card_lotte')
    assert delete.status_code == 200
    assert delete.json()['is_active'] is False


def test_sync_transactions_inserts_new_rows():
    r = client.post('/sync/transactions')
    assert r.status_code == 200
    body = r.json()
    assert body['inserted'] >= 1


def test_alert_preview_endpoint():
    r = client.get('/alerts/preview')
    assert r.status_code == 200
    body = r.json()
    assert 'alerts' in body
