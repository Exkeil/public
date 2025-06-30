from dishka import Provider, Scope, provide
import os
from call_center_downloader.domains.call_center.repositories.call_center import CallCenterRepository
from call_center_downloader.domains.call_center.services.call_center import CallCenterService
from call_center_downloader.infrastructure.adapters.call_center_api import CallCenterApiAdapter
from call_center_downloader.infrastructure.storage.csv_storage import CSVStorage

class MainProvider(Provider):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    @provide(scope=Scope.APP)
    def get_api_adapter(self) -> CallCenterApiAdapter:
        from yarl import URL
        return CallCenterApiAdapter(
            base_url=URL(os.getenv("APP_API_BASE_URL")),
            username=os.getenv("APP_API_USERNAME"),
            password=os.getenv("APP_API_PASSWORD"),
            domain_id=int(os.getenv("APP_API_DOMAIN_ID")),
        )

    @provide(scope=Scope.APP)
    def get_storage(self) -> CSVStorage:
        return CSVStorage(output_dir=self.parser.storage_output_dir)

    @provide(scope=Scope.APP)
    def get_call_center_repository(self, api: CallCenterApiAdapter) -> CallCenterRepository:
        return CallCenterRepository(api=api)

    @provide(scope=Scope.APP)
    def get_call_center_service(self, repository: CallCenterRepository, storage: CSVStorage) -> CallCenterService:
        return CallCenterService(repository=repository, storage=storage)