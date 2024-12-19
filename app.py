from flask import Flask, request, jsonify
import json
import os
from typing import List, Dict, Union

Book = Dict[str, Union[int, str]] 
Member = Dict[str, Union[int, str]]
Books = List[Book]
Members = List[Member]

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return "Welcome to the Library Management System API!"

# Data storage files
BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"


def authenticate():
    token = request.headers.get("Authorization")
    if not token or token != "my-secret-token":
        return jsonify({"error": "Unauthorized access!"}), 401


# file read and write
def read_data(file_name: str) -> Union[Books, Members]:
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r") as file:
        return json.load(file)

def write_data(file_name: str, data: Union[Books, Members]) -> None:
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
        
@app.before_request
def check_admin_auth():
    if request.path.startswith("/admin/"):
        auth_response = authenticate()
        if auth_response:
            return auth_response


# Admin operations
@app.route("/admin/books", methods=["GET"])
def get_books():
    books = read_data(BOOKS_FILE)
    page = int(request.args.get("page", 1))  
    limit = int(request.args.get("limit", 10))
    result = paginate(books, page, limit)
    return jsonify(result)

@app.route("/admin/books", methods=["POST"])
def add_book() -> Dict[str, str]:
    book = request.json
    books = read_data(BOOKS_FILE)
    books.append(book)
    write_data(BOOKS_FILE, books)
    return jsonify({"message": "Book added successfully!"}), 201

@app.route("/admin/books/<int:book_id>", methods=["PUT"])
def update_book(book_id: int) -> Dict[str, str]:
    books = read_data(BOOKS_FILE)
    for book in books:
        if book["id"] == book_id:
            book.update(request.json)
            write_data(BOOKS_FILE, books)
            return jsonify({"message": "Book updated successfully!"})
    return jsonify({"error": "Book not found!"}), 404

@app.route("/admin/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int) -> Dict[str, str]:
    books = read_data(BOOKS_FILE)
    books = [book for book in books if book["id"] != book_id]
    write_data(BOOKS_FILE, books)
    return jsonify({"message": "Book deleted successfully!"})

@app.route("/admin/members", methods=["GET"])
def get_members() -> Members:
    members = read_data(MEMBERS_FILE)
    page = int(request.args.get("page", 1))  
    limit = int(request.args.get("limit", 10))
    result = paginate(members, page, limit)
    return jsonify(result)

@app.route("/admin/members", methods=["POST"])
def add_member() -> Dict[str, str]:
    member = request.json
    members = read_data(MEMBERS_FILE)
    members.append(member)
    write_data(MEMBERS_FILE, members)
    return jsonify({"message": "Member added successfully!"}), 201

@app.route("/admin/members/<int:member_id>", methods=["PUT"])
def update_member(member_id: int) -> Dict[str, str]:
    members = read_data(MEMBERS_FILE)
    for member in members:
        if member["id"] == member_id:
            member.update(request.json)
            write_data(MEMBERS_FILE, members)
            return jsonify({"message": "Member updated successfully!"})
    return jsonify({"error": "Member not found!"}), 404

@app.route("/admin/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id: int) -> Dict[str, str]:
    members = read_data(MEMBERS_FILE)
    members = [member for member in members if member["id"] != member_id]
    write_data(MEMBERS_FILE, members)
    return jsonify({"message": "Member deleted successfully!"})

# User operations
@app.route("/user/books", methods=["GET"])
def list_books() -> Books:
    books = read_data(BOOKS_FILE)
    page = int(request.args.get("page", 1))  
    limit = int(request.args.get("limit", 10))
    result = paginate(books, page, limit)
    return jsonify(result)

@app.route("/user/books/search", methods=["GET"])
def search_books() -> Books:
    query = request.args.get("q", "").lower()
    books = read_data(BOOKS_FILE)
    filtered_books = [book for book in books if query in book.get("title", "").lower() or query in book.get("author", "").lower()]
    return jsonify(filtered_books)

@app.route("/user/members/<int:member_id>", methods=["GET"])
def get_member_info(member_id: int) -> Union[Member, Dict[str, str]]:
    members = read_data(MEMBERS_FILE)
    for member in members:
        if member["id"] == member_id:
            return jsonify(member)
    return jsonify({"error": "Member not found!"}), 404

def paginate(data, page=1, limit=10):
    start = (page - 1) * limit
    end = start + limit
    paginated_data = data[start:end]
    return {
        "data": paginated_data,
        "meta": {
            "page": page,
            "limit": limit,
            "total_items": len(data),
            "total_pages": (len(data) + limit - 1) // limit,
        },
    }


if __name__ == "__main__":
    app.run(debug=True)
