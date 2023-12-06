from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    redirect,
    url_for,
    session,
)

import urllib3
import json
from pathlib import Path
import os

from source.mongo_connect import MongoConnector
from source.constants import *

urllib3.disable_warnings()

def open_file():
    with open(str(Path(os.environ.get("PYTHONPATH"), 'source', 'templates','test.html')), "r") as file_fh:
        return ''.join(map(str,file_fh.readlines()))



app = Flask(__name__)

#edges = [{"from": "r1", "to": "r4", "width": 1}, {"from": "r1", "to": "r4", "width": 1}, {"from": "r2", "to": "r3", "width": 1}, {"from": "r2", "to": "r5", "width": 1}, {"from": "r3", "to": "r4", "width": 1}, {"from": "r4", "to": "r5", "width": 1}, {"from": 20, "to": 21, "width": 5}]
#nodes = [{"color": "#97c2fc", "id": "r1", "label": "r1", "shape": "dot", "size": 10}, {"color": "#97c2fc", "id": "r2", "label": "r2", "shape": "dot", "size": 10}, {"color": "#97c2fc", "id": "r3", "label": "r3", "shape": "dot", "size": 10}, {"color": "#97c2fc", "id": "r5", "label": "r5", "shape": "dot", "size": 10}, {"color": "#97c2fc", "id": "r4", "label": "r4", "shape": "dot", "size": 10}, {"group": 2, "id": 20, "label": 20, "shape": "dot", "size": 20, "title": "couple"}, {"group": 2, "id": 21, "label": 21, "shape": "dot", "size": 15, "title": "couple"}, {"group": 3, "id": 25, "label": "lonely", "shape": "dot", "size": 25, "title": "lonely node"}]
#edges = [{'from': 'aci_tenant.demo-test.id', 'to': 'aci_vrf.demo-VRF.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_bridge_domain.demo-app-bd.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_application_epg.demo-app.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'width': 1}, {'from': 'aci_tenant.demo-test.id', 'to': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'width': 1}, {'from': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'to': 'aci_vrf.demo-VRF.id', 'width': 1}]
#edges = [{'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_tenant.demo-test.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_bridge_domain.demo-app-bd.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_application_epg.demo-app.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'width': 1}, {'from': 'aci_tenant.demo-test.id', 'to': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'width': 1}]
edges = [{'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_tenant.demo-test.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_bridge_domain.demo-app-bd.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'width': 1}, {'from': 'aci_bridge_domain.demo-app-bd.id', 'to': 'aci_application_epg.demo-app.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'width': 1}, {'from': 'aci_application_epg.demo-app.id', 'to': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'width': 1}, {'from': 'aci_tenant.demo-test.id', 'to': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'width': 1}, {'from': 'aci_vrf.demo-VRF.id', 'to': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'width': 1}]

#nodes =[{'color': '#97c2fc', 'id': 'aci_tenant.demo-test.id', 'label': 'aci_tenant.demo-test.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_vrf.demo-VRF.id', 'label': 'aci_vrf.demo-VRF.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'label': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_bridge_domain.demo-app-bd.id', 'label': 'aci_bridge_domain.demo-app-bd.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'label': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_application_epg.demo-app.id', 'label': 'aci_application_epg.demo-app.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'label': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'label': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'label': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'shape': 'dot', 'size': 10}]
nodes = [{'color': '#97c2fc', 'id': 'aci_tenant.demo-test.id', 'label': 'aci_tenant.demo-test.id', 'shape': 'dot', 'size': 10}, {'color': '#FF5349', 'id': 'aci_vrf.demo-VRF.id', 'label': 'aci_vrf.demo-VRF.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'label': 'aci_vrf_to_bgp_address_family_context.vrf-to-bgp-family-example.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_bridge_domain.demo-app-bd.id', 'label': 'aci_bridge_domain.demo-app-bd.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'label': 'aci_subnet.SUBNET-10-10-10-1-24.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_application_epg.demo-app.id', 'label': 'aci_application_epg.demo-app.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'label': 'aci_epg_to_static_path.path-129-1-3-999-r.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'label': 'aci_epg_to_static_path.path-129-1-3-1000-r.id', 'shape': 'dot', 'size': 10}, {'color': '#97c2fc', 'id': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'label': 'aci_bgp_address_family_context.bgp-family-context-example.id', 'shape': 'dot', 'size': 10}]


@app.route("/testDiagram", methods=["GET"])
def landing_page():
    return open_file().replace('{{edges}}',json.dumps(edges)).replace('{{nodes}}',json.dumps(nodes))


@app.route("/css/<path:path>", methods=["GET"])
def return_css(path):
    return send_file(f"static/css/{path}")


@app.route("/js/<path:path>", methods=["GET"])
def return_js(path):
    return send_file(f"static/js/{path}")


@app.route("/", methods=["GET"])
@app.route("/table", methods=["GET"])
def get_table_page():
    return render_template('table.html')


@app.route("/table", methods=["POST"])
def post_table_page():
    resp_dict = {}
    mongo_conn = MongoConnector()
    mongo_conn.init_client('aciTfCollection')
    df_results = mongo_conn.search_all_columns_for_item(request.get_json().get('search'))
    if len(df_results) > 0:
        resp_dict.update({'error': False, 'data': df_results.to_html(
                index=False, border=1, table_id="response-table", justify="center", classes='data-table')})
    else:
        resp_dict.update({'error': True, 'errorMsg': 'no results found'})
    return jsonify(resp_dict)

from source.acf_tf_draw import fetch_tf_collection

@app.route("/draw", methods=["GET"])
def get_draw_page():
    mongo_conn = MongoConnector()
    mongo_conn.init_client('aciTfCollection')
    print(mongo_conn.return_distinct_values_of_column('resourceId'))
    df_deps, _ = fetch_tf_collection()

    return render_template('draw.html')



if __name__ == "__main__":
    app.run(use_reloader=False, port=5020, debug=True, host="0.0.0.0")

