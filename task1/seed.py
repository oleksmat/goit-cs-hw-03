import psycopg2
from psycopg2 import Error
from faker import Faker
import random

def connect_to_database():
    try:
        # makes psycopg connect using Postgres env variables
        # https://www.postgresql.org/docs/current/libpq-envars.html
        connection = psycopg2.connect("")
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def generate_users(cursor, num_users=10):
    fake = Faker()
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id",
            (fullname, email)
        )
    print(f"{num_users} users generated successfully")


def generate_tasks(cursor, num_tasks=100):
    fake = Faker()
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=4)[:-1]
        description = fake.text(max_nb_chars=200)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cursor.execute(
            """INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)""",
            (title, description, status_id, user_id)
        )
    print(f"{num_tasks} tasks generated successfully")


def setup_database(connection):
    try:
        cursor = connection.cursor()

        # Generate fake data
        generate_users(cursor)
        generate_tasks(cursor)

        connection.commit()
        print("Data generation completed successfully")

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
