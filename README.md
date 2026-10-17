# Chess Competition Platform 

Note: This is an application written in 2024 from scratch with zero use of Artificial Intelligence.

The application has been extracted from the original notebook into connected Python modules. The notebook remains as the original reference; run the Python launcher to use the refactored application.

## Run

Use Python 3 with Tkinter installed. No third-party Python packages are required.

```sh
python3 main.py
```

Open the admin menu with:

```sh
python3 main.py admin
```

The admin menu supports generating a competition, entering results, and advancing rounds. Generating a competition replaces the current year's bracket, so use it only when enrollment is ready. At least two players must be enrolled.

The existing admin password remains the default. You can override it with the `CHESS_ADMIN_PASSWORD` environment variable.

## Files and dependencies

| File | Responsibility | Imports from this project |
| --- | --- | --- |
| `main.py` | Command-line launcher and admin menu | `gui`, `admin` |
| `gui.py` | Main user window | `registration`, `bracket`, `storage` |
| `registration.py` | School/player registration and enrollment | `storage`, `config` |
| `bracket.py` | Competition chart window | `storage` |
| `admin.py` | Generate matches, record results, advance rounds | `storage`, `config` |
| `storage.py` | Database queries, ID counters, bracket text files | `config` |
| `config.py` | Shared settings and paths | None |

Data paths are relative to `config.py`, so launching from another working directory still uses this project's data. Keep the database (`chess.db`) and text data files (`id.txt`, `array.txt`, and `competitorlist.txt`) together in the `data/` folder. The existing database and text files are reused without migration.

Importing modules does not launch the application. The root user window owns the Tkinter event loop; registration and chart windows receive their parent explicitly.

## Validation

All modules were parsed and imported successfully. A four-player tournament was generated, advanced, and completed against temporary files and a temporary database, including creation of the next year's competition table. The GUI was not manually exercised.
