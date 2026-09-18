from decimal import Decimal, ROUND_HALF_UP


def currency_to_decimal(value: str) -> Decimal:
    cleaned = value.replace("$", "").replace(",", "").strip()
    return Decimal(cleaned).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def currency_to_cents(value: str) -> int:
    return int(currency_to_decimal(value) * 100)


def amount_to_cents(value) -> int:
    return int(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
