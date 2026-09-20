import sqlite3
from pathlib import Path

from .base import BackupResult, DBAdapter


class SQLiteAdapter(DBAdapter):
    """conn expects: path (path to the source .db file)"""

    def test_connection(self) -> bool:
        return Path(self.conn["path"]).exists()

    def detect_version(self) -> str:
        return sqlite3.sqlite_version

    def backup(self, dest_path: Path) -> BackupResult:
        # sqlite3's backup API is online-safe (handles concurrent writers),
        # unlike a raw file copy which can grab a half-written page.
        src = sqlite3.connect(self.conn["path"])
        dst = sqlite3.connect(dest_path)
        with dst:
            src.backup(dst)
        src.close()
        dst.close()
        return BackupResult(
            path=dest_path,
            db_type="sqlite",
            db_version=self.detect_version(),
            size_bytes=dest_path.stat().st_size,
        )

    def restore(self, source_path: Path) -> None:
        src = sqlite3.connect(source_path)
        dst = sqlite3.connect(self.conn["path"])
        with dst:
            src.backup(dst)
        src.close()
        dst.close()