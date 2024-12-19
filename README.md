# Library Management System API

A Flask-based REST API for managing a library, allowing CRUD operations for books and members. The API also includes features like pagination, search functionality, and token-based authentication for admin routes.

---

## Features

1. **CRUD Operations**:

   - Admins can create, read, update, and delete books and members.
   - Users can view books and member details.

2. **Pagination**:

   - Supports paginated responses for both books and members.

3. **Search**:

   - Users can search for books by title or author.

4. **Token-Based Authentication**:

   - Admin routes are secured and require a token to access.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install Flask
   ```

---

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Access the API at `http://127.0.0.1:5000/`.

---

## API Endpoints

### **Admin Endpoints**

All admin endpoints require a valid token in the `Authorization` header.

#### Books

- `GET /admin/books`: Get paginated list of books.
- `POST /admin/books`: Add a new book.
- `PUT /admin/books/<book_id>`: Update an existing book.
- `DELETE /admin/books/<book_id>`: Delete a book.

#### Members

- `GET /admin/members`: Get paginated list of members.
- `POST /admin/members`: Add a new member.
- `PUT /admin/members/<member_id>`: Update a member's details.
- `DELETE /admin/members/<member_id>`: Remove a member.

#### Headers

```json
{
  "Authorization": "my-secret-token"
}
```

### **User Endpoints**

#### Books

- `GET /user/books`: Get paginated list of books.
- `GET /user/books/search?q=<query>`: Search for books by title or author.

#### Members

- `GET /user/members/<member_id>`: Get details of a specific member.

---

## Assumptions and Limitations

1. **Authentication**:

   - Admin token is hardcoded as `"my-secret-token"`.

2. **Data Persistence**:

   - Data is stored in JSON files (`books.json`, `members.json`).

3. **No Third-Party Libraries**:

   - To adhere to constraints, only Flask is used (no external libraries).

4. **Pagination**:

   - Default `page=1` and `limit=10` for paginated endpoints.

---

## Testing

Automated tests are implemented using `unittest`.

1. Run the test suite:

   ```bash
   python -m unittest test_library_api.py
   ```

2. Test coverage:

   - Fetching books and members with pagination.
   - Adding, updating, and deleting books/members.
   - Authentication for admin routes.
   - Searching for books.

---

## Design Choices

1. **Separation of Admin and User Routes**:

   - Admin routes (`/admin/`) are secured and provide CRUD operations.
   - User routes (`/user/`) are read-only.

2. **Pagination**:

   - Simplifies responses for large datasets and improves performance.

3. **JSON Storage**:

   - Simplified storage solution for the sake of this project.

4. **Modular Code**:

   - Helper functions for reading/writing data and pagination.

---

## Future Improvements

1. **Database Integration**:

   - Replace JSON storage with a relational database (e.g., SQLite, PostgreSQL).

2. **Enhanced Authentication**:

   - Implement user roles and dynamic tokens.

3. **Error Handling**:

   - Improve response messages for edge cases and invalid inputs.

4. **Deployment**:

   - Deploy the application using a cloud platform (e.g., AWS, Heroku).

---

## Author

**Your Name**\
[Jay262422](https://github.com/jay262422)\
Email: [jay.p7@ahduni.edu.in](mailto\:jay.p7@ahduni.edu.in)



