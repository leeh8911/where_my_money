from where_my_money import summarize_spending


def test_summarize_spending():
    assert summarize_spending([1200, 300.5, 499.5]) == 2000.0
