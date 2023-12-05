import os
import time
from pathlib import Path
import re
import pickle
import glob
import logging
import subprocess
from datetime import datetime,timezone
import concurrent.futures
import argparse
import sys
import pandas as pd
import numpy as np
import hcl


if "__file__" in globals():
    WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
else:
    WORKING_DIRECTORY = os. getcwd()


def rename_local(resource_key) :
    return "local."+ resource_key


def prepare_local(resource_key):
    """Lambdo func: Returns Locoted Locol value"""
    return re.findall(r" (local\-[\w]+)",resource_key)[0]


def open_hcl_file(hcl_file):
    """Opens and reads the HCL file"""
    with open(hcl_file, encoding="UTF-8") as file_handler:
        return hcl.load(file_handler)


def extract_data_from_dict(dictionary, resource_id=''):
    """Returns key/value items Using a recursive Lookup (using DevNet resource files)"""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            yield from extract_data_from_dict (value, ".".join((resource_id, key)))
        elif isinstance(value, list):
            for value_list in value:
                if isinstance (value_list, dict):
                    yield from extract_data_from_dict(value_list,".".join((resource_id, key)))
        else:
            yield ".".join((resource_id, key)).lstrip('.'), value


files_with_prefix = ['/Users/antonyoliver/projects/cognition/aci/demo/example/nac_contract.tf']
#files_with_prefix = ['/Users/antonyoliver/projects/cognition/aci/demo/example/test_tenant.tf']
file_location = '/Users/antonyoliver/projects/cognition/aci/demo/example'


def resolve_resource_id(resource_key):
    if resource_key.split('.')[0] == 'resource':
        return '.'.join((resource_key.split('.')[1],resource_key.split('.')[2]))+'.id'
    return 'N/A'


def build():
    i = 1
    df_tf = pd.DataFrame(columns=['file','resourceType','resourceId','resourceKey','resourceValue'], index=[i])
    print("Files starting with '.tf':")
    for file_path in glob.glob(f"{file_location}/*.tf"):
        print(file_path)
        hcl_dict = open_hcl_file(file_path)
        if 'locals' in hcl_dict:
            locals_dict = hcl_dict['locals']
        elif 'resource' in hcl_dict or 'module' in hcl_dict:
            for resource_key, resource_value in extract_data_from_dict(hcl_dict):
                df_tf.loc[i,'file'] = file_path
                df_tf.loc[i,'resourceType'] = str(resource_key.split('.')[1])
                df_tf.loc[i,'resourceId'] = str(resolve_resource_id(resource_key))
                df_tf.loc[i,'resourceKey'] = str(resource_key)
                df_tf.loc[i,'resourceValue'] = str(resource_value)
                i +=1
    return df_tf

