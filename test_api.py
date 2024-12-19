import unittest
import json
from app import app, BOOKS_FILE, MEMBERS_FILE  # Import your Flask app and files
import os

class LibraryAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup temporary test data."""
        cls.test_books = [
            {"id": 1, "title": "Test Book 1", "author": "Author 1", "genre": "Fiction", "published_year": 2020},
            {"id": 2, "title": "Test Book 2", "author": "Author 2", "genre": "Non-Fiction", "published_year": 2021},
        ]
        cls.test_members = [
            {"id": 1, "name": "Member 1", "email": "member1@example.com"},
            {"id": 2, "name": "Member 2", "email": "member2@example.com"},
        ]
        
        # Write test data to temporary JSON files
        with open(BOOKS_FILE, "w") as books_file:
            json.dump(cls.test_books, books_file)
        with open(MEMBERS_FILE, "w") as members_file:
            json.dump(cls.test_members, members_file)

        app.testing = True
        cls.client = app.test_client()  # Flask test client

    @classmethod
    def tearDownClass(cls):
        """Clean up test data."""
        os.remove(BOOKS_FILE)
        os.remove(MEMBERS_FILE)

    def test_get_books(self):
        """Test fetching books with pagination."""
        response = self.client.get("/user/books?page=1&limit=1")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 1)  # Should return one book
        #response = self.client.get("/user/books")
        #print(response.get_json())
        self.assertEqual(data["meta"]["total_items"], 3)
        self.assertEqual(data["meta"]["total_pages"], 3)

    def test_add_book(self):
        """Test adding a new book (admin)."""
        new_book = {
            "id": 3,
            "title": "New Test Book",
            "author": "New Author",
            "genre": "Science",
            "published_year": 2022,
        }
        headers = {"Authorization": "my-secret-token"}
        response = self.client.post("/admin/books", json=new_book, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["message"], "Book added successfully!")

        # Verify book was added
        response = self.client.get("/user/books")
        data = response.get_json()
        self.assertEqual(len(data["data"]), 3)

    def test_unauthorized_access(self):
        """Test accessing admin routes without a token."""
        response = self.client.post("/admin/books", json={})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["error"], "Unauthorized access!")

    def test_search_books(self):
        """Test searching for books."""
        response = self.client.get("/user/books/search?q=Test Book 1")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Book 1")

if __name__ == "__main__":
    unittest.main()
