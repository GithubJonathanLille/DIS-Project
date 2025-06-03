# 🧠 Full Setup Guide: Flask + PostgreSQL Movie Recommendation App

A simple Flask web application to search for and discover movies based on various criteria.

## Prerequisites

*   Python 3.8+ and pip
*   PostgreSQL (installed and running)

## Setup Instructions

This guide walks you through setting up and running your app from scratch.


1.  **👨‍🦯‍➡️👨‍🦯 Clone or 📥 Download the Repository:**
    Get the project files onto your local machine.

    ```bash
    git clone https://github.com/Sofus-Holm/What-To-Watch
    ```

2. **📲 Navigate to Project Directory:**
    ```bash
    cd path/to/what_to_watch
    ```

3. **🧱 Create Database**
    ```bash
    createdb What_to_watch_db
    ```

4. **🧾 Import Schema**
    ```bash
    psql What_to_watch_db < db_schema.sql
    ```

5. **⚙️ Create and Activate Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate      # Mac/Linux
    venv\Scripts\activate       # Windows
    ```

6. **📦 Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

7. **📊 Populate Database**
    ```bash
    python populate_db.py
    ```

8. **🚀 Run the App**
    ```bash
    python run.py
    ```

Then open your browser and visit:
    ```bash
    http://127.0.0.1:5000/
    ```

# You're now ready to use the app!




---
## Extra: 🗑️ To delete Database
```bash
dropdb What_to_watch_db
```
---
