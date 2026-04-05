# PAC-Py-OPC-SQL

OPC UA → SQL Server bridge that subscribes to OPC tags and writes data into
`dbo.OpcEvents` and `dbo.OpcAnalog` tables.

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** `mssql-python` ships a self-contained TDS driver — no ODBC driver
> installation is required on the host.

## Configuration

All settings live in `opc_tags_list.py`.

### OPC UA connection

```python
OPC_URL  = "opc.tcp://<host>:<port>"
OPC_USER = "<username>"
OPC_PASS = "<password>"
```

### SQL Server connection (`DB_CONFIG`)

`DB_CONFIG` is a plain dict in `opc_tags_list.py`:

```python
DB_CONFIG = {
    "server":                 "192.168.1.72",
    "port":                   1433,
    "database":               "DB_NEW_TEST",
    "user":                   "",          # empty → Windows/Kerberos auth
    "password":               "",          # see env-var section below
    "trusted_connection":     "yes",       # Windows integrated auth
    "trust_server_certificate": "yes",
    # "encrypt": "yes",                    # uncomment to force TLS
}
```

#### SQL Server Login (UID/PWD) instead of Windows auth

1. Set `trusted_connection` to `""` (empty string) in `DB_CONFIG`.
2. Provide credentials via environment variables — **never hard-code secrets**:

   ```bash
   export DB_USER=sa
   export DB_PASSWORD=YourStrongPassword
   ```

   The application reads them automatically:

   ```python
   "user":     os.environ.get("DB_USER", ""),
   "password": os.environ.get("DB_PASSWORD", ""),
   ```

## T-SQL and User-Defined Functions

Because `db_mssql.execute()` / `db_mssql.executemany()` accept arbitrary T-SQL,
you can call any UDF that already exists in the target database:

```python
import db_mssql

# Scalar UDF in a SELECT
rows = db_mssql.execute("SELECT dbo.MyUdf(?)", ("input_value",))

# UDF inside an INSERT
db_mssql.execute(
    "INSERT INTO dbo.OpcEvents (NodeId, [Value], [Timestamp], QualityIsGood, QualityStatus) "
    "VALUES (?, dbo.NormaliseValue(?), GETDATE(), ?, ?)",
    ("ns=1;s=MyTag", 3.14, 1, "Good")
)
```

## Database Schema (DDL)

```sql
CREATE TABLE dbo.OpcEvents (
    Id            INT IDENTITY PRIMARY KEY,
    NodeId        NVARCHAR(256)  NOT NULL,
    [Value]       NVARCHAR(MAX)  NULL,
    [Timestamp]   DATETIME       NOT NULL DEFAULT GETDATE(),
    QualityIsGood BIT            NOT NULL,
    QualityStatus NVARCHAR(128)  NOT NULL
);

CREATE TABLE dbo.OpcAnalog (
    Id            INT IDENTITY PRIMARY KEY,
    NodeId        NVARCHAR(256)  NOT NULL,
    [Value]       FLOAT          NULL,
    [Timestamp]   DATETIME       NOT NULL DEFAULT GETDATE(),
    QualityIsGood BIT            NOT NULL,
    QualityStatus NVARCHAR(128)  NOT NULL
);
```

## Architecture

```
OPC UA Server
    │
    ▼  (asyncua subscription)
SubscriptionHandler  ──► event_queue / analog_queue
                              │
                         db_writer()  ──► db_mssql.executemany()  ──► SQL Server
                              │                  ▲
                    (on DB error)           (reconnect)
                              │
                         JSONBufferManager  (./buffer/*.json)
                              │
                    sync_buffer_to_db()  ──► db_mssql  ──► SQL Server
```

- All blocking DB calls run in a `ThreadPoolExecutor` so the asyncio event loop
  is never blocked.
- `db_mssql.DBConnection` provides automatic commit/rollback as a context manager.
