from pathlib import Path

from .base import BackupResult, DBAdapter
from ..utils.shell import run, ShellError


class PostgresAdapter(DBAdapter):
    """conn expects: host, port, user, password, dbname"""

    def _dsn(self) -> str:
        c = self.conn
        return (
            f"postgresql://{c['user']}:{c['password']}@"
            f"{c['host']}:{c.get('port', 5432)}/{c['dbname']}"
        )

    def test_connection(self) -> bool:
        try:
            run(["pg_isready", "-d", self._dsn()])
            return True
        except ShellError:
            return False

    def detect_version(self) -> str:
        out = run(["psql", self._dsn(), "-t", "-c", "SHOW server_version;"])
        return out.strip()

    def backup(self, dest_path: Path) -> BackupResult:
        # -Fc = custom format: compressed, supports selective restore
        run(["pg_dump", "-Fc", self._dsn(), "-f", str(dest_path)])
        return BackupResult(
            path=dest_path,
            db_type="postgres",
            db_version=self.detect_version(),
            size_bytes=dest_path.stat().st_size,
        )

    def restore(self, source_path: Path) -> None:
        run(["pg_restore", "--clean", "--if-exists", "-d", self._dsn(), str(source_path)])