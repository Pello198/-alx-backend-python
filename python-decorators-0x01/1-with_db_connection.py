#!/usr/bin/env python3
import sqlite3
import functools


def with_db_connection(func):
    """Decorator that opens and closes a database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open connection
        conn = sqlite3.connect("users.db")
        try:
            # Pass connection as first argument to the function
            result = func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is always closed
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


#### Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
