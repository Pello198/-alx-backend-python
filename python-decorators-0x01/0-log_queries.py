#!/usr/bin/env python3
import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # try to fetch query argument
        query = None
        if args:
            query = args[0]
        elif "query" in kwargs:
            query = kwargs["query"]

        if query:
            print(f"Executing SQL query: {query}")
        else:
            print("No SQL query provided")

        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
