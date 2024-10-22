#!/usr/bin/env python3
"""returns all students by sorted average"""

def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.
    The output will include a new field 'averageScore'.
    :param mongo_collection: pymongo collection object
    :return: list of students sorted by average score
    """
    # Use MongoDB aggregation to calculate average scores and sort
    pipeline = [
        {
            "$project": {
                "name": 1,  # Include the 'name' field
                "averageScore": { "$avg": "$scores" }  # Calculate the average of 'scores'
            }
        },
        { 
            "$sort": { "averageScore": -1 }  # Sort by 'averageScore' in descending order
        }
    ]
    
    # Perform the aggregation and return the results as a list
    return list(mongo_collection.aggregate(pipeline))
