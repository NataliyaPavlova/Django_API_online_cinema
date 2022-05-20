import os

from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'postgres': {
        'dbname': os.environ.get('DB_NAME_PSTGR'),
        'user': os.environ.get('DB_USER_PSTGR'),
        'password': os.environ.get('DB_PASSWORD_PSTGR'),
        'host': os.environ.get('DB_HOST_PSTGR', '127.0.0.1'),
        'port': os.environ.get('DB_PORT_PSTGR', 5432),
        },
    'sqlite': {
        'dbname': os.environ.get('DB_NAME_SQLITE'),
    }

}
