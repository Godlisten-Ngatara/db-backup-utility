import sqlite3
import subprocess
import sys
from pathlib import Path


def test_sqlite_backup_end_to_end_from_cli(tmp_path):
    source_db = tmp_path / "source.db"
    backup_dir = tmp_path / "backups"

    conn = sqlite3.connect(source_db)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany("INSERT INTO users (name) VALUES (?)", [("alice",), ("bob",)])
    conn.commit()
    conn.close()

    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parents[1] / "cli.py"),
        "backup",
        "--db-type",
        "sqlite",
        "--name",
        "demo",
        "--db-path",
        str(source_db),
        "--backup-dir",
        str(backup_dir),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))

    assert proc.returncode == 0, proc.stderr
    assert backup_dir.exists()
    created_backup = list(backup_dir.glob("demo_sqlite.dump"))
    assert len(created_backup) == 1

    backup_path = created_backup[0]
    assert backup_path.stat().st_size > 0
    assert "[OK]" in proc.stdout
