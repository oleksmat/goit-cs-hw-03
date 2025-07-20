import psycopg2
from psycopg2 import Error

def connect_to_database():
    try:
        connection = psycopg2.connect("")
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def setup_database(connection):
    try:
        cursor = connection.cursor()

        setup_script = """
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id       SERIAL PRIMARY KEY,
                           fullname VARCHAR(100) NOT NULL,
                           email    VARCHAR(100) NOT NULL UNIQUE
                       );

                       CREATE TABLE IF NOT EXISTS status
                       (
                           id   SERIAL PRIMARY KEY,
                           name VARCHAR(50) NOT NULL UNIQUE
                       );

                       CREATE TABLE IF NOT EXISTS tasks
                       (
                           id          SERIAL PRIMARY KEY,
                           title       VARCHAR(100) NOT NULL,
                           description TEXT,
                           status_id   INTEGER REFERENCES status (id),
                           user_id     INTEGER REFERENCES users (id) ON DELETE CASCADE
                       );

                       INSERT INTO status (name)
                       VALUES ('new'),
                              ('in progress'),
                              ('completed');
        """

        # Execute SQL script
        cursor.execute(setup_script)
        connection.commit()
        print("Tables created successfully")

    except Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    # Connect to database
    connection = connect_to_database()

    if connection:
        # Create users table
        setup_database(connection)

        # Close database connection
        connection.close()
