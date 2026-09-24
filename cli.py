import argparse
from pathlib import Path

from core.engine import BackupEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Backup and restore databases")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup", help="Create a database backup")
    backup_parser.add_argument("--db-type", required=True, choices=["sqlite", "postgres", "mysql", "mongodb"])
    backup_parser.add_argument("--name", required=True)
    backup_parser.add_argument("--db-path", help="Path to the SQLite database file")
    backup_parser.add_argument("--host", default="localhost")
    backup_parser.add_argument("--port", type=int)
    backup_parser.add_argument("--user", default="")
    backup_parser.add_argument("--password", default="")
    backup_parser.add_argument("--dbname", default="")
    backup_parser.add_argument("--backup-dir", type=Path, default=Path("./backups"))

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "backup":
        if args.db_type == "sqlite":
            if not args.db_path:
                parser.error("--db-path is required for sqlite backups")
            engine = BackupEngine(args.backup_dir)
            engine.run(args.db_type, args.name, path=args.db_path)
            return 0

        if not args.dbname:
            parser.error("--dbname is required for non-sqlite backups")

        engine = BackupEngine(args.backup_dir)
        engine.run(
            args.db_type,
            args.name,
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            dbname=args.dbname,
        )
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
