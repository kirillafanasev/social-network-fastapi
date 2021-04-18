import databases
from config import settings

database = databases.Database(settings.DATABASE_URL)
