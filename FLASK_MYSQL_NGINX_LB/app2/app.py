from flask import Flask, render_template_string
import mysql.connector
import os
import time
import socket

app = Flask(__name__)

# Wait for MySQL
while True:
    try:
        db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "db"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", "password"),
            database=os.environ.get("MYSQL_DATABASE", "mydb")
        )
        cursor = db.cursor()
        # Ensure table exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            app_name VARCHAR(50),
            visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        db.commit()
        print("Connected to MySQL and table ready!")
        break
    except mysql.connector.Error as err:
        print(f"MySQL not ready yet: {err}")
        time.sleep(3)

@app.route("/")
def home():
    app_name = "App 2"
    cursor = db.cursor()
    cursor.execute("INSERT INTO visits (app_name) VALUES (%s)", (app_name,))
    db.commit()
    cursor.execute("SELECT COUNT(*) FROM visits WHERE app_name=%s", (app_name,))
    count = cursor.fetchone()[0]
    hostname = socket.gethostname()

    html = f"""
    <h1>{app_name}</h1>
    <p>Total Visits: {count}</p>
    <p>Container Hostname: {hostname}</p>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
