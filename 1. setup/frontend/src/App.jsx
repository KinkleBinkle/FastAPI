import { useEffect, useState } from "react";

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState("");
  const [error, setError] = useState("");

  // Fetch students on page load
  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = () => {
    fetch("http://127.0.0.1:8000/students")
      .then((res) => res.json())
      .then((data) => {
        setStudents(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching students:", err);
        setLoading(false);
      });
  };

  const handleAddStudent = (e) => {
    e.preventDefault();

    if (!newName.trim()) {
      setError("Name is required");
      return;
    }

    fetch("http://127.0.0.1:8000/students", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: newName }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to add student");
        }
        return res.json();
      })
      .then((student) => {
        setStudents([...students, student]); // add to list
        setNewName(""); // clear input
        setError(""); // clear error
      })
      .catch((err) => {
        console.error("Error adding student:", err);
        setError("Could not add student");
      });
  };

  if (loading) {
    return <p style={{ textAlign: "center" }}>Loading...</p>;
  }

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Student List</h1>

      {/* Add Student Form */}
      <form onSubmit={handleAddStudent} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter student name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <button type="submit" style={{ padding: "8px 16px" }}>
          Add Student
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Student List */}
      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {students.map((s) => (
            <li key={s.id}>
              <strong>ID:</strong> {s.id} — <strong>Name:</strong> {s.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;