import os
from dotenv import load_dotenv

from app import Application

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_GEO = os.getenv("API_KEY_GEO")


app = Application(API_KEY, API_KEY_GEO)

app.run()