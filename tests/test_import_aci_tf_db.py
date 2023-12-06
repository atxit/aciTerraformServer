import sys
from unittest.mock import patch, MagicMock
import pytest

from source.import_aci_tf import (open_hcl_file,
                                  extract_data_from_dict,
                                  resolve_resource_id,
parse_args,ImportTfFiles
                                  )


def test_open_hcl_file(sample_hcl_file):
    # Test if the function can open and read a sample HCL file
    result = open_hcl_file(sample_hcl_file)

    # Replace the assertions with the actual structure of your HCL file
    assert result == {"key1": "value1", "key2": "value2"}


def test_extract_data_from_dict():
    # Test case 1: Simple dictionary
    dictionary_1 = {'key1': 'value1', 'key2': 'value2'}
    expected_result_1 = [('key1', 'value1'), ('key2', 'value2')]
    assert list(extract_data_from_dict(dictionary_1)) == expected_result_1

    # Test case 2: Nested dictionary
    dictionary_2 = {'key1': {'nested_key': 'nested_value'}, 'key2': 'value2'}
    expected_result_2 = [('key1.nested_key', 'nested_value'), ('key2', 'value2')]
    assert list(extract_data_from_dict(dictionary_2)) == expected_result_2

    # Test case 3: Dictionary with lists
    dictionary_3 = {'key1': [{'list_key': 'list_value'}, {'list_key': 'list_value2'}], 'key2': 'value2'}
    expected_result_3 = [('key1.list_key', 'list_value'), ('key1.list_key', 'list_value2'), ('key2', 'value2')]
    assert list(extract_data_from_dict(dictionary_3)) == expected_result_3

    # Test case 4: Empty dictionary
    dictionary_4 = {}
    expected_result_4 = []
    assert list(extract_data_from_dict(dictionary_4)) == expected_result_4

    # Test case 5: Dictionary with an empty string as resource_id
    dictionary_5 = {'key1': 'value1', 'key2': {'nested_key': 'nested_value'}}
    expected_result_5 = [('key1', 'value1'), ('key2.nested_key', 'nested_value')]
    assert list(extract_data_from_dict(dictionary_5, resource_id='')) == expected_result_5


def test_resolve_resource_id():
    # Test case 1: Valid resource key
    resource_key_1 = 'resource.key1.key2.id'
    expected_result_1 = 'key1.key2.id'
    assert resolve_resource_id(resource_key_1) == expected_result_1

    # Test case 2: Valid resource key with more components
    resource_key_2 = 'resource.key1.key2.key3.id'
    expected_result_2 = 'key1.key2.id'
    assert resolve_resource_id(resource_key_2) == expected_result_2

    # Test case 3: Invalid resource key
    resource_key_3 = 'not_a_resource.key1.key2.id'
    expected_result_3 = 'N/A'
    assert resolve_resource_id(resource_key_3) == expected_result_3

    # Test case 4: Resource key without 'resource' prefix
    resource_key_4 = 'key1.key2.id'
    expected_result_4 = 'N/A'
    assert resolve_resource_id(resource_key_4) == expected_result_4

    # Test case 5: Empty resource key
    resource_key_5 = ''
    expected_result_5 = 'N/A'
    assert resolve_resource_id(resource_key_5) == expected_result_5


def test_parse_args():
    # Test case 1: Valid folder location provided
    with patch.object(sys, 'argv', ['script_name', '-f', '/path/to/folder']):
        result = parse_args()
        assert result == '/path/to/folder'

    # Test case 2: No folder location provided (should print message and exit)
    with patch.object(sys, 'argv', ['script_name']):
        with pytest.raises(SystemExit) as e:
            parse_args()
        assert e.value.code == 1


def test_import_tf_files():
    # Test case 1: Valid file location provided
    with patch('source.import_aci_tf.glob.glob', return_value=['/path/to/file1.tf', '/path/to/file2.tf']):
        import_tf = ImportTfFiles('/path/to', return_frame=True)
        import_tf.search_tf_files()

        # Ensure tf_file_list is populated correctly
        assert import_tf.tf_file_list == ['/path/to/file1.tf', '/path/to/file2.tf']

