"""
ACI TF Draw is responsible for generating the interdependencies table. Next, the code
 will identify paths which match the user input selection. Lastly, the code will generate a
 node and edge array used by the front end to generate the diagram.
"""
import pandas as pd
import numpy as np

from source.mongo_connect import MongoConnector


class TfDraw:
    """
    The drawing class
    """

    def __init__(self, search_resource):
        self.search_resource = search_resource
        self.df_results = pd.DataFrame()
        self.df_root = pd.DataFrame()

    def fetch_tf_collection(self):
        """
        Builds a table which contains the TF resource dependencies
        :return:
        """
        mongo_conn = MongoConnector()
        mongo_conn.init_client(collection_name="aciTfCollection")
        df_tf = mongo_conn.return_full_collection()
        df_tf = df_tf.loc[~df_tf["resourceId"].str.match("N/A")].copy()
        df_deps = df_tf.loc[df_tf["resourceValue"].str.contains(r".id$")].copy()
        for resource_type in df_deps["resourceType"]:
            df_tf = df_tf.loc[~df_tf["resourceType"].str.match(resource_type)].copy()

        self.df_root = df_tf[["resourceId"]].drop_duplicates().copy()
        df_deps = df_deps[["resourceId", "resourceValue"]].copy()
        column_ref = 0
        self.df_root.rename(columns={"resourceId": column_ref}, inplace=True)
        df_deps.rename(columns={"resourceValue": column_ref}, inplace=True)
        self.df_root = self.df_root.merge(
            df_deps, left_on=column_ref, right_on=column_ref, how="inner"
        )
        self.df_root.rename(columns={"resourceId": column_ref + 1}, inplace=True)
        df_deps.rename(columns={column_ref: column_ref + 1}, inplace=True)
        column_ref += 1
        continue_processing = True

        while continue_processing:
            current_shape = self.df_root.shape
            self.df_root = self.df_root.merge(
                df_deps, left_on=column_ref, right_on=column_ref, how="outer"
            ).dropna(subset=[column_ref - 1])
            self.df_root.rename(columns={"resourceId": column_ref + 1}, inplace=True)
            df_deps.rename(columns={column_ref: column_ref + 1}, inplace=True)
            self.df_root.dropna(how="all", axis=1, inplace=True)
            self.df_root.fillna("", inplace=True)
            column_ref += 1
            if current_shape == self.df_root.shape:
                continue_processing = False
        print(df_deps)

    def located_searched_item(self):
        """
        filters the dependencies table using the users input (search_resource)
        :return:
        """
        remove_list = []
        searching = True
        for column_id in self.df_root.columns:
            df_column = self.df_root.loc[
                self.df_root[column_id].str.contains(self.search_resource)
            ].copy()
            if len(df_column) == 0 and searching:
                remove_list.append(column_id)
            else:
                searching = False
                self.df_results = pd.concat([self.df_results, df_column])
        self.df_results = (
            self.df_results.replace("", np.nan).dropna(axis=1, how="all").fillna("")
        )
        self.df_results.index = np.arange(1, len(self.df_results) + 1)
        # print(self.df_results)

    def create_network_x_node_ids(self):
        """
        :return: the node list used by the front end to generate the diagram
        """
        node_id_list = []
        for i in self.df_results.index:
            for c in self.df_results.columns:
                if (
                    self.df_results.at[i, c] != ""
                    and self.df_results.at[i, c] not in node_id_list
                ):
                    node_id_list.append(self.df_results.at[i, c])

        node_list = []
        for node_id in node_id_list:
            if self.search_resource == node_id:
                color = "#96CEB4"
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

    def create_network_x_edge_ids(self):
        """
        the edge list used by the front end to generate the diagram
        :return: edge list [{'from' : 'x', 'to' : 'y'},{'from' : 'y', 'to' : 'z'}]
        """
        edge_id_list = []
        for i in self.df_results.index:
            for c in self.df_results.columns:
                try:
                    if (
                        self.df_results.at[i, c] != ""
                        and self.df_results.at[i, c + 1] != ""
                        and ":".join(
                            (self.df_results.at[i, c], self.df_results.at[i, c + 1])
                        )
                        not in edge_id_list
                    ):
                        edge_id_list.append(
                            ":".join(
                                (self.df_results.at[i, c], self.df_results.at[i, c + 1])
                            )
                        )
                except KeyError:
                    pass

        edge_list = []
        for edge_ids in edge_id_list:
            if self.search_resource == edge_ids.split(":")[1]:
                edge_id_from = edge_ids.split(":")[1]
                edge_id_to = edge_ids.split(":")[0]
            else:
                edge_id_from = edge_ids.split(":")[0]
                edge_id_to = edge_ids.split(":")[1]
            edge_list.append({"from": edge_id_from, "to": edge_id_to, "width": 1})
        return edge_list

    def main(self):
        """
        Main execution block
        :return: node and edge lists (arrays)
        """
        self.fetch_tf_collection()
        self.located_searched_item()
        return self.create_network_x_node_ids(), self.create_network_x_edge_ids()
