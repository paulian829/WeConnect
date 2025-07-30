# WeConnect

WeConnect is a Flask based web application for managing user uploads, tasks and scheduling.  The
application integrates with a MySQL database and uses a large set of templates stored under
`templates/` for the user interface.  The project appears to have been used for a school or office
workflow where files are uploaded, reviewed and passed through several approval stages.

## Repository layout

- `flask_app.py` – main application file containing all Flask routes and logic.
- `database.py` – helper functions for interacting with the MySQL database.
- `Schedule.py` – small script that checks scheduled tasks and creates events.
- `weconnect.sql` – SQL dump used to create the MySQL schema and seed data.
- `templates/` – HTML templates for the UI.
- `static/` – static assets (CSS, JS and uploaded files).

The project also includes a `requirements.txt` with all Python dependencies and a minimal
`package.json` for Node dependencies (currently only `firebase-admin`).

## Setup

1. Create and activate a Python virtual environment.
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Import the database schema using the `weconnect.sql` file into your MySQL server.
4. Run the Flask development server:

   ```bash
   python flask_app.py
   ```

By default the application starts in debug mode and listens on the local machine.

## Notes for developers

New routes and database interactions are primarily handled in `flask_app.py` and
`database.py`.  The project makes heavy use of stored procedures defined inside the
MySQL database.  When making changes to the schema remember to update the
corresponding procedure calls in `database.py`.
