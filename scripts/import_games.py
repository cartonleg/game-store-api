import argparse
import asyncio
import sys
from pathlib import Path

from app.database.database import async_session_factory, engine
from app.database.repositories.games import GameRepository
from app.modules.admin.exceptions import CatalogReplaceError
from app.modules.admin.service import AdminService
from app.utils.csv_parser import CsvParseError


async def run(csv_path: Path, *, replace: bool) -> int:
    content = csv_path.read_text(encoding="utf-8-sig")

    async with async_session_factory() as session:
        service = AdminService(session, GameRepository(session))
        try:
            result = await service.import_games_csv(content, replace=replace)
        except CsvParseError as exc:
            print(f"CSV error: {exc}", file=sys.stderr)
            return 1
        except CatalogReplaceError as exc:
            print(f"Import error: {exc}", file=sys.stderr)
            return 1

    print(f"Imported {result.imported_count} games (replace={result.replaced_existing})")
    await engine.dispose()
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Import games from a CSV file into the database")
    parser.add_argument("csv_path", type=Path, help="Path to the CSV file (e.g. data/items.csv)")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing games before import",
    )
    args = parser.parse_args()

    if not args.csv_path.is_file():
        print(f"File not found: {args.csv_path}", file=sys.stderr)
        sys.exit(1)

    sys.exit(asyncio.run(run(args.csv_path, replace=args.replace)))


if __name__ == "__main__":
    main()
