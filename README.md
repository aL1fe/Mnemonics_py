# Mnemonics

A Telegram bot for learning English vocabulary (with Ukrainian translations) using spaced repetition. Words live in a shared dictionary (`main_dictionary`) and each user's progress is tracked with a per-word `weight` used for spaced repetition (`user_articles`).


## 1. Clone the repository

```powershell
git clone https://github.com/aL1fe/Mnemonics_py.git
cd Mnemonics_py
```

## 2. Create the environment and install dependencies

### Windows (PowerShell)

```powershell
.\setup.ps1
```

`setup.ps1` creates a `.venv` virtual environment and installs everything from [requirements.txt](requirements.txt).

### Linux / macOS

```bash
. ./setup.sh
conda activate mnemonics
```

`setup.sh` creates and activates a Conda environment named `mnemonics` (Python 3.12) and installs [requirements.txt](requirements.txt). It must be *sourced* (`. ./setup.sh`), not executed, so the environment activation persists in your current shell.

## 3. Set up PostgreSQL

Install PostgreSQL and create an empty database for the project, e.g.:

```sql
CREATE DATABASE phrases_and_words;
```

A local installation, Docker container, or any managed PostgreSQL instance will work — you only need the host, port, credentials and database name for the next step.

## 4. Configure environment variables

The app loads configuration from a `.env.{ENVIRONMENT}` file, where `ENVIRONMENT` defaults to `dev` (see [config.py](config.py)). Create `.env.dev` in the project root (use `.env.prod` and set `ENVIRONMENT=prod` for a production run):

```env
TELEGRAM_API_TOKEN="your_telegram_api_token"
DB_USER="postgres"
DB_PASS="password"
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="phrases_and_words"
```

| Variable | Description | Default |
|---|---|---|
| `TELEGRAM_API_TOKEN` | Bot token issued by BotFather | — |
| `DB_USER` | PostgreSQL user | — |
| `DB_PASS` | PostgreSQL password | — |
| `DB_HOST` | PostgreSQL host | — |
| `DB_PORT` | PostgreSQL port | — |
| `DB_NAME` | PostgreSQL database name | — |
| `WHISPER_URL` | Base URL of a speech-to-text service used for voice messages | `http://127.0.0.1:8006` |

## 5. Initialize the database schema

With the virtual environment activated and `.env.dev` configured, apply the existing migrations:

```powershell
alembic upgrade head
```

This creates the `main_dictionary`, `users` and `user_articles` tables and seeds `main_dictionary` with an initial set of English/Ukrainian word pairs (see [migrations/versions](migrations/versions)).

### Useful Alembic commands

```powershell
alembic upgrade head                          # apply all pending migrations
alembic history                               # show migration history
alembic downgrade -1                          # roll back the last migration
alembic revision --autogenerate -m "message"  # generate a new migration after model changes
```

## 6. Run the application

### Windows (PowerShell)

```powershell
.\.venv\Scripts\activate.ps1
python .\main.py
```

### Linux / macOS

```bash
conda activate mnemonics
python ./main.py
```
