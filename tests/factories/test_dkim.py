import pytest

from backend import factories


@pytest.fixture
def factory():
    return factories.DKIMVerdictFactory()


@pytest.mark.asyncio
async def test_dkim_valid(dkim_valid_eml: bytes, factory: factories.DKIMVerdictFactory):
    verdict = await factory.call(
        eml_file=dkim_valid_eml, eml=factories.EmlFactory().call(dkim_valid_eml)
    )
    assert verdict
    assert verdict.name == "DKIM"
    assert len(verdict.details) > 0


@pytest.mark.asyncio
async def test_dkim_invalid(
    dkim_invalid_eml: bytes, factory: factories.DKIMVerdictFactory
):
    verdict = await factory.call(
        eml_file=dkim_invalid_eml, eml=factories.EmlFactory().call(dkim_invalid_eml)
    )
    assert verdict
    assert verdict.name == "DKIM"
    assert verdict.malicious
    assert len(verdict.details) > 0


@pytest.mark.asyncio
async def test_dkim_no_signature(
    dkim_no_signature_eml: bytes, factory: factories.DKIMVerdictFactory
):
    verdict = await factory.call(
        eml_file=dkim_no_signature_eml,
        eml=factories.EmlFactory().call(dkim_no_signature_eml),
    )
    assert verdict is None
