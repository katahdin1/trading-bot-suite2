# data/webull_auth.py
from webull import paper_webull
import os
from dotenv import load_dotenv

load_dotenv()

def login_webull():
    wb = paper_webull()
    wb.login(username=os.getenv("WEBULL_USERNAME"), password=os.getenv("WEBULL_PASSWORD"))
    return wb
