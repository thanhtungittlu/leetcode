import os
from .config import Application, MobioEnvironment

APP_TMP_DATA_DIR = os.path.join(Application.APPLICATION_DATA_DIR, 'tmp')

STATIC_DATA_DIR = os.path.join(Application.PUBLIC_DATA_DIR, 'static')

os.makedirs(STATIC_DATA_DIR, exist_ok=True)
os.makedirs(APP_TMP_DATA_DIR, exist_ok=True)

URL_STATIC = MobioEnvironment.PUBLIC_HOST
