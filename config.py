import os
from dotenv import load_dotenv

load_dotenv()

# OBS
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_SENHA = os.getenv("OBS_SENHA", "")
OBS_TIMEOUT = int(os.getenv("OBS_TIMEOUT", 3))

# Liturgia
URL_LITURGIA = "https://liturgia.cancaonova.com/pb/"

REQUEST_TIMEOUT = 10

# Animated Lower Thirds
QUANTIDADE_MAXIMA_PAINEIS = 4
QUANTIDADE_MAXIMA_DE_SLOTS = 10

PAINEL_TITULO = 1
PAINEL_LEITURAS = 2