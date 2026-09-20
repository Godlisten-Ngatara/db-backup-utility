from pathlib import Path

from ..adapters.init import get_adapter


class BackupEngine:
    def __init__(self, backup_dir: Path):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def run(self, db_type: str, name: str, **conn_params):
        adapter = get_adapter(db_type, **conn_params)

        if not adapter.test_connection():
            raise ConnectionError(f"Cannot reach {db_type} with given params")

        dest = self.backup_dir / f"{name}_{db_type}.dump"
        result = adapter.backup(dest)

        print(f"[OK] {result.db_type} v{result.db_version} "
              f"-> {result.path} ({result.size_bytes} bytes)")
        return result


if __name__ == "__main__":
    # Demo: same engine, same call shape, different adapters underneath.
    engine = BackupEngine(backup_dir="./backups")

    engine.run(
        "sqlite",
        name="demo",
        path="./example.db",
    )

    # Same pattern would apply to the others, just swap db_type + params:
    # engine.run("postgres", name="demo", host="localhost", user="postgres",
    #            password="secret", dbname="mydb")
    # engine.run("mysql", name="demo", host="localhost", user="root",
    #            password="secret", dbname="mydb")
    # engine.run("mongodb", name="demo", uri="mongodb://localhost:27017",
    #            dbname="mydb")