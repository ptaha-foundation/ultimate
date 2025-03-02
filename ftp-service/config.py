import os

from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    FTP_HOST: str
    FTP_PORT: int
    DJANGO_AUTH_URL: str
    DJANGO_UPLOAD_URL: str
    TIMEOUT: int
    DTP_READ_LIMIT: int
    DTP_WRITE_LIMIT: int
    MAX_CONNECTIONS: int
    MAX_CONNECTIONS_PER_IP: int
    LOG_FILE: str

    @classmethod
    def load(cls):
        load_dotenv()
        
        config = cls(
            FTP_HOST=os.getenv('FTP_HOST', '0.0.0.0'),
            FTP_PORT=int(os.getenv('FTP_PORT', 2121)),
            DJANGO_AUTH_URL=os.getenv('DJANGO_AUTH_URL', ''),
            DJANGO_UPLOAD_URL=os.getenv('DJANGO_UPLOAD_URL', ''),
            TIMEOUT=int(os.getenv('REQUEST_TIMEOUT', 10)),
            DTP_READ_LIMIT=int(os.getenv('DTP_READ_LIMIT', 1024 * 1024)),
            DTP_WRITE_LIMIT=int(os.getenv('DTP_WRITE_LIMIT', 1024 * 1024)),
            MAX_CONNECTIONS=int(os.getenv('MAX_CONNECTIONS', 100)),
            MAX_CONNECTIONS_PER_IP=int(os.getenv('MAX_CONNECTIONS_PER_IP', 5)),
            LOG_FILE=os.getenv('LOG_FILE', 'logs/ftp_service.log'),
        )

        if not all([config.DJANGO_AUTH_URL, config.DJANGO_UPLOAD_URL]):
            raise ValueError("Missing required environment variables")
            
        return config


EXPECTED_HEADERS = [
    'lot_date',
    'ksss_nb_code',
    'ksss_fuel_code',
    'initial_volume',
    'available_volume',
    'status',
    'lot_price',
    'price_per_ton'
]
