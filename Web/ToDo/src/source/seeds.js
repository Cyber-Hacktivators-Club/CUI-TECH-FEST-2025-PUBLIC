import sqlite3 from "sqlite3";
import { open } from "sqlite";
import fs from "fs";

async function initializeFlag() {
  const flagPath = "/flag.txt";
  return new Promise((resolve, reject) => {
    fs.readFile(flagPath, "utf8", (err, data) => {
      if (err) {
        console.error("Failed to read flag:", err);
        reject(err);
        return;
      }
      const flag = data.trim();
        resolve(flag);

      fs.unlink(flagPath, (err) => {
        if (err) {
          console.error("Failed to delete flag file:", err);
          reject(err);
          return;
        }
        resolve(flag);
      });
    });
  });
}

async function setupDatabase(flag) {
  const db = await open({
    filename: "./hacker.sqlite",
    driver: sqlite3.Database,
  });

  await db.exec(`CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    user_level TEXT DEFAULT 'normal',
    description TEXT
  );`);

  await db.run(
    `INSERT INTO tasks (task_name, user_level, description) VALUES
    ('Complete the quarterly budget report', 'normal', 'Ensure all departments have submitted their reports.'),
    ('Plan team building activity', 'normal', 'Book a venue and prepare the actual agenda.'),
    ('Update project roadmap', 'normal', 'Revise the deadlines and milestones for the current projects.'),
    ('Employee performance reviews', 'admin', 'Review all employee performance by end of the month.'),
    ('Launch new product line', 'admin', 'Coordinate with the marketing and sales teams for the upcoming product launch.'),
    ('Secure offsite data backup', 'admin', 'Ensure all critical data is securely backed up at the offsite location.'),
    ('You can find the FLAG in the description, maybe?', 'admin', '${flag}');`
  );

  console.log("Database setup completed!");
  await db.close();
}

initializeFlag().then(setupDatabase).catch(console.error);
