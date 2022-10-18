import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path.cwd() / '.env')

HOST = os.environ.get("HOST")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DATABASE = os.environ.get("DATABASE")
TABLE_NAME = "expenses"
ERROR_PAGE = "Error_page.html"
REDIRECT_PAGE = "index"
