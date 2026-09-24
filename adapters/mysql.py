from pathlib import Path

from adapters.base import BackupResult, DBAdapter
from utils.shell import run, ShellError


class MySQLAdapter(DBAdapter):
    """conn expects: host, port, user, password, dbname"""

    def _auth_args(self) -> list[str]:
        c = self.conn
        return [
            f"-h{c['host']}", f"-P{c.get('port', 3306)}",
            f"-u{c['user']}", f"-p{c['password']}",
        ]

    def test_connection(self) -> bool:
        try:
            run(["mysqladmin", *self._auth_args(), "ping"])
            return True
        except ShellError:
            return False

    def detect_version(self) -> str:
        out = run(["mysql", *self._auth_args(), "-N", "-e", "SELECT VERSION();"])
        return out.strip()

    def backup(self, dest_path: Path) -> BackupResult:
        sql = run([
            "mysqldump", *self._auth_args(),
            "--single-transaction", "--routines", "--triggers",
            self.conn["dbname"],
        ])
        dest_path.write_text(sql)
        return BackupResult(
            path=dest_path,
            db_type="mysql",
            db_version=self.detect_version(),
            size_bytes=dest_path.stat().st_size,
        )

    def restore(self, source_path: Path) -> None:
        with open(source_path) as f:
            import subprocess
            subprocess.run(
                ["mysql", *self._auth_args(), self.conn["dbname"]],
                stdin=f, check=True,
            )