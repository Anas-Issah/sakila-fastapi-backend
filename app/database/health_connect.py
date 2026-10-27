import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg


load_dotenv(Path.cwd().parent/"app"/".env")

url = os.getenv("DB_HEALTH_CHECK_URL")

if not url:
    print("this wont work")


def get_db():

    return psycopg.connect(url)

