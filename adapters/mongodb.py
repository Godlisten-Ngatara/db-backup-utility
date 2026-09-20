from pathlib import Path

from .base import BackupResult, DBAdapter
from ..utils.shell import run, ShellError


class MongoDBAdapter(DBAdapter):
    """conn expects: uri (full mongodb:// connection string), dbname"""

    def test_connection(self) -> bool:
        try:
            run(["mongosh", self.conn["uri"], "--eval", "db.runCommand({ping: 1})"])
            return True
        except ShellError:
            return False

    def detect_version(self) -> str:
        out = run(["mongosh", self.conn["uri"], "--quiet", "--eval", "db.version()"])
        return out.strip()

    def backup(self, dest_path: Path) -> BackupResult:
        run([
            "mongodump", f"--uri={self.conn['uri']}",
            f"--db={self.conn['dbname']}",
            "--archive=" + str(dest_path), "--gzip",
        ])
        return BackupResult(
            path=dest_path,
            db_type="mongodb",
            db_version=self.detect_version(),
            size_bytes=dest_path.stat().st_size,
        )

    def restore(self, source_path: Path) -> None:
        run([
            "mongorestore", f"--uri={self.conn['uri']}",
            "--archive=" + str(source_path), "--gzip", "--drop",
        ])