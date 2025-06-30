import os
from dotenv import load_dotenv
from settings import API, DB_URL, OBJECTS

# Загружаем переменные окружения
load_dotenv()

# API настройки
API = {
    'url': os.getenv('API_BASE_URL', 'https://lk-al.cprt.su/api/'),
    'user': os.getenv('API_USERNAME', 'admin@callcenter-al.cprt.su'),
    'pass': os.getenv('API_PASSWORD', 'RNEvCAkt'),
    'domain': int(os.getenv('DOMAIN_ID', '2'))
}

# База данных
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/api_data')

# Объекты для выгрузки (True - системный, False - доменный)
OBJECTS = {
    "PbxHost": True,
    "GSSystem": True,
    "GSPluginCore": True,
    "GSPluginCDR": True,
    "GSDefaults": True,
    "ModCallCenter": True,
    "DomainCDR": False,
    "DomainQueue": False,
    "DomainUser": False,
}

# Output Configuration
OUTPUT_DIR = "data"

# API Objects Configuration
OBJECTS_TO_EXPORT = {
    "PbxHost": True,
    "GSSystem": True,
    "GSPluginCore": True,
    "GSPluginCDR": True,
    "GSDefaults": True,
    "ModCallCenter": True,
    "ModEventSocket": True,
    "ModXmlCdr": True,
    "DomainCDR": False,
    "DomainDialPlan": False,
    "DomainQueueCDR": False,
    "DomainGateway": False
}

# API Objects Configuration
OBJECTS = {
    "PbxHost": {"system": True},
    "GSSystem": {"system": True},
    "GSPluginCore": {"system": True},
    "GSPluginCDR": {"system": True},
    "GSDefaults": {"system": True},
    "ModCallCenter": {"system": True},
    "ModEventSocket": {"system": True},
    "ModXmlCdr": {"system": True},
    "DomainCDR": {"system": False},
    "DomainDialPlan": {"system": False},
    "DomainDialerBatch": {"system": False},
    "DomainDialerContact": {"system": False},
    "DomainDialerAttempt": {"system": False},
    "DomainQueue": {"system": False},
    "DomainQueueCDR": {"system": False},
    "DomainConference": {"system": False},
    "DomainConferenceCdr": {"system": False},
    "DomainUser": {"system": False},
    "DomainGateway": {"system": False},
    "DomainSofiaProfile": {"system": False},
    "DomainDPEResult": {"system": False},
    "DomainNotify": {"system": False},
    "DomainVoiceMail": {"system": False}
} 