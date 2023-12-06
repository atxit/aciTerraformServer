"""
Mongo Connector is responsible for all interactions between the code and the mongo DB
"""
from datetime import datetime, timezone

import pymongo
import pandas as pd

from source.constants import *


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

    def search_all_columns_for_item(self,searched_item):
        df_results = pd.DataFrame()

        for column_id in FIELD_LIST:
            if searched_item != 'all':
                query_dict = {column_id: {'$regex': searched_item, '$options': 'i'}}
            else:
                query_dict = {}
            df_results = pd.concat([df_results, pd.DataFrame(
                list(self.collection.find(query_dict)))])

        if len(df_results) > 0:
            df_results.drop_duplicates(inplace=True)
            df_results.drop(columns=['_id'], inplace=True)
            df_results['importTime'] = df_results['importTime'].apply(epoch_to_utc)
        print(df_results)
        return df_results

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

    def return_distinct_values_of_column(self, column_name):
        return self.collection.distinct(column_name)

def epoch_to_utc(epoch_value):
    utc_datetime = datetime.utcfromtimestamp(epoch_value).replace(tzinfo=timezone.utc)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')

