import json

import httpx
import pytest
from respx import MockRouter

from backend.factories.inquest import InQuestVerdict, InQuestVerdictFactory


def test_inquest_verdict(inquest_dfi_details_response: str):
    sha256 = "e86c5988a3a6640fb90b90b9e9200e4cce0669594dbb5422622946208c124149"
    dict_ = json.loads(inquest_dfi_details_response)

    verdict = InQuestVerdict.build(dict_)
    assert verdict.sha256 == sha256
    assert verdict.malicious is True
    assert verdict.reference_link == f"https://labs.inquest.net/dfi/sha256/{sha256}"


@pytest.mark.asyncio
async def test_inquest(inquest_dfi_details_response: str, respx_mock: MockRouter):
    sha256 = "e86c5988a3a6640fb90b90b9e9200e4cce0669594dbb5422622946208c124149"
    respx_mock.get(
        f"https://labs.inquest.net/api/dfi/details?sha256={sha256}",
    ).mock(
        return_value=httpx.Response(200, content=inquest_dfi_details_response),
    )

    verdict = await InQuestVerdictFactory.from_sha256s([sha256])
    assert verdict.malicious is True
