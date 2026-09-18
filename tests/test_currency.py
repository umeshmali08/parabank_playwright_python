from utils.currency import currency_to_cents, amount_to_cents


def test_currency_parser():
    assert currency_to_cents("$150.00") == 15000
    assert currency_to_cents("$25.50") == 2550
    assert currency_to_cents("$8.99") == 899
    assert amount_to_cents(150 + 25.50 + 8.99) == 18449
