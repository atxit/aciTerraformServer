"""
Mongo Connector is responsible for all interactions between the code and the mongo DB
"""
import pymongo

import pandas as pd


class MongoConnector:
    """
    A grouping of mongo related methods.
    """

    def __init__(self):
        self.collection = None

    def init_client(self, collection_name):
        """
        initiates the mongo client
        :param collection_name: applies the collection name to the client
        """
        pymongo_client = pymongo.MongoClient("localhost", 27017)
        pymongo_db = pymongo_client["aciTfServer"]
        self.collection = pymongo_db[collection_name]

    def remove_collection(self):
        """
        removes the collection (table) from Mongo
        :return: NO RETURN
        """
        self.collection.drop()

    def write_collection(self, df_db):
        """
        bulk update to mongo collection/table
        :return: NO RETURN
        """
        _ = self.collection.insert_many(df_db.to_dict("records"))

    def return_value_from_table(self, searched_column, find_key, return_value_in):
        """
        :param searched_column: the column (head/field) in which to search for the key.
        :param find_key: the key to match on when searching within the provided column.
        :param return_value_in: the column location (head/field) of the value.
        :return: returns the value which corresponds to the key match.
         - returns DF is search was successful.
         - returns None if no data was found.
        """
        df_search = pd.DataFrame(
            list(self.collection.find({searched_column: find_key}))
        )
        if len(df_search) > 0:
            return df_search.set_index(searched_column).at[find_key, return_value_in]
        return None

    def return_full_collection(self):
        """
        :param searched_column: the column (head/field) in which to search for the key.
        :param find_key: the key to match on when searching within the provided column.
        :return: a slice of the DB which matches the input args
        """
        df_returned = pd.DataFrame(list(self.collection.find()))
        if len(df_returned) > 0 and "_id" in df_returned.columns:
            df_returned.drop(columns=["_id"], inplace=True)
            return df_returned
        return pd.DataFrame()
