import pytest
from import_aci_tf.import_aci_tf_db import open_hcl_file

@pytest.fixture
def sample_hcl_file(tmp_path):
    hcl_content = """
    key1 = "value1"
    key2 = "value2"
    """
    file_path = tmp_path / "sample.hcl"
    with open(file_path, "w", encoding="UTF-8") as file_handler:
        file_handler.write(hcl_content)
    return file_path



