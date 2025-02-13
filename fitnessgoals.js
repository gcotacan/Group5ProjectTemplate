const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser');



const app = express();
app.use(bodyParser.json()); // or app.use(express.json()) if you prefer



const pool = new Pool({
  //user: 'YOUR_DB_USER',
  //host: 'localhost',
  //database: 'YOUR_DB_NAME',
  //password: 'YOUR_DB_PASSWORD',
  //port: 5432,
});



pool.query(`
  CREATE TABLE IF NOT EXISTS daily_goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    target_calories INT NOT NULL,
    target_protein INT NOT NULL,
    target_carbs INT NOT NULL,
    target_fats INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
`)
.then(() => {
  console.log('Table "daily_goals" is ready');
})
.catch(err => {
  console.error('Error creating table:', err);
});



app.post('/daily-goal', async (req, res) => {
  const { user_id, target_calories, target_protein, target_carbs, target_fats } = req.body;

  try {
    // Using Postgres's "ON CONFLICT" to upsert on user_id
    const query = `
      INSERT INTO daily_goals (user_id, target_calories, target_protein, target_carbs, target_fats)
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT (user_id)
      DO UPDATE SET
        target_calories = EXCLUDED.target_calories,
        target_protein  = EXCLUDED.target_protein,
        target_carbs    = EXCLUDED.target_carbs,
        target_fats     = EXCLUDED.target_fats,
        updated_at      = NOW()
      RETURNING goal_id;
    `;

    const values = [user_id, target_calories, target_protein, target_carbs, target_fats];
    const result = await pool.query(query, values);

    res.status(200).json({
      goal_id: result.rows[0].goal_id,
      message: 'Daily goals set successfully!'
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error setting daily goals' });
  }
});



app.get('/daily-goal/:user_id', async (req, res) => {
  const { user_id } = req.params;

  try {
    const query = `
      SELECT user_id, target_calories, target_protein, target_carbs, target_fats
      FROM daily_goals
      WHERE user_id = $1
    `;
    const result = await pool.query(query, [user_id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'No daily goal found for this user.' });
    }

    res.status(200).json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error retrieving daily goals' });
  }
});



const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
