
export DATABASE_URL=mysql+pymysql://kirill:kirill@127.0.0.1/social_network?charset=utf8mb4
alembic revision --autogenerate -m "Added required tables"
alembic downgrade base
alembic upgrade head