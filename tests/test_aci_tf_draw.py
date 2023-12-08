from unittest.mock import patch, MagicMock

import pandas as pd

from source.aci_tf_draw import TfDraw


@patch("source.import_aci_tf.MongoConnector")
def test_fetch_tf_collection(patched_mongo, return_df_tf_draw):
    patched_mongo.return_full_collection.return_value = return_df_tf_draw
    tf_draw = TfDraw(search_resource="resource.test.id")
    tf_draw.fetch_tf_collection()


def test_located_searched_item(return_df_tf_draw, df_results_dict):
    tf_draw = TfDraw(search_resource="aci_vrf.demo-VRF.id")
    tf_draw.df_root = pd.DataFrame.from_dict(return_df_tf_draw)
    tf_draw.located_searched_item()
    assert tf_draw.df_results.to_dict() == df_results_dict


def test_create_network_x_node_ids():
    tf_draw = TfDraw(search_resource="aci_vrf.demo-VRF.id")
    tf_draw.df_results = pd.DataFrame.from_dict(
        {0: {1: "aci_tenant.demo-test.id"}, 1: {1: "aci_vrf.demo-VRF.id"}}
    )
    results = tf_draw.create_network_x_node_ids()
    assert results == [
        {
            "color": "#97c2fc",
            "id": "aci_tenant.demo-test.id",
            "label": "aci_tenant.demo-test.id",
            "shape": "dot",
            "size": 10,
        },
        {
            "color": "#96CEB4",
            "id": "aci_vrf.demo-VRF.id",
            "label": "aci_vrf.demo-VRF.id",
            "shape": "dot",
            "size": 10,
        },
    ]


def test_create_network_x_edge_ids():
    tf_draw = TfDraw(search_resource="aci_vrf.demo-VRF.id")
    tf_draw.df_results = pd.DataFrame.from_dict(
        {0: {1: "aci_tenant.demo-test.id"}, 1: {1: "aci_vrf.demo-VRF.id"}}
    )
    results = tf_draw.create_network_x_edge_ids()
    assert results == [
        {"from": "aci_vrf.demo-VRF.id", "to": "aci_tenant.demo-test.id", "width": 1}
    ]


def test_create_network_x_edge_ids_reserve():
    tf_draw = TfDraw(search_resource="aci_vrf.demo-VRF.id")
    tf_draw.df_results = pd.DataFrame.from_dict(
        {1: {1: "aci_tenant.demo-test.id"}, 0: {1: "aci_vrf.demo-VRF.id"}}
    )
    results = tf_draw.create_network_x_edge_ids()
    assert results == [
        {"from": "aci_vrf.demo-VRF.id", "to": "aci_tenant.demo-test.id", "width": 1}
    ]


def test_main():
    tf_draw = TfDraw(search_resource="aci_vrf.demo-VRF.id")
    tf_draw.fetch_tf_collection = MagicMock()
    tf_draw.located_searched_item = MagicMock()
    mock_create_network_x_node_ids = tf_draw.create_network_x_node_ids = MagicMock()
    mock_create_network_x_node_ids.return_value = ["test"]
    mock_create_network_x_edge_ids = tf_draw.create_network_x_edge_ids = MagicMock()
    mock_create_network_x_edge_ids.return_value = ["test"]
    node_id_list, edge_id_list = tf_draw.main()
    assert node_id_list == ["test"]
    assert edge_id_list == ["test"]
