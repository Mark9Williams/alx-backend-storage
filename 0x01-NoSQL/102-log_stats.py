#!/usr/bin/env python3
"""provides statistics about nginx"""
from pymongo import MongoClient


def log_stats():
    """Provides statistics about Nginx logs stored in MongoDB"""
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.logs  # Access the logs database
    collection = db.nginx  # Access the nginx collection

    # Total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count documents for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of documents with method=GET and path=/status
    status_check = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 most frequent IP addresses
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 10}  # Limit to the top 10
    ]
    top_ips = list(collection.aggregate(pipeline))

    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
