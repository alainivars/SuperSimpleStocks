from main import add_some_trade_record


def test_add_some_trade_record():
    assert len(add_some_trade_record()) == 10
