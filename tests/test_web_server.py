import os
from pathlib import Path

from unittest.mock import patch, MagicMock
import pandas as pd

from source.web_server import (
    process_table_query_request,
    process_compare_request,
    create_resource_selection,
    create_cfg_collection
)


def open_file(path_to_file):
    with open(path_to_file, "r", encoding="UTF8") as file_open:
        return "".join(map(str, file_open))


def test_return_css_route(client):
    response = client.get("/css/style.css")
    assert response.status_code == 200
    assert (
        open_file(
            str(
                Path(
                    os.path.dirname(os.getcwd()), "source", "static", "css", "style.css"
                )
            )
        )
        in response.data.decode()
    )


def test_return_css_route_nonexistent_file(client):
    response = client.get("/css/nonexistent.css")
    assert response.status_code == 500


def test_return_js_route(client):
    response = client.get("/js/js_draw.js")
    assert response.status_code == 200
    assert (
        open_file(
            str(
                Path(
                    os.path.dirname(os.getcwd()), "source", "static", "js", "js_draw.js"
                )
            )
        )
        in response.data.decode()
    )


def test_return_js_route_nonexistent_file(client):
    response = client.get("/js/nonexistent.js")
    assert response.status_code == 500


def test_get_table_page_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert (
        open_file(
            str(Path(os.path.dirname(os.getcwd()), "source", "templates", "table.html"))
        )
        in response.data.decode()
    )

    response = client.get("/table")
    assert response.status_code == 200
    assert (
        open_file(
            str(Path(os.path.dirname(os.getcwd()), "source", "templates", "table.html"))
        )
        in response.data.decode()
    )


def test_post_table_query_route_table(client):
    with patch("source.web_server.process_table_query_request") as mock_mongo_connector:
        mock_mongo_connector.return_value = {"test": "test"}
        response = client.post("/table", json={"search": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"test": "test"}

        response = client.post("/diff", json={"search": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"test": "test"}


def test_process_table_query_request(post_table_html_results, post_table_dict_results):
    with patch("source.web_server.MongoConnector") as mock_mongo_connector:
        mock_mongo_connector.init_client.return_value = {}
        mock_mongo_connector.return_value.search_all_columns_for_item.return_value = (
            pd.DataFrame.from_dict(post_table_dict_results)
        )
        assert post_table_html_results == process_table_query_request(
            "http://127.0.0.1:5020/table", {"search": "aci_aaep_to_domain"}
        )
        mock_mongo_connector.return_value.search_all_columns_for_item.return_value = {}
        assert {
            "error": True,
            "errorMsg": "no results found",
        } == process_table_query_request(
            "http://127.0.0.1:5020/table", {"search": "ttt"}
        )
        mock_mongo_connector.return_value.search_all_columns_for_item.return_value = (
            pd.DataFrame.from_dict(post_table_dict_results)
        )
        assert post_table_html_results == process_table_query_request(
            "http://127.0.0.1:5020/diff", {"search": "aci_aaep_to_domain"}
        )
        mock_mongo_connector.return_value.search_all_columns_for_item.return_value = {}
        assert {
            "error": True,
            "errorMsg": "no results found",
        } == process_table_query_request(
            "http://127.0.0.1:5020/diff", {"search": "ttt"}
        )


def test_get_draw_page(client):
    with patch(
        "source.web_server.create_resource_selection"
    ) as mock_create_resource_selection:
        mock_create_resource_selection.return_value = ""
        response = client.get("/draw")
        assert response.status_code == 200


def test_post_draw_page(client):
    with patch("source.web_server.TfDraw") as tf_draw:
        tf_draw.return_value.main.return_value = (["www"], ["sss"])
        response = client.post("/draw", json={"resource": "test"})
        assert response.status_code == 200
        assert response.get_json() == {
            "error": False,
            "data": {"nodes": ["www"], "edges": ["sss"]},
        }


def test_get_diff_page(client):
    response = client.get("diff")
    assert response.status_code == 200
    assert (
        open_file(
            str(Path(os.path.dirname(os.getcwd()), "source", "templates", "diff.html"))
        )
        in response.data.decode()
    )


def test_get_import_page(client):
    with patch("source.web_server.MongoConnector") as mock_mongo_connector:
        mock_mongo_connector.init_client.return_value = {}
        mock_mongo_connector.return_value.return_value_from_table.return_value = (
            "/path/to/somewhere"
        )
        response = client.get("import")
        assert response.status_code == 200
        assert (
            open_file(
                str(
                    Path(
                        os.path.dirname(os.getcwd()),
                        "source",
                        "templates",
                        "import.html",
                    )
                )
            ).replace("{{ absolute_path }}", "/path/to/somewhere")
            in response.data.decode()
        )


def test_post_import_page_test_one(client):
    with patch("source.web_server.ImportTfFiles") as import_tf_files:
        import_tf_files.return_value.main.return_value = (True, "test")
        response = client.post("/import", json={"path": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"error": True, "errorMsg": "test"}


def test_post_import_page_test_two(client):
    with patch("source.web_server.ImportTfFiles") as import_tf_files:
        with patch("source.web_server.MongoConnector") as mock_mongo_connector:
            mock_mongo_connector.return_value = MagicMock()
            mock_mongo_connector.return_value.insert_single_value.return_value = (
                "/path/to/somewhere"
            )
            import_tf_files.return_value.main.return_value = (False, "test")
            response = client.post("/import", json={"path": "test"})
            assert response.status_code == 200
            assert response.get_json() == {"error": False, "data": "successful import"}


def test_get_compare_page(client):
    response = client.get("compare")
    assert response.status_code == 200
    assert (
        open_file(
            str(
                Path(
                    os.path.dirname(os.getcwd()), "source", "templates", "compare.html"
                )
            )
        )
        in response.data.decode()
    )


def test_post_compare_page(client):
    with patch("source.web_server.process_compare_request") as process_compare_request:
        process_compare_request.return_value = {"test": "test"}
        response = client.post("/compare", json={"test": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"test": "test"}


def test_process_compare_request_test_one():
    with patch("source.web_server.ImportTfFiles") as import_tf_files:
        import_tf_files.return_value = MagicMock()
        import_tf_files.return_value.main.return_value = (True, "error")
        assert {"error": True, "errorMsg": "error"} == process_compare_request({})


def test_process_compare_request_test_two(
    post_table_dict_results, post_table_html_results
):
    with patch("source.web_server.ImportTfFiles") as import_tf_files:
        import_tf_files.return_value = MagicMock()
        import_tf_files.return_value.main.return_value = (
            False,
            pd.DataFrame.from_dict(post_table_dict_results),
        )
        assert post_table_html_results == process_compare_request({})


def test_create_resource_selection_test_one(client):
    with patch("source.web_server.MongoConnector") as mock_mongo_connector:
        mock_mongo_connector.init_client.return_value = {}
        mock_mongo_connector.return_value.return_distinct_values_of_column.return_value = [
            "a",
            "b",
            "c",
            "N/A",
            "failed to import",
        ]
        assert create_resource_selection() == (
            ' <label for="resourceId">Select a Resource ID:</label>\n'
            '                    <select id="resourceId" '
            'onchange="drawDeps(this)"><option value=""></option><option '
            'value="a">a</option><option value="b">b</option><option '
            'value="c">c</option></select>'
        )


def test_create_resource_selection_test_two(client):
    with patch("source.web_server.MongoConnector") as mock_mongo_connector:
        mock_mongo_connector.init_client.return_value = {}
        mock_mongo_connector.return_value.return_distinct_values_of_column.return_value = (
            []
        )
        assert create_resource_selection() == (
            ' <label for="resourceId">Select a Resource ID:</label>\n'
            '                    <select id="resourceId" '
            'onchange="drawDeps(this)"></select>'
        )


def test_create_cfg_collection():
    with patch("source.web_server.MongoConnector") as mock_mongo_connector:
        mock_mongo_connector.init_client.return_value = {}
        mock_mongo_connector.return_value.return_full_collection.return_value = {}
        create_cfg_collection()
