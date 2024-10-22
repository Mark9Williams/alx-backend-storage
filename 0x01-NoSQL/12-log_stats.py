#!/usr/bin/env python3
"""provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    # Connect to MongoDB (default connection)
    client = MongoClient()
    db = client.logs   # Database: logs
    collection = db.nginx  # Collection: nginx

    # Count total logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count logs per HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count logs for GET requests to /status
    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
