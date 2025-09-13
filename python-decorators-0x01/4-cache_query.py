#!/usr/bin/env python3
import time
import sqlite3
import functools


query_cache = {}


def with_db_connection(func):
    """Decorator that opens and closes a database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from args/kwargs
        query = None
        if "query" in kwargs:
            query = kwargs["query"]
        elif len(args) > 1:  # args[0] is conn, so query should be at index 1
            query = args[1]

        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Cached result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call:", users)

    #### Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call:", users_again)
