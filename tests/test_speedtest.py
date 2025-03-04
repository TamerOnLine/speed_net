import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import create_database, save_results, get_last_results



import unittest
import sqlite3
from src.main import create_database, save_results, get_last_results


class TestSpeedTestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Setup test database before each test."""
        self.test_db = "test_speed_results.db"
        
        # إنشاء قاعدة بيانات الاختبار
        conn = sqlite3.connect(self.test_db)
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

    def tearDown(self):
        """Cleanup database after each test."""
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_create_database(self):
        """Test if database is created successfully."""
        create_database()
        conn = sqlite3.connect("speed_results.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='speed_test_results'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result, "Database table was not created!")

    def test_save_results(self):
        """Test if results are saved correctly in the database."""
        save_results(100, 50, 20)  # حفظ بيانات اختبار وهمية
        
        conn = sqlite3.connect("speed_results.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM speed_test_results ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result, "Failed to save data to the database!")
        self.assertEqual(result[1], 100, "Download speed value mismatch!")
        self.assertEqual(result[2], 50, "Upload speed value mismatch!")
        self.assertEqual(result[3], 20, "Ping value mismatch!")

    def test_get_last_results(self):
        """Test retrieving last saved results."""
        save_results(120, 60, 30)
        save_results(130, 70, 40)

        results = get_last_results(2)
        
        self.assertEqual(len(results), 2, "Expected 2 results, but got a different number!")
        self.assertEqual(results[0][1], 130, "First result download speed mismatch!")
        self.assertEqual(results[1][1], 120, "Second result download speed mismatch!")

if __name__ == "__main__":
    unittest.main()
