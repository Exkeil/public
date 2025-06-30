import pytest

from bitrix_downloader.args import Parser
from bitrix_downloader.domains.bitrix.repositories.bitrix import IBitrixRepository
from bitrix_downloader.domains.bitrix.services.bitrix import BitrixService
from bitrix_downloader.infrastructure.adapters.bitrix import BitrixClient


@pytest.fixture
def bitrix_service(
    parser: Parser,
    bitrix_client: BitrixClient,
    bitrix_repository: IBitrixRepository,
) -> BitrixService:
    return BitrixService(
        bitrix_repository=bitrix_repository,
        bitrix_client=bitrix_client,
        sng_entity_id=parser.bitrix.sng_entity_id,
        world_entity_id=parser.bitrix.world_entity_id,
        mass_recruitment_entity_id=parser.bitrix.mass_recruitment_entity_id,
        call_center_entity_id=parser.bitrix.call_center_entity_id,
        chunk_size=parser.bitrix.chunk_size,
    )
