from .base import DBAdapter, BackupResult
from .postgres import PostgresAdapter
from .mysql import MySQLAdapter
from .mongodb import MongoDBAdapter
from .sqlite import SQLiteAdapter

REGISTRY: dict[str, type[DBAdapter]] = {
    "postgres": PostgresAdapter,
    "mysql": MySQLAdapter,
    "mongodb": MongoDBAdapter,
    "sqlite": SQLiteAdapter,
}


def get_adapter(db_type: str, **conn_params) -> DBAdapter:
    try:
        cls = REGISTRY[db_type]
    except KeyError:
        raise ValueError(f"Unsupported db_type '{db_type}'. Options: {list(REGISTRY)}")
    return cls(**conn_params)