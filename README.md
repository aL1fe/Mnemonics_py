Creat .env.prod or .env.dev config files with following structure:
TELEGRAM_API_TOKEN="your_telegram_api_token"
For PostgresQL:
DB_USER="postgres"
DB_PASS="password"
DB_HOST="127.0.0.1" 
DB_PORT="5432"
DB_NAME="phrases_and_words"

For MS SQL:
TELEGRAM_API_TOKEN="your_telegram_api_token"
DB_USER="sa"
DB_PASS="password"
DB_HOST="localhost" 
DB_PORT="1433"
DB_NAME="phrases_and_words"
Setup database from scratch

Launch command:
alembic revision --autogenerate -m "init"
alembic upgrade head
alembic history

