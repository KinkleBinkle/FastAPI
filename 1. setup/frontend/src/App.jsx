import { useEffect, useState } from "react";

function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTitle, setNewTitle] = useState("");
  const [newAuthor, setNewAuthor] = useState("");
  const [error, setError] = useState("");
  const [searchAuthor, setSearchAuthor] = useState("");
  const [bookId, setBookId] = useState("");
  const [selectedBook, setSelectedBook] = useState(null);

  // For editing
  const [editId, setEditId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editAuthor, setEditAuthor] = useState("");

  // Fetch all books on load
  useEffect(() => {
    fetchBooks();
  }, []);

  // GET /books
  const fetchBooks = (author = "") => {
    setLoading(true);
    let url = "http://127.0.0.1:8000/books";
    if (author) {
      url += `?author=${author}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setBooks(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching books:", err);
        setLoading(false);
      });
  };

  // GET /books/{id}
  const fetchBookById = () => {
    if (!bookId.trim()) {
      setError("Enter a valid book ID");
      return;
    }

    fetch(`http://127.0.0.1:8000/books/${bookId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Book not found");
        }
        return res.json();
      })
      .then((data) => {
        setSelectedBook(data);
        setError("");
      })
      .catch((err) => {
        console.error("Error fetching book:", err);
        setError("Could not fetch book");
      });
  };

  // POST /books
  const handleAddBook = (e) => {
    e.preventDefault();

    if (!newTitle.trim() || !newAuthor.trim()) {
      setError("Both title and author are required");
      return;
    }

    fetch("http://127.0.0.1:8000/books", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: newTitle, author: newAuthor }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to add book");
        }
        return res.json();
      })
      .then((book) => {
        setBooks([...books, book]);
        setNewTitle("");
        setNewAuthor("");
        setError("");
      })
      .catch((err) => {
        console.error("Error adding book:", err);
        setError("Could not add book");
      });
  };

  // PUT /books/{id}
  const handleUpdateBook = (e) => {
    e.preventDefault();

    if (!editTitle.trim() || !editAuthor.trim()) {
      setError("Both title and author are required for update");
      return;
    }

    fetch(`http://127.0.0.1:8000/books/${editId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: editTitle, author: editAuthor }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to update book");
        }
        return res.json();
      })
      .then((updatedBook) => {
        setBooks(books.map((b) => (b.id === updatedBook.id ? updatedBook : b)));
        setEditId(null);
        setEditTitle("");
        setEditAuthor("");
        setError("");
      })
      .catch((err) => {
        console.error("Error updating book:", err);
        setError("Could not update book");
      });
  };

  // DELETE /books/{id}
  const handleDeleteBook = (id) => {
    if (!window.confirm("Are you sure you want to delete this book?")) return;

    fetch(`http://127.0.0.1:8000/books/${id}`, {
      method: "DELETE",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to delete book");
        }
        setBooks(books.filter((b) => b.id !== id));
      })
      .catch((err) => {
        console.error("Error deleting book:", err);
        setError("Could not delete book");
      });
  };

  if (loading) {
    return <p style={{ textAlign: "center" }}>Loading...</p>;
  }

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>📚 Book Manager</h1>

      {/* Add Book Form */}
      <form onSubmit={handleAddBook} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter book title"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <input
          type="text"
          placeholder="Enter author name"
          value={newAuthor}
          onChange={(e) => setNewAuthor(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <button type="submit" style={{ padding: "8px 16px" }}>
          Add Book
        </button>
      </form>

      {/* Filter by author */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search by author"
          value={searchAuthor}
          onChange={(e) => setSearchAuthor(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <button
          onClick={() => fetchBooks(searchAuthor)}
          style={{ padding: "8px 16px" }}
        >
          Search
        </button>
        <button
          onClick={() => {
            setSearchAuthor("");
            fetchBooks();
          }}
          style={{ padding: "8px 16px", marginLeft: "8px" }}
        >
          Reset
        </button>
      </div>

      {/* Fetch book by ID */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="number"
          placeholder="Enter book ID"
          value={bookId}
          onChange={(e) => setBookId(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <button onClick={fetchBookById} style={{ padding: "8px 16px" }}>
          Get Book
        </button>
      </div>

      {selectedBook && (
        <div style={{ marginBottom: "20px", color: "blue" }}>
          <h3>Book Found:</h3>
          <p>
            <strong>ID:</strong> {selectedBook.id} — <strong>Title:</strong>{" "}
            {selectedBook.title} — <strong>Author:</strong>{" "}
            {selectedBook.author}
          </p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Book List */}
      {books.length === 0 ? (
        <p>No books found.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {books.map((b) => (
            <li key={b.id} style={{ marginBottom: "10px" }}>
              <strong>ID:</strong> {b.id} — <strong>Title:</strong> {b.title} —{" "}
              <strong>Author:</strong> {b.author}
              <button
                style={{ marginLeft: "10px" }}
                onClick={() => {
                  setEditId(b.id);
                  setEditTitle(b.title);
                  setEditAuthor(b.author);
                }}
              >
                Edit
              </button>
              <button
                style={{ marginLeft: "10px", color: "red" }}
                onClick={() => handleDeleteBook(b.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Edit Form */}
      {editId && (
        <form onSubmit={handleUpdateBook} style={{ marginTop: "20px" }}>
          <h3>Update Book (ID: {editId})</h3>
          <input
            type="text"
            placeholder="Edit title"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            style={{ padding: "8px", marginRight: "8px" }}
          />
          <input
            type="text"
            placeholder="Edit author"
            value={editAuthor}
            onChange={(e) => setEditAuthor(e.target.value)}
            style={{ padding: "8px", marginRight: "8px" }}
          />
          <button type="submit" style={{ padding: "8px 16px" }}>
            Save
          </button>
          <button
            type="button"
            onClick={() => setEditId(null)}
            style={{ padding: "8px 16px", marginLeft: "8px" }}
          >
            Cancel
          </button>
        </form>
      )}
    </div>
  );
}

export default App;
