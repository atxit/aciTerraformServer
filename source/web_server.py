"""
ACI TF Web Services, responsible for serving HTML, JS, CSS and responding to API calls.
"""
import os
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file

from markupsafe import Markup

from source.mongo_connect import MongoConnector
from source.aci_tf_draw import TfDraw
from source.import_aci_tf import ImportTfFiles

app = Flask(__name__)


path_short_cut = {
    "example": str(Path(os.environ["PYTHONPATH"], "example")),
    "proposed": str(Path(os.environ["PYTHONPATH"], "proposed")),
}


@app.route("/css/<path:path>", methods=["GET"])
def return_css(path):
    """
    Serves CSS
    :param path: URL Path
    :return: CSS File
    """
    return send_file(f"static/css/{path}")


@app.route("/js/<path:path>", methods=["GET"])
def return_js(path):
    """
    Serves JS
    :param path: URL Path
    :return: JS File
    """
    return send_file(f"static/js/{path}")


@app.route("/acitfserver", methods=["GET"])
@app.route("/table", methods=["GET"])
def get_table_page():
    """
    :return: table HTML page
    """
    return render_template("table.html")


@app.route("/diff", methods=["POST"])
@app.route("/table", methods=["POST"])
def post_table_query():
    """
    API receiver, responds to API requests to the diff and table flask routes
    searches table, returns matches and creates HTML table
    :return: JSON
    """
    return jsonify(process_table_query_request(request.url, request.get_json()))


@app.route("/draw", methods=["GET"])
def get_draw_page():
    """
    :return: Draw HTML
    """
    test = Markup(create_resource_selection())
    return render_template("draw.html", resource_selection=test)


@app.route("/draw", methods=["POST"])
def post_draw_page():
    """
    API receiver, responds to API requests to the draw flask route
    request node and edge list which is used to create the JS diagram
    :return: JSON
    """
    tf_draw = TfDraw(request.get_json().get("resource"))
    node_list, edge_list = tf_draw.main()
    return jsonify({"error": False, "data": {"nodes": node_list, "edges": edge_list}})


@app.route("/diff", methods=["GET"])
def get_diff_page():
    """
    :return: diff HTML
    """
    return render_template("diff.html")


@app.route("/import", methods=["GET"])
def get_import_page():
    """
    :return: import HTML
    """
    mongo_cfg_conn = MongoConnector()
    mongo_cfg_conn.init_client("aciTfCfg")
    return render_template(
        "import.html",
        absolute_path=mongo_cfg_conn.return_value_from_table(
            searched_column="key", find_key="path", return_value_in="value"
        ),
    )


@app.route("/import", methods=["POST"])
def post_import_page():
    """
    :return: import HTML
    """
    import_tf_files = ImportTfFiles(
        file_location=path_short_cut.get(
            request.get_json().get("path"), request.get_json().get("path")
        )
    )
    error, error_msg = import_tf_files.main()

    if error:
        return jsonify({"error": error, "errorMsg": error_msg})

    mongo_cfg_conn = MongoConnector()
    mongo_cfg_conn.init_client("aciTfCfg")
    mongo_cfg_conn.insert_single_value(
        search_column="key",
        search_value="path",
        update_column="value",
        updated_value=request.get_json().get("path"),
    )

    return jsonify({"error": error, "data": "successful import"})


@app.route("/compare", methods=["GET"])
def get_compare_page():
    """
    :return: diff HTML
    """
    return render_template("compare.html")


@app.route("/compare", methods=["POST"])
def post_compare_query():
    """
    API receiver, responds to API requests to the diff and table flask routes
    searches table, returns matches and creates HTML table
    :return: JSON
    """
    return jsonify(process_compare_request(request.get_json()))


def process_compare_request(request_json):
    """
    creates an HTML table of the searched results

    :param request_url: the request URL
    :param request_json: JSON payload
    :return: result dict
    """
    resp_dict = {}
    import_tf_files = ImportTfFiles(
        path_short_cut.get(request_json.get("path"), request_json.get("path")),
        return_diff=True,
    )
    error, results = import_tf_files.main()
    if not error:
        resp_dict.update(
            {
                "error": False,
                "data": results.to_html(
                    index=False,
                    border=1,
                    table_id="response-table",
                    justify="center",
                    classes="data-table",
                ),
            }
        )
    else:
        resp_dict.update({"error": True, "errorMsg": results})
    return resp_dict


def process_table_query_request(request_url, request_json):
    """
    creates an HTML table of the searched results

    :param request_url: the request URL
    :param request_json: JSON payload
    :return: result dict
    """
    resp_dict = {}
    mongo_conn = MongoConnector()
    if request_url.split("/")[-1] == "table":
        mongo_conn.init_client("aciTfCollection")
    else:
        mongo_conn.init_client("aciTfCollectionDiff")
    df_results = mongo_conn.search_all_columns_for_item(request_json.get("search"))
    if len(df_results) > 0:
        resp_dict.update(
            {
                "error": False,
                "data": df_results.to_html(
                    index=False,
                    border=1,
                    table_id="response-table",
                    justify="center",
                    classes="data-table",
                ),
            }
        )
    else:
        resp_dict.update({"error": True, "errorMsg": "no results found"})
    return resp_dict


def create_resource_selection():
    """
    Creates the selection input box for the draw diagram
    :return: HTML selection input
    """
    select_str = """ <label for="resourceId">Select a Resource ID:</label>
                    <select id="resourceId" onchange="drawDeps(this)">"""
    mongo_conn = MongoConnector()
    mongo_conn.init_client("aciTfCollection")
    resource_list = mongo_conn.return_distinct_values_of_column("resourceId")
    if len(resource_list) > 0:
        if "N/A" in resource_list:
            resource_list.remove("N/A")
        if "failed to import" in resource_list:
            resource_list.remove("failed to import")
        resource_list.sort()
        resource_list.insert(0, "")
    for resource_id in resource_list:
        select_str += f'<option value="{resource_id}">{resource_id}</option>'
    select_str += "</select>"
    return select_str


def create_cfg_collection():
    """
    builds the cfg collection which is used to save persistent data
    """
    mongo_cfg_conn = MongoConnector()
    mongo_cfg_conn.init_client("aciTfCfg")
    df_cfg = mongo_cfg_conn.return_full_collection()
    if len(df_cfg) == 0:
        df_cfg = pd.DataFrame(columns=["key", "value"], index=[1])
        df_cfg.loc[1, "key"] = "path"
        df_cfg.fillna("", inplace=True)
        mongo_cfg_conn.write_collection(df_db=df_cfg)


if __name__ == "__main__":
    create_cfg_collection()  # pragma: no cover
    app.run(
        use_reloader=False, port=5020, debug=True, host="0.0.0.0"
    )  # pragma: no cover
