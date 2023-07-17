#!/usr/bin/env python3
"""
script inserts a new document in a collection based on kwargs
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    script insert into mongo_collection
    """
    return mongo_collection.insert_one(kwargs).inserted_id
