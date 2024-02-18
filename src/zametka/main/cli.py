import alembic.config
import sys

from zametka.notes.infrastructure.db.alembic.config import (
    ALEMBIC_CONFIG as NOTES_ALEMBIC,
)
from zametka.access_service.infrastructure.persistence.alembic.config import (
    ALEMBIC_CONFIG as ACCESS_SERVICE_ALEMBIC,
)


def notes_alembic_handler(args: list[str]) -> None:
    alembic.config.main(  # type:ignore
        argv=["-c", NOTES_ALEMBIC, *args],
    )


def access_service_alembic_handler(args: list[str]) -> None:
    alembic.config.main(  # type:ignore
        argv=["-c", ACCESS_SERVICE_ALEMBIC, *args],
    )


def main() -> None:
    print(">> zametka CLI <<")

    argv = sys.argv[1:]
    module = argv[0]
    option = argv[1]
    args = argv[2:]

    modules = {
        "notes": {
            "alembic": notes_alembic_handler,
        },
        "access_service": {
            "alembic": access_service_alembic_handler,
        },
    }

    if module not in modules:
        print("No such module.")
        return None

    if option not in modules[module]:
        print("No such option.")
        return None

    modules[module][option](args)
