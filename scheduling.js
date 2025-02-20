npm install express node-schedule node-notifier

const express = require('express');
const schedule = require('node-schedule');
const notifier = require('node-notifier');

const app = express();
app.use(express.json());

// In a real app, use a database. Here, we'll store in an array:
let reminders = [];

/**
 * POST /reminders
 * Body example:
 * {
 *   "title": "Stretch Break",
 *   "message": "Time to stand up and stretch",
 *   "notifyAt": "2025-02-25T10:00:00Z"
 * }
 */
app.post('/reminders', (req, res) => {
  const { title, message, notifyAt } = req.body;

  // Validate
  if (!title || !message || !notifyAt) {
    return res.status(400).json({ error: 'title, message, and notifyAt are required.' });
  }

  // Create a unique ID
  const id = reminders.length + 1;

  // Create reminder object
  const reminder = { id, title, message, notifyAt };
  reminders.push(reminder);

  // Schedule notification
  schedule.scheduleJob(new Date(notifyAt), () => {
    notifier.notify(
      {
        title: title,
        message: message,
        sound: true,        // Play a sound (on macOS and Windows)
        wait: false         // No action required from user to proceed
      },
      (err, response, metadata) => {
        if (err) {
          console.error(`Error showing notification #${id}`, err);
        } else {
          console.log(`Displayed notification #${id}: ${title}`);
        }
      }
    );
  });

  return res.json({
    message: 'Reminder scheduled',
    reminder
  });
});

/**
 * GET /reminders
 * Returns all current reminders (for debugging)
 */
app.get('/reminders', (req, res) => {
  res.json(reminders);
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
