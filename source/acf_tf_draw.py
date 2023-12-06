import pandas as pd
import numpy as np

from source.mongo_connect import MongoConnector


class TfDraw:
    def __init__(self, search_resource):
        self.search_resource = search_resource

    @staticmethod
    def fetch_tf_collection():
        mongo_conn = MongoConnector()
        mongo_conn.init_client(collection_name="aciTfCollection")
        df_tf = mongo_conn.return_full_collection()
        df_tf = df_tf.loc[~df_tf["resourceId"].str.match("N/A")].copy()
        df_deps = df_tf.loc[df_tf["resourceValue"].str.contains(r".id$")].copy()
        for resource_type in df_deps["resourceType"]:
            df_tf = df_tf.loc[~df_tf["resourceType"].str.match(resource_type)].copy()
            #
        df_root = df_tf[["resourceId"]].drop_duplicates().copy()
        df_deps = df_deps[["resourceId", "resourceValue"]].copy()
        column_ref = 0
        df_root.rename(columns={"resourceId": column_ref}, inplace=True)
        df_deps.rename(columns={"resourceValue": column_ref}, inplace=True)
        df_root = df_root.merge(
            df_deps, left_on=column_ref, right_on=column_ref, how="inner"
        )
        df_root.rename(columns={"resourceId": column_ref + 1}, inplace=True)
        df_deps.rename(columns={column_ref: column_ref + 1}, inplace=True)
        column_ref += 1
        continue_processing = True
        #
        while continue_processing:
            current_shape = df_root.shape
            df_root = df_root.merge(
                df_deps, left_on=column_ref, right_on=column_ref, how="outer"
            ).dropna(subset=[column_ref - 1])
            df_root.rename(columns={"resourceId": column_ref + 1}, inplace=True)
            df_deps.rename(columns={column_ref: column_ref + 1}, inplace=True)
            df_root.dropna(how="all", axis=1, inplace=True)
            df_root.fillna("", inplace=True)
            column_ref += 1
            if current_shape == df_root.shape:
                continue_processing = False
        return df_root


    def located_searched_item(self, df_root, resource_lookup):
        df_results = pd.DataFrame()
        remove_list = []
        searching = True
        for column_id in df_root.columns:
            df_column = df_root.loc[df_root[column_id].str.contains(resource_lookup)].copy()
            if len(df_column) == 0 and searching:
                remove_list.append(column_id)
            else:
                searching = False
                df_results = pd.concat([df_results, df_column])
        df_results = df_results.replace("", np.nan).dropna(axis=1, how="all").fillna("")
        df_results.index = np.arange(1, len(df_results) + 1)
        return df_results


def create_network_x_node_ids(df_paths):
    node_id_list = []
    for i in df_paths.index:
        for c in df_paths.columns:
            if df_paths.at[i, c] != "" and df_paths.at[i, c] not in node_id_list:
                node_id_list.append(df_paths.at[i, c])
    #
    node_list = []
    for node_id in node_id_list:
        if resource_lookup == node_id:
            color = "#FF5349"
        else:
            color = "#97c2fc"
        node_list.append(
            {
                "color": color,
                "id": node_id,
                "label": node_id,
                "shape": "dot",
                "size": 10,
            }
        )
    return node_list


def create_network_x_edge_ids(df_paths):
    edge_id_list = []
    for i in df_paths.index:
        for c in df_paths.columns:
            try:
                if (
                    df_paths.at[i, c] != ""
                    and df_paths.at[i, c + 1] != ""
                    and ":".join((df_paths.at[i, c], df_paths.at[i, c + 1]))
                    not in edge_id_list
                ):
                    edge_id_list.append(
                        ":".join((df_paths.at[i, c], df_paths.at[i, c + 1]))
                    )
            except KeyError:
                pass
    #
    edge_list = []
    for edge_ids in edge_id_list:
        if resource_lookup == edge_ids.split(":")[1]:
            edge_id_from = edge_ids.split(":")[1]
            edge_id_to = edge_ids.split(":")[0]
        else:
            edge_id_from = edge_ids.split(":")[0]
            edge_id_to = edge_ids.split(":")[1]
        edge_list.append({"from": edge_id_from, "to": edge_id_to, "width": 1})
    return edge_list


resource_lookup = "aci_vrf.demo-VRF.id"
df_root = fetch_tf_collection()
df_paths = located_searched_item(df_root, resource_lookup)
node_list = create_network_x_node_ids(df_paths)
edge_list = create_network_x_edge_ids(df_paths)
