#!/usr/bin/env python3
"""a Python function that lists all documents in a collection"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in the collection based on kwargs.
    :param mongo_collection: The pymongo collection object
    :param kwargs: The key-value pairs for the new document
    :return: The _id of the newly inserted document
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
