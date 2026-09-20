from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BackupResult:
    path: Path
    db_type: str
    db_version: str
    size_bytes: int


class DBAdapter(ABC):
    """Common interface every database-specific adapter must implement."""

    def __init__(self, **connection_params):
        self.conn = connection_params

    @abstractmethod
    def test_connection(self) -> bool:
        """Return True if the DB is reachable with current params."""

    @abstractmethod
    def backup(self, dest_path: Path) -> BackupResult:
        """Dump the database to dest_path and return metadata about it."""

    @abstractmethod
    def restore(self, source_path: Path) -> None:
        """Restore the database from a previously created backup file."""

    @abstractmethod
    def detect_version(self) -> str:
        """Return the DB engine version string, for the manifest."""