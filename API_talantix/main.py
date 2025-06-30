from typing import List, Optional
import requests
from datetime import datetime
from sqlalchemy.orm import Session

from models import APIRequest, APIResponse, APIRecord
from database import init_db, Session as DBSession
from config import API, OBJECTS
from logger import setup_logger

logger = setup_logger()

# Настройка базы данных
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ApiData(Base):
    __tablename__ = "api_data"
    id = Column(Integer, primary_key=True)
    object_type = Column(String, index=True)
    external_id = Column(String, index=True)
    data = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_system = Column(Boolean)

class APIClient:
    """Клиент для работы с API"""
    
    def __init__(self):
        self.base_url: str = API['url']
        self.token: Optional[str] = None
        self.headers: dict = {"Content-Type": "application/json"}
        
        # Отключаем предупреждения для незащищенного соединения
        requests.packages.urllib3.disable_warnings()
    
    def authenticate(self) -> bool:
        request = APIRequest(
            action="auth",
            obj="User",
            action_id="auth_request",
            params={"login": API['user'], "password": API['pass']}
        )
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=request.to_dict(),
            verify=False
        )
        api_response = APIResponse.from_dict(response.json())
        
        if api_response.code == 200:
            self.token = api_response.body['token']
            self.headers["Authorization"] = f"Bearer {self.token}"
            logger.info("Успешная аутентификация")
            return True
            
        logger.error(f"Ошибка аутентификации: {api_response.message}")
        return False

    def fetch_data(self, obj_name: str, is_system: bool) -> List[APIRecord]:
        if not self.token:
            logger.error("Отсутствует токен авторизации")
            return []

        all_data: List[APIRecord] = []
        offset = 0
        limit = 100

        while True:
            request = APIRequest(
                action="list",
                obj=obj_name,
                action_id=f"list_{obj_name.lower()}",
                params={} if is_system else {"domain_id": API['domain']},
                limit=limit,
                offset=offset
            )

            if "CDR" in obj_name:
                request.filter_ = {
                    "field_list": [{"field": "dt", "condition_type": 5, "value": 0}],
                    "type": 0
                }

            response = requests.post(
                self.base_url,
                json=request.to_dict(),
                headers=self.headers,
                verify=False
            )
            
            if response.status_code != 200:
                logger.error(f"Ошибка получения данных: {response.text}")
                break

            data = response.json()
            records = data.get("list", [])
            
            if not records:
                break

            api_records = [
                APIRecord.from_raw_data(record, obj_name, is_system)
                for record in records
            ]
            
            all_data.extend(api_records)
            logger.info(f"Получено {len(records)} записей типа {obj_name}")

            if len(records) < limit:
                break
                
            offset += limit

        return all_data

def save_to_db(session: Session, records: List[APIRecord]) -> None:
    if not records:
        return
        
    for record in records:
        db_item = ApiData(
            object_type=record.object_type,
            external_id=record.id,
            data=record.data,
            created_at=record.created_at,
            updated_at=record.updated_at,
            is_system=record.is_system
        )
        session.add(db_item)
        
    session.commit()
    logger.info(f"Сохранено {len(records)} записей типа {records[0].object_type}")

def main() -> None:
    logger.info("Начало выгрузки данных")
    
    init_db()
    client = APIClient()

    if not client.authenticate():
        logger.error("Выгрузка остановлена из-за ошибки аутентификации")
        return

    session = DBSession()
    
    for obj_name, is_system in OBJECTS.items():
        logger.info(f"Обработка объекта {obj_name}")
        records = client.fetch_data(obj_name, is_system)
        save_to_db(session, records)
        
    logger.info("Выгрузка успешно завершена")
    session.close()

if __name__ == "__main__":
    main() 