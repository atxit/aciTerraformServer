"""
The import ACI TF module is responsible for importing the HCL/TF files and performing
 diffs.
"""
import copy
import time
import glob
import concurrent.futures
import argparse
import sys

import pandas as pd
import numpy as np
import hcl

from source.mongo_connect import MongoConnector, epoch_to_utc
from source.constants import FIELD_LIST


def open_hcl_file(tf_file_path):
    """
    :param tf_file_path: location of TF file
    :return: HCL in dict format
    """
    try:
        with open(tf_file_path, encoding="UTF-8") as file_handler:
            return hcl.load(file_handler)
    except ValueError:
        return {}


def extract_data_from_dict(dictionary, resource_id=""):
    """
    :param dictionary: The input HCL dict
    :param resource_id: resource ID
    :return: the full resource ID and its value
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            yield from extract_data_from_dict(value, ".".join((resource_id, key)))
        elif isinstance(value, list):
            for value_list in value:
                if isinstance(value_list, dict):
                    yield from extract_data_from_dict(
                        value_list, ".".join((resource_id, key))
                    )
        else:
            yield ".".join((resource_id, key)).lstrip("."), value


def resolve_resource_id(resource_key):
    """
    :param resource_key: regenerates the resource key ID field
    :return: resource key ID (for resources) or N/A (for modules)
    """
    if resource_key.split(".")[0] == "resource":
        return (
            ".".join((resource_key.split(".")[1], resource_key.split(".")[2])) + ".id"
        )
    return "N/A"


def parse_args():
    """
    Parsers the input args, not used when this module is imported
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default=None, help="folder location containing .tf files")
    args = parser.parse_args(sys.argv[1:])
    if args.f is None:
        print("please provide folder location")
        sys.exit(1)
    return args.f


class ImportTfFiles:
    """
    import TF class
    """

    tf_file_list = []
    df_tf = pd.DataFrame()
    locals_dict = {}
    mongo_connector_aci_tf = None
    import_time = 0

    def __init__(self, file_location, return_diff=False):
        super().__init__()
        self.file_location = file_location
        self.return_diff = return_diff

    def search_tf_files(self):
        """
        locates all .tf files found within the file_location var
        :return:
        """
        self.tf_file_list = glob.glob(f"{self.file_location}/*.tf")

    def start_processing(self):
        """
        :return: dataFrame containing TF input values
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            cfg_executor = {
                executor.submit(self.import_hcl, file_path): file_path
                for file_path in self.tf_file_list
            }
            for future_results in concurrent.futures.as_completed(cfg_executor):
                self.df_tf = pd.concat(
                    [self.df_tf, future_results.result()], axis=0, sort=False
                )

        print(self.df_tf)
        self.df_tf.index = np.arange(1, len(self.df_tf) + 1)
        if len(self.df_tf) > 0:
            self.df_tf.insert(0, "importTime", self.import_time)

    def import_hcl(self, file_path):
        """
        :param file_path: location of TF file
        :return: A dataFrame which contains the contents of the HCL file
        """
        i = 1
        df_tf = pd.DataFrame(
            columns=FIELD_LIST,
            index=[i],
        )

        hcl_dict = open_hcl_file(file_path)
        print(hcl_dict)
        if "locals" in hcl_dict:
            locals_dict = hcl_dict["locals"]
            for key_local, value_local in locals_dict.items():
                self.locals_dict.update({".".join(("local", key_local)): value_local})
            return pd.DataFrame()

        if "provider" in hcl_dict:
            return pd.DataFrame()

        if "resource" in hcl_dict or "module" in hcl_dict:
            print(hcl_dict)
            for resource_key, resource_value in extract_data_from_dict(hcl_dict):
                print(resource_key)
                df_tf.loc[i, "file"] = file_path
                df_tf.loc[i, "resourceType"] = str(resource_key.split(".")[1])
                df_tf.loc[i, "resourceId"] = str(resolve_resource_id(resource_key))
                df_tf.loc[i, "resourceKey"] = str(resource_key)
                df_tf.loc[i, "resourceValue"] = str(resource_value)
                i += 1
            return df_tf

        df_tf.loc[1, "file"] = file_path
        df_tf.loc[1, "resourceType"] = "failed to import"
        df_tf.loc[1, "resourceId"] = "failed to import"
        df_tf.loc[1, "resourceKey"] = "failed to import"
        df_tf.loc[1, "resourceValue"] = "failed to import"

        return df_tf

    def perform_diff(self):
        """
        performs a diff by comparing the update against the existing collection
        if nothing has changed, no diff will be recorded.
        if change (or an updated) has occured then two lines are generated
        for a removal or addition, only one line is present
        :return:
        """

        df_past = self.mongo_connector_aci_tf.return_full_collection()
        if len(df_past) > 0 and len(self.df_tf) > 0:
            df_present = copy.deepcopy(self.df_tf)
            df_present.insert(0, "updateType", "addition")
            df_past.insert(0, "updateType", "removal")
            df_diff_concat = (
                pd.concat([df_present, df_past])
                .drop_duplicates(
                    subset=[
                        "resourceType",
                        "resourceId",
                        "resourceKey",
                        "resourceValue",
                    ],
                    keep=False,
                )
                .drop(columns=["importTime"])
            )
            if len(df_diff_concat) > 0:
                df_diff_concat.insert(0, "importTime", self.import_time)

                if self.return_diff:
                    print(df_diff_concat)
                    df_diff_concat["importTime"] = df_diff_concat["importTime"].apply(
                        epoch_to_utc
                    )
                    return False, df_diff_concat

                mongo_connector_diff = MongoConnector()
                mongo_connector_diff.init_client(collection_name="aciTfCollectionDiff")

                mongo_connector_diff.write_collection(
                    df_db=df_diff_concat.sort_values(
                        by=[
                            "resourceType",
                            "resourceId",
                            "resourceKey",
                            "resourceValue",
                        ]
                    )
                )
                return False, None

            return True, "no diff detected"

        return True, "could not diff, past or present DataFrames missing"

    def apply_locals(self):
        """
        resolves local var if present
        """
        if len(self.locals_dict) > 0:
            self.df_tf["resourceValue"] = self.df_tf["resourceValue"].apply(
                lambda x: self.locals_dict.get(x, x)
            )

    def main(self):
        """
        main processing block
        :return: error (bool) and error message (if True) or False and DataFrame (if return_diff)
         or None (if not)
        """
        self.mongo_connector_aci_tf = MongoConnector()
        self.mongo_connector_aci_tf.init_client(collection_name="aciTfCollection")
        self.import_time = time.time()

        self.search_tf_files()
        if len(self.tf_file_list) > 0:
            self.start_processing()
            self.apply_locals()
            diff_error, df_diff = self.perform_diff()
            if self.return_diff:
                return diff_error, df_diff

            self.mongo_connector_aci_tf.remove_collection()
            self.mongo_connector_aci_tf.write_collection(df_db=self.df_tf)
            print("completed")
            return False, None
        return True, f"no .tf files in {self.file_location}"



if __name__ == "__main__":
    import_tf_files = ImportTfFiles(parse_args()) # pragma: no cover
    error, error_msg = import_tf_files.main() # pragma: no cover
    if error: # pragma: no cover
        print(error_msg) # pragma: no cover
