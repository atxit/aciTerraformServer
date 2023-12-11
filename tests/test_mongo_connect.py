import sys
from unittest.mock import patch, mock_open, MagicMock

import pandas as pd
import pytest

from source.mongo_connect import MongoConnector


@patch("source.mongo_connect.pymongo")
def test_init_client(patch_pymongo):
    mongo = MongoConnector()
    mongo.init_client(collection_name="test")
    assert isinstance(mongo.collection, MagicMock)


def test_remove_collection():
    mongo = MongoConnector()
    mongo.collection = MagicMock()
    mongo.remove_collection()


def test_write_collection():
    mongo = MongoConnector()
    mongo.collection = MagicMock()
    mongo.write_collection(
        pd.DataFrame.from_dict(
            {
                "file": {1: "test"},
                "importTime": {1: "now"},
                "resourceId": {1: "test"},
                "resourceKey": {1: "resource.test"},
                "resourceType": {1: "test"},
                "resourceValue": {1: "test"},
            }
        )
    )


def test_search_all_columns_for_item(write_collection_fixture):
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = write_collection_fixture
    mongo.collection = mongo_mock
    result = mongo.search_all_columns_for_item("test")
    assert result.to_dict() == {
        "file": {
            0: "/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf"
        },
        "importTime": {0: "2023-12-08 10:07:43 UTC"},
        "resourceId": {
            0: "aci_bgp_address_family_context.bgp-family-context-example.id"
        },
        "resourceKey": {
            0: "resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn"
        },
        "resourceType": {0: "aci_bgp_address_family_context"},
        "resourceValue": {0: "aci_tenant.demo-test.id"},
    }


def test_search_all_columns_for_item_all(write_collection_fixture):
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = write_collection_fixture
    mongo.collection = mongo_mock
    result = mongo.search_all_columns_for_item("all")
    assert result.to_dict() == {
        "file": {
            0: "/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf"
        },
        "importTime": {0: "2023-12-08 10:07:43 UTC"},
        "resourceId": {
            0: "aci_bgp_address_family_context.bgp-family-context-example.id"
        },
        "resourceKey": {
            0: "resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn"
        },
        "resourceType": {0: "aci_bgp_address_family_context"},
        "resourceValue": {0: "aci_tenant.demo-test.id"},
    }


def test_search_all_columns_no_results():
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = {}
    mongo.collection = mongo_mock
    result = mongo.search_all_columns_for_item("test")
    assert result.to_dict() == {}


def test_return_value_from_table(return_value_from_table_fixture):
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = return_value_from_table_fixture
    mongo.collection = mongo_mock
    result = mongo.return_value_from_table(
        searched_column="key", find_key="path", return_value_in="value"
    )
    assert result == "/Users/machine/projects/aciTerraformServer/example"


def test_return_value_from_table_return_none():
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = {}
    mongo.collection = mongo_mock
    result = mongo.return_value_from_table(
        searched_column="key", find_key="path", return_value_in="value"
    )
    assert result is None


def test_return_full_collection(return_value_from_table_fixture):
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = return_value_from_table_fixture
    mongo.collection = mongo_mock
    result = mongo.return_full_collection()
    assert result.to_dict() == {
        "key": {0: "path"},
        "value": {0: "/Users/machine/projects/aciTerraformServer/example"},
    }


def test_return_full_collection_return_empty_df():
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = {}
    mongo.collection = mongo_mock
    result = mongo.return_full_collection()
    assert result.to_dict() == {}


def test_return_distinct_values_of_column():
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.distinct.return_value = "test"
    mongo.collection = mongo_mock
    result = mongo.return_distinct_values_of_column("test")
    assert result == "test"


def test_insert_single_value(return_value_from_table_fixture):
    mongo = MongoConnector()
    mongo_mock = MagicMock()
    mongo_mock.find.return_value = return_value_from_table_fixture
    mongo.collection = mongo_mock
    mongo.insert_single_value(
        search_column="test",
        search_value="test",
        update_column="test",
        updated_value="test",
    )
