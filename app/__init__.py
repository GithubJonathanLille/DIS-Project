from flask import Flask
import psycopg2
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_key_for_what_to_watch' # Change this!

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    return conn

from app import routes # Import routes after app is created