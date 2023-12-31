import sys
from unittest.mock import patch, mock_open, MagicMock

import pandas as pd
import pytest

from source.import_aci_tf import (
    open_hcl_file,
    extract_data_from_dict,
    resolve_resource_id,
    parse_args,
    ImportTfFiles,
    epoch_to_utc,
)


def test_open_hcl_file(sample_hcl_file):
    result = open_hcl_file(sample_hcl_file)
    assert result == {"key1": "value1", "key2": "value2"}


def test_open_hcl_file_with_invalid_file():
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = ValueError("Invalid JSON")
        result = open_hcl_file("/path/to/invalid.tf")
        mock_file.assert_called_once_with("/path/to/invalid.tf", encoding="UTF-8")
        assert result == {}


def test_extract_data_from_dict():
    dictionary_1 = {"key1": "value1", "key2": "value2"}
    expected_result_1 = [("key1", "value1"), ("key2", "value2")]
    assert list(extract_data_from_dict(dictionary_1)) == expected_result_1

    dictionary_2 = {"key1": {"nested_key": "nested_value"}, "key2": "value2"}
    expected_result_2 = [("key1.nested_key", "nested_value"), ("key2", "value2")]
    assert list(extract_data_from_dict(dictionary_2)) == expected_result_2

    dictionary_3 = {
        "key1": [{"list_key": "list_value"}, {"list_key": "list_value2"}],
        "key2": "value2",
    }
    expected_result_3 = [
        ("key1.list_key", "list_value"),
        ("key1.list_key", "list_value2"),
        ("key2", "value2"),
    ]
    assert list(extract_data_from_dict(dictionary_3)) == expected_result_3

    dictionary_4 = {}
    expected_result_4 = []
    assert list(extract_data_from_dict(dictionary_4)) == expected_result_4

    dictionary_5 = {"key1": "value1", "key2": {"nested_key": "nested_value"}}
    expected_result_5 = [("key1", "value1"), ("key2.nested_key", "nested_value")]
    assert (
        list(extract_data_from_dict(dictionary_5, resource_id="")) == expected_result_5
    )


def test_resolve_resource_id():
    resource_key_1 = "resource.key1.key2.id"
    expected_result_1 = "key1.key2.id"
    assert resolve_resource_id(resource_key_1) == expected_result_1

    resource_key_2 = "resource.key1.key2.key3.id"
    expected_result_2 = "key1.key2.id"
    assert resolve_resource_id(resource_key_2) == expected_result_2

    resource_key_3 = "not_a_resource.key1.key2.id"
    expected_result_3 = "N/A"
    assert resolve_resource_id(resource_key_3) == expected_result_3

    resource_key_4 = "key1.key2.id"
    expected_result_4 = "N/A"
    assert resolve_resource_id(resource_key_4) == expected_result_4

    resource_key_5 = ""
    expected_result_5 = "N/A"
    assert resolve_resource_id(resource_key_5) == expected_result_5


def test_parse_args():
    with patch.object(sys, "argv", ["script_name", "-f", "/path/to/folder"]):
        result = parse_args()
        assert result == "/path/to/folder"

    with patch.object(sys, "argv", ["script_name"]):
        with pytest.raises(SystemExit) as e:
            parse_args()
        assert e.value.code == 1


def test_import_tf_file_class_init():
    import_tf_files = ImportTfFiles(file_location="test")
    assert import_tf_files.file_location == "test"

    import_tf_files = ImportTfFiles(file_location="test", return_diff=True)
    assert import_tf_files.return_diff == True


def test_search_tf_files():
    with patch(
        "source.import_aci_tf.glob.glob",
        return_value=["/path/to/file1.tf", "/path/to/file2.tf"],
    ):
        import_tf = ImportTfFiles("/path/to", return_diff=True)
        import_tf.search_tf_files()
        assert import_tf.tf_file_list == ["/path/to/file1.tf", "/path/to/file2.tf"]


class Executor:
    @staticmethod
    def result():
        return pd.DataFrame.from_dict(
            {
                "file": {1: "test"},
                "resourceId": {1: "test"},
                "resourceKey": {1: "resource.test"},
                "resourceType": {1: "test"},
                "resourceValue": {1: "test"},
            }
        )


def test_start_processing():
    with patch("source.import_aci_tf.concurrent.futures.ThreadPoolExecutor"):
        with patch(
            "source.import_aci_tf.concurrent.futures.as_completed",
            return_value=[Executor],
        ):
            import_tf = ImportTfFiles("/path/to")
            import_tf.tf_file_list = ["/path/to/file1.tf"]
            import_tf.start_processing()


def test_start_processing_nothing_returned():
    with patch("source.import_aci_tf.concurrent.futures.ThreadPoolExecutor"):
        with patch(
            "source.import_aci_tf.concurrent.futures.as_completed", return_value={}
        ):
            import_tf = ImportTfFiles("/path/to")
            import_tf.tf_file_list = ["/path/to/file1.tf"]
            import_tf.df_tf = pd.DataFrame.from_dict(
                {
                    "file": {1: "test"},
                    "resourceId": {1: "test"},
                    "resourceKey": {1: "resource.test"},
                    "resourceType": {1: "test"},
                    "resourceValue": {1: "test"},
                }
            )
            import_tf.start_processing()


def test_import_hcl_failed(import_hcl_failed_results):
    with patch("source.import_aci_tf.open_hcl_file", return_value={}):
        import_tf = ImportTfFiles("/path/to")
        results = import_tf.import_hcl(file_path="test")
        assert results.to_dict() == import_hcl_failed_results


def test_import_hcl_locals():
    with patch(
        "source.import_aci_tf.open_hcl_file", return_value={"locals": {"test": "test"}}
    ):
        import_tf = ImportTfFiles("/path/to")
        results = import_tf.import_hcl(file_path="test")
        assert results.to_dict() == {}
        assert import_tf.locals_dict == {"local.test": "test"}


def test_import_hcl_provider():
    with patch("source.import_aci_tf.open_hcl_file", return_value={"provider": {}}):
        import_tf = ImportTfFiles("/path/to")
        results = import_tf.import_hcl(file_path="test")
        assert results.to_dict() == {}


@patch(
    "source.import_aci_tf.open_hcl_file", return_value={"resource": {"test": "test"}}
)
@patch("source.import_aci_tf.resolve_resource_id", return_value="test")
def test_import_hcl_resource(resolve_resource_id, open_hcl_file):
    import_tf = ImportTfFiles("/path/to")
    results = import_tf.import_hcl(file_path="test")
    assert results.to_dict() == {
        "file": {1: "test"},
        "resourceId": {1: "test"},
        "resourceKey": {1: "resource.test"},
        "resourceType": {1: "test"},
        "resourceValue": {1: "test"},
    }


@patch("source.import_aci_tf.open_hcl_file", return_value={"module": {"test": "test"}})
@patch("source.import_aci_tf.resolve_resource_id", return_value="test")
def test_import_hcl_module(resolve_resource_id, open_hcl_file):
    import_tf = ImportTfFiles("/path/to")
    results = import_tf.import_hcl(file_path="test")
    assert results.to_dict() == {
        "file": {1: "test"},
        "resourceId": {1: "test"},
        "resourceKey": {1: "module.test"},
        "resourceType": {1: "test"},
        "resourceValue": {1: "test"},
    }


def test_perform_diff_no_diff(mocker):
    import_tf = ImportTfFiles("/path/to")
    import_tf.tf_file_list = ["/path/to/file1.tf"]
    import_tf.df_tf = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    mongo_connector_aci_tf = mocker.patch.object(
        ImportTfFiles, "mongo_connector_aci_tf"
    )
    mongo_connector_aci_tf.return_full_collection.return_value = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    error, result = import_tf.perform_diff()
    assert error is True
    assert result == "no diff detected"


def test_perform_diff_missing(mocker):
    import_tf = ImportTfFiles("/path/to")
    import_tf.tf_file_list = ["/path/to/file1.tf"]
    import_tf.df_tf = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    mongo_connector_aci_tf = mocker.patch.object(
        ImportTfFiles, "mongo_connector_aci_tf"
    )
    mongo_connector_aci_tf.return_full_collection.return_value = pd.DataFrame.from_dict(
        {}
    )

    error, result = import_tf.perform_diff()
    assert error is True
    assert result == "could not diff, past or present DataFrames missing"


def test_perform_diff_diff_return(mocker):
    import_tf = ImportTfFiles("/path/to", return_diff=True)
    import_tf.tf_file_list = ["/path/to/file1.tf"]
    import_tf.df_tf = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test1"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    mongo_connector_aci_tf = mocker.patch.object(
        ImportTfFiles, "mongo_connector_aci_tf"
    )
    mongo_connector_aci_tf.return_full_collection.return_value = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    error, result = import_tf.perform_diff()
    assert error is False
    assert result.to_dict() == {
        "file": {1: "test"},
        "importTime": {1: 0},
        "resourceId": {1: "test"},
        "resourceKey": {1: "resource.test"},
        "resourceType": {1: "test"},
        "resourceValue": {1: "test"},
        "updateType": {1: "removal"},
    }


@patch("source.import_aci_tf.MongoConnector")
def test_perform_diff_diff_mongo(patch_mongo, mocker):
    import_tf = ImportTfFiles("/path/to", return_diff=False)
    import_tf.tf_file_list = ["/path/to/file1.tf"]
    import_tf.df_tf = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test1"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    mongo_connector_aci_tf = mocker.patch.object(
        ImportTfFiles, "mongo_connector_aci_tf"
    )
    mongo_connector_aci_tf.return_full_collection.return_value = pd.DataFrame.from_dict(
        {
            "file": {1: "test"},
            "importTime": {1: "now"},
            "resourceId": {1: "test"},
            "resourceKey": {1: "resource.test"},
            "resourceType": {1: "test"},
            "resourceValue": {1: "test"},
        }
    )

    error, result = import_tf.perform_diff()
    assert error is False
    assert result == None


def test_apply_locals(post_table_dict_results, apply_locals_results):
    import_tf = ImportTfFiles("/path/to", return_diff=False)
    import_tf.df_tf = pd.DataFrame.from_dict(post_table_dict_results)
    import_tf.locals_dict = {"aci_tenant.demo-test.id": "changed"}
    import_tf.apply_locals()
    assert import_tf.df_tf.to_dict() == apply_locals_results


@patch("source.import_aci_tf.MongoConnector")
def test_main_return_no_tf_files(patch_mongo):
    import_tf = ImportTfFiles("/path/to", return_diff=False)
    import_tf.search_tf_files = MagicMock()
    import_tf.tf_file_list = []
    error, result = import_tf.main()
    assert error is True
    assert result == "no .tf files in /path/to"


@patch("source.import_aci_tf.MongoConnector")
def test_main_return_tf_files_return(patch_mongo):
    import_tf = ImportTfFiles("/path/to", return_diff=True)
    import_tf.search_tf_files = MagicMock()
    import_tf.tf_file_list = ["test"]
    import_tf.start_processing = MagicMock()
    import_tf.apply_locals = MagicMock()
    mock_perform_diff = MagicMock()
    mock_perform_diff.return_value = (False, {})
    import_tf.perform_diff = mock_perform_diff
    error, result = import_tf.main()
    assert error is False
    assert result == {}


@patch("source.import_aci_tf.MongoConnector")
def test_main_return_tf_files(patch_mongo):
    import_tf = ImportTfFiles("/path/to", return_diff=False)
    import_tf.search_tf_files = MagicMock()
    import_tf.tf_file_list = ["test"]
    import_tf.start_processing = MagicMock()
    import_tf.apply_locals = MagicMock()
    mock_perform_diff = MagicMock()
    mock_perform_diff.return_value = (False, {})
    import_tf.perform_diff = mock_perform_diff
    error, result = import_tf.main()
    assert error is False
    assert result is None


def test_epoch_to_utc():
    assert epoch_to_utc(111) == "1970-01-01 00:01:51 UTC"
