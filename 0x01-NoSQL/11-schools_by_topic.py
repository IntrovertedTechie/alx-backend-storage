#!/usr/bin/env python3
"""
script list school
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    script returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})
