import pytest
from api.parabank_api import ParaBankAPI


@pytest.mark.api
def test_parabank_openapi_is_available(api_context):
    api = ParaBankAPI(api_context)
    document = api.get_openapi()
    assert document["info"]["title"] == "The ParaBank REST API"
    assert "/cleanDB" in document["paths"]
