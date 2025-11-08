import express from "express";
import sqlite3 from "sqlite3";
import { open } from "sqlite";

const app = express();
const port = 8080;

app.set("view engine", "ejs");
app.use(express.static("public"));

// Set up database connection
async function openDb() {
  return open({
    filename: "./hacker.sqlite",
    driver: sqlite3.Database,
  });
}

app.get("/", async (req, res) => {
  try {
    const db = await openDb();
    const searchTerm = req.query.term || "";

    // Intentional SQL injection point for CTF
    // ' AND task_name LIKE '%${searchTerm}%
    if (searchTerm) {
      const query = `SELECT task_name FROM tasks WHERE user_level = 'normal' AND task_name = '%${searchTerm}%'`;
      console.log(query);
      const results = await db.all(query);
      console.log(results);
      res.render("index", { tasks: results });
    } else {
      const query = "SELECT task_name FROM tasks WHERE user_level = 'normal'";
      const results = await db.all(query);
      res.render("index", { tasks: results });
    }
  } catch (err) {
    console.error(err);
    res.send("Error");
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
