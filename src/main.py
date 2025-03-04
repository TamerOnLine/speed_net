import speedtest
import sqlite3
from datetime import datetime


def create_database():
    """Create the SQLite database and results table if not exists."""
    conn = sqlite3.connect("speed_results.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS speed_test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            download_speed INTEGER,
            upload_speed INTEGER,
            ping INTEGER,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def save_results(download_speed, upload_speed, ping):
    """Save the speed test results into the database with rounded values."""
    conn = sqlite3.connect("speed_results.db")
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # تقريب القيم إلى أقرب عدد صحيح
    download_speed = round(download_speed)
    upload_speed = round(upload_speed)
    ping = round(ping)

    cursor.execute('''
        INSERT INTO speed_test_results (download_speed, upload_speed, ping, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (download_speed, upload_speed, ping, timestamp))
    
    conn.commit()
    conn.close()


def get_last_results(limit=5):
    """Retrieve the last N speed test results from the database."""
    conn = sqlite3.connect("speed_results.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM speed_test_results
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def test_internet_speed():
    """Run a speed test and display/store the results."""
    st = speedtest.Speedtest()
    
    print("Selecting the best server...")
    st.get_best_server()
    
    print("Measuring download speed...")
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    
    print("Measuring upload speed...")
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    
    ping = st.results.ping  # Get ping value

    # تقريب القيم قبل العرض والتخزين
    download_speed_rounded = round(download_speed)
    upload_speed_rounded = round(upload_speed)
    ping_rounded = round(ping)

    # Display results
    print("\nInternet Speed Test Results:")
    print(f"Download Speed: {download_speed_rounded} Mbps")
    print(f"Upload Speed: {upload_speed_rounded} Mbps")
    print(f"Ping: {ping_rounded} ms")

    # Save to database
    save_results(download_speed, upload_speed, ping)
    print("\nResults saved to the database.")


if __name__ == "__main__":
    create_database()
    test_internet_speed()
    
    # Display last 5 results
    print("\nLast 5 Speed Test Results:")
    for row in get_last_results():
        print(f"ID: {row[0]}, Download: {row[1]} Mbps, Upload: {row[2]} Mbps, Ping: {row[3]} ms, Time: {row[4]}")
