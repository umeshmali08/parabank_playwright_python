from faker import Faker
from uuid import uuid4
from time import time_ns
from config.config import DEFAULT_PASSWORD

fake = Faker()


def create_customer() -> dict:

    # Alphanumeric + time + random component
    unique_id = f"{str(time_ns())[-8:]}{uuid4().hex[:4]}"

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "street": fake.street_address(),
        "city": fake.city(),
        "state": "CA",
        "zip_code": fake.postcode(),
        "phone": fake.msisdn()[:10],
        "ssn": fake.numerify(text="#########"),
        "username": f"qa{unique_id}",
        "password": DEFAULT_PASSWORD,
    }