#!/usr/bin/env python3
""" changes all topics of a school document based on the name"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """
    Updates all topics of a school document based on the name.
    :param mongo_collection: The pymongo collection object
    :param name: The school name to update (string)
    :param topics: The list of topics (list of strings) to set for the school
    """
    mongo_collection.update_many(
        {"name": name},  # Filter documents where name matches
        {"$set": {"topics": topics}}  # Set the new topics list
    )
