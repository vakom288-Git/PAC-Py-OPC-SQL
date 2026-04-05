# === НАСТРОЙКИ ПОДКЛЮЧЕНИЯ ===
OPC_URL = "opc.tcp://192.168.2.215:4880"
OPC_USER = "admin"
OPC_PASS = "admin"
OPC_CONN_NODEID = "sys.opc.connection"

import os as _os  # noqa: E402

# SQL Server connection parameters for mssql-python (TDS driver).
# Credentials can be overridden via environment variables DB_USER / DB_PASSWORD.
# For Windows/Kerberos integrated auth leave user/password empty and set
# trusted_connection="yes".
DB_CONFIG = {
    "server": "192.168.1.72",
    "port": 1433,
    "database": "DB_NEW_TEST",
    "user": _os.environ.get("DB_USER", ""),           # e.g. "sa"
    "password": _os.environ.get("DB_PASSWORD", ""),   # set DB_PASSWORD env var
    "trusted_connection": "yes",                      # Windows/Kerberos auth
    "trust_server_certificate": "yes",
    # "encrypt": "yes",                               # uncomment to force TLS
}

# === СПИСКИ ТЕГОВ ===
EVENT_TAGS = [
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_1",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_2",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_3",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_4",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_5",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_6",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_7",
    "ns=1;s=Data_Conf.Dev1.DO1332-1 (32ch DO).DO_3_8",
]

ANALOG_TAGS = [
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI_5_1",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_2",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_3",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_4",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_5",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_6",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_7",
    "ns=1;s=Data_Conf.Dev1.AI1316-5 (8ch TC).AI-5_8"
]

# === НАСТРОЙКИ ПЕРИОДИЧНОСТИ И БУФЕРИЗАЦИИ ===
ANALOG_SAVE_INTERVAL = 10      # секунд - как часто снимать срез аналогов
DB_BATCH_SIZE = 500            # максимум записей в одном batch INSERT
JSON_BUFFER_MAX_MB = 500       # максимальный размер буфера в МБ
JSON_BUFFER_MAX_RECORDS = 10000 # максимум записей в одном JSON файле