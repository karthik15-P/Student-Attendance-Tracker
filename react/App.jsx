import React, { useState } from "react";

function App() {
    const [students, setStudents] = useState([
        {
            id: 1,
            rollNumber: "RA2411001",
            name: "Student One",
            attendance: 82
        },
        {
            id: 2,
            rollNumber: "RA2411002",
            name: "Student Two",
            attendance: 68
        },
        {
            id: 3,
            rollNumber: "RA2411003",
            name: "Student Three",
            attendance: 91
        }
    ]);

    const [name, setName] = useState("");
    const [rollNumber, setRollNumber] = useState("");

    const addStudent = () => {
        if (!name.trim() || !rollNumber.trim()) {
            alert("Please enter student name and roll number.");
            return;
        }

        const newStudent = {
            id: Date.now(),
            rollNumber: rollNumber,
            name: name,
            attendance: 0
        };

        setStudents([...students, newStudent]);

        setName("");
        setRollNumber("");
    };

    const deleteStudent = (id) => {
        setStudents(
            students.filter((student) => student.id !== id)
        );
    };

    const lowAttendanceCount = students.filter(
        (student) => student.attendance < 75
    ).length;

    return (
        <div style={styles.container}>

            <h1>React Student Attendance Component</h1>

            <div style={styles.summary}>
                <div style={styles.card}>
                    <h3>Total Students</h3>
                    <p>{students.length}</p>
                </div>

                <div style={styles.card}>
                    <h3>Low Attendance</h3>
                    <p>{lowAttendanceCount}</p>
                </div>
            </div>

            <div style={styles.form}>
                <h2>Add Student</h2>

                <input
                    type="text"
                    placeholder="Student Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={styles.input}
                />

                <input
                    type="text"
                    placeholder="Roll Number"
                    value={rollNumber}
                    onChange={(e) => setRollNumber(e.target.value)}
                    style={styles.input}
                />

                <button
                    onClick={addStudent}
                    style={styles.button}
                >
                    Add Student
                </button>
            </div>

            <div style={styles.tableContainer}>

                <h2>Student Attendance</h2>

                <table style={styles.table}>

                    <thead>
                        <tr>
                            <th style={styles.th}>Roll Number</th>
                            <th style={styles.th}>Name</th>
                            <th style={styles.th}>Attendance</th>
                            <th style={styles.th}>Status</th>
                            <th style={styles.th}>Action</th>
                        </tr>
                    </thead>

                    <tbody>

                        {students.map((student) => (

                            <tr key={student.id}>

                                <td style={styles.td}>
                                    {student.rollNumber}
                                </td>

                                <td style={styles.td}>
                                    {student.name}
                                </td>

                                <td style={styles.td}>
                                    {student.attendance}%
                                </td>

                                <td style={styles.td}>
                                    {student.attendance < 75
                                        ? "Low Attendance"
                                        : "Good"}
                                </td>

                                <td style={styles.td}>

                                    <button
                                        onClick={() =>
                                            deleteStudent(student.id)
                                        }
                                        style={styles.deleteButton}
                                    >
                                        Delete
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    );
}

const styles = {

    container: {
        fontFamily: "Arial, sans-serif",
        padding: "30px",
        maxWidth: "1000px",
        margin: "auto"
    },

    summary: {
        display: "flex",
        gap: "20px",
        marginBottom: "30px"
    },

    card: {
        background: "#f4f6f8",
        padding: "20px",
        borderRadius: "8px",
        flex: 1,
        textAlign: "center"
    },

    form: {
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "8px",
        marginBottom: "30px"
    },

    input: {
        padding: "10px",
        marginRight: "10px",
        marginBottom: "10px",
        border: "1px solid #ccc",
        borderRadius: "5px"
    },

    button: {
        padding: "10px 18px",
        background: "#2563eb",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer"
    },

    tableContainer: {
        marginTop: "20px"
    },

    table: {
        width: "100%",
        borderCollapse: "collapse"
    },

    th: {
        background: "#1f2937",
        color: "white",
        padding: "12px"
    },

    td: {
        padding: "12px",
        borderBottom: "1px solid #ddd",
        textAlign: "center"
    },

    deleteButton: {
        background: "#dc2626",
        color: "white",
        border: "none",
        padding: "8px 12px",
        borderRadius: "5px",
        cursor: "pointer"
    }
};

export default App;s