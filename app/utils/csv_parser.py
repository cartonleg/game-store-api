import csv
import io
from decimal import Decimal, InvalidOperation

from app.database.models import Game, Locations


REQUIRED_COLUMNS = {"title", "description", "price", "location"}


class CsvParseError(ValueError):
    """Raised when a CSV file cannot be parsed into game rows."""


def parse_games_csv(content: str) -> list[Game]:
    if not content.strip():
        raise CsvParseError("CSV file is empty")

    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise CsvParseError("CSV file is missing a header row")

    headers = {name.strip() for name in reader.fieldnames}
    if not REQUIRED_COLUMNS.issubset(headers):
        missing = ", ".join(sorted(REQUIRED_COLUMNS - headers))
        raise CsvParseError(f"CSV is missing required columns: {missing}")

    games = []
    for line_number, row in enumerate(reader, start=2):
        try:
            location = Locations(row["location"].strip())
            price = Decimal(row["price"].strip())
            title = row["title"].strip()
            description = row["description"].strip()
        except (KeyError, ValueError, InvalidOperation) as exc:
            raise CsvParseError(f"Invalid data on line {line_number}") from exc

        if not title or not description:
            raise CsvParseError(f"Title and description are required on line {line_number}")

        games.append(
            Game(
                title=title,
                description=description,
                price=price,
                location=location,
            )
        )

    if not games:
        raise CsvParseError("CSV file contains no game rows")

    return games
