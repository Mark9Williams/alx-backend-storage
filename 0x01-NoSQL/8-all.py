#!/usr/bin/env python3
"""a Python function that lists all documents in a collection"""

from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    :param mongo_collection: The pymongo collection object
    :return: A list of all documents, or an empty list if no document exists
    """
    documents = list(mongo_collection.find())
    return documents if documents else []
