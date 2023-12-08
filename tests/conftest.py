import pytest
from source.web_server import app
from bson.objectid import ObjectId


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


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def post_table_html_results():
    yield {
        "error": False,
        "data": '<table border="1" class="dataframe data-table" id="response-table">\n  <thead>\n    <tr style="text-align: center;">\n      <th>importTime</th>\n      <th>file</th>\n      <th>resourceType</th>\n      <th>resourceId</th>\n      <th>resourceKey</th>\n      <th>resourceValue</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>2023-12-07 14:19:28 UTC</td>\n      <td>/Users/machine/projects/aciTerraformServer/example/demo_app_profile.tf</td>\n      <td>aci_application_profile</td>\n      <td>aci_application_profile.demo-app-profile.id</td>\n      <td>resource.aci_application_profile.demo-app-profile.tenant_dn</td>\n      <td>aci_tenant.demo-test.id</td>\n    </tr>\n    <tr>\n      <td>2023-12-07 14:19:28 UTC</td>\n      <td>/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf</td>\n      <td>aci_bgp_address_family_context</td>\n      <td>aci_bgp_address_family_context.bgp-family-context-example.id</td>\n      <td>resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn</td>\n      <td>aci_tenant.demo-test.id</td>\n    </tr>\n    <tr>\n      <td>2023-12-07 14:19:28 UTC</td>\n      <td>/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf</td>\n      <td>aci_vrf</td>\n      <td>aci_vrf.demo-VRF.id</td>\n      <td>resource.aci_vrf.demo-VRF.tenant_dn</td>\n      <td>aci_tenant.demo-test.id</td>\n    </tr>\n    <tr>\n      <td>2023-12-07 14:19:28 UTC</td>\n      <td>/Users/machine/projects/aciTerraformServer/example/demo_app_epg.tf</td>\n      <td>aci_bridge_domain</td>\n      <td>aci_bridge_domain.demo-app-bd.id</td>\n      <td>resource.aci_bridge_domain.demo-app-bd.tenant_dn</td>\n      <td>aci_tenant.demo-test.id</td>\n    </tr>\n  </tbody>\n</table>',
    }


@pytest.fixture
def import_hcl_failed_results():
    yield {
        "file": {1: "test"},
        "resourceType": {1: "failed to import"},
        "resourceId": {1: "failed to import"},
        "resourceKey": {1: "failed to import"},
        "resourceValue": {1: "failed to import"},
    }


@pytest.fixture
def post_table_dict_results():
    yield {
        "importTime": {
            0: "2023-12-07 14:19:28 UTC",
            1: "2023-12-07 14:19:28 UTC",
            2: "2023-12-07 14:19:28 UTC",
            3: "2023-12-07 14:19:28 UTC",
        },
        "file": {
            0: "/Users/machine/projects/aciTerraformServer/example/demo_app_profile.tf",
            1: "/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf",
            2: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            3: "/Users/machine/projects/aciTerraformServer/example/demo_app_epg.tf",
        },
        "resourceType": {
            0: "aci_application_profile",
            1: "aci_bgp_address_family_context",
            2: "aci_vrf",
            3: "aci_bridge_domain",
        },
        "resourceId": {
            0: "aci_application_profile.demo-app-profile.id",
            1: "aci_bgp_address_family_context.bgp-family-context-example.id",
            2: "aci_vrf.demo-VRF.id",
            3: "aci_bridge_domain.demo-app-bd.id",
        },
        "resourceKey": {
            0: "resource.aci_application_profile.demo-app-profile.tenant_dn",
            1: "resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn",
            2: "resource.aci_vrf.demo-VRF.tenant_dn",
            3: "resource.aci_bridge_domain.demo-app-bd.tenant_dn",
        },
        "resourceValue": {
            0: "aci_tenant.demo-test.id",
            1: "aci_tenant.demo-test.id",
            2: "aci_tenant.demo-test.id",
            3: "aci_tenant.demo-test.id",
        },
    }


@pytest.fixture
def apply_locals_results():
    yield {
        "file": {
            0: "/Users/machine/projects/aciTerraformServer/example/demo_app_profile.tf",
            1: "/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf",
            2: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            3: "/Users/machine/projects/aciTerraformServer/example/demo_app_epg.tf",
        },
        "importTime": {
            0: "2023-12-07 14:19:28 UTC",
            1: "2023-12-07 14:19:28 UTC",
            2: "2023-12-07 14:19:28 UTC",
            3: "2023-12-07 14:19:28 UTC",
        },
        "resourceId": {
            0: "aci_application_profile.demo-app-profile.id",
            1: "aci_bgp_address_family_context.bgp-family-context-example.id",
            2: "aci_vrf.demo-VRF.id",
            3: "aci_bridge_domain.demo-app-bd.id",
        },
        "resourceKey": {
            0: "resource.aci_application_profile.demo-app-profile.tenant_dn",
            1: "resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn",
            2: "resource.aci_vrf.demo-VRF.tenant_dn",
            3: "resource.aci_bridge_domain.demo-app-bd.tenant_dn",
        },
        "resourceType": {
            0: "aci_application_profile",
            1: "aci_bgp_address_family_context",
            2: "aci_vrf",
            3: "aci_bridge_domain",
        },
        "resourceValue": {0: "changed", 1: "changed", 2: "changed", 3: "changed"},
    }


@pytest.fixture
def write_collection_fixture():
    yield [
        {
            "_id": ObjectId("6572eaf01bc2d4a61510c592"),
            "importTime": 1702030063.941511,
            "file": "/Users/machine/projects/aciTerraformServer/example/aci_bgp_address_family_context.tf",
            "resourceType": "aci_bgp_address_family_context",
            "resourceId": "aci_bgp_address_family_context.bgp-family-context-example.id",
            "resourceKey": "resource.aci_bgp_address_family_context.bgp-family-context-example.tenant_dn",
            "resourceValue": "aci_tenant.demo-test.id",
        }
    ]


@pytest.fixture
def return_value_from_table_fixture():
    yield [
        {
            "_id": ObjectId("6571d0c0d8901a5373642f9a"),
            "key": "path",
            "value": "/Users/machine/projects/aciTerraformServer/example",
        }
    ]


@pytest.fixture
def return_df_tf_draw():
    yield {
        "file": {
            0: "/Users/machine/projects/aciTerraformServer/example/test_tenant.tf",
            1: "/Users/machine/projects/aciTerraformServer/example/test_tenant.tf",
            2: "/Users/machine/projects/aciTerraformServer/example/test_tenant.tf",
            3: "/Users/machine/projects/aciTerraformServer/example/test_tenant.tf",
            4: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            5: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            6: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            7: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            8: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            9: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            10: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            11: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            12: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            13: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            14: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            15: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
        },
        "resourceType": {
            0: "aci_tenant",
            1: "aci_tenant",
            2: "aci_tenant",
            3: "aci_tenant",
            4: "aci_vrf",
            5: "aci_vrf",
            6: "aci_vrf",
            7: "aci_vrf",
            8: "aci_vrf",
            9: "aci_vrf",
            10: "aci_vrf",
            11: "aci_vrf",
            12: "aci_vrf",
            13: "aci_vrf",
            14: "aci_vrf",
            15: "aci_vrf",
        },
        "resourceId": {
            0: "aci_tenant.demo-test.id",
            1: "aci_tenant.demo-test.id",
            2: "aci_tenant.demo-test.id",
            3: "aci_tenant.demo-test.id",
            4: "aci_vrf.demo-VRF.id",
            5: "aci_vrf.demo-VRF.id",
            6: "aci_vrf.demo-VRF.id",
            7: "aci_vrf.demo-VRF.id",
            8: "aci_vrf.demo-VRF.id",
            9: "aci_vrf.demo-VRF.id",
            10: "aci_vrf.demo-VRF.id",
            11: "aci_vrf.demo-VRF.id",
            12: "aci_vrf.demo-VRF.id",
            13: "aci_vrf.demo-VRF.id",
            14: "aci_vrf.demo-VRF.id",
            15: "aci_vrf.demo-VRF.id",
        },
        "resourceKey": {
            0: "resource.aci_tenant.demo-test.name",
            1: "resource.aci_tenant.demo-test.description",
            2: "resource.aci_tenant.demo-test.annotation",
            3: "resource.aci_tenant.demo-test.name_alias",
            4: "resource.aci_vrf.demo-VRF.tenant_dn",
            5: "resource.aci_vrf.demo-VRF.name",
            6: "resource.aci_vrf.demo-VRF.description",
            7: "resource.aci_vrf.demo-VRF.annotation",
            8: "resource.aci_vrf.demo-VRF.bd_enforced_enable",
            9: "resource.aci_vrf.demo-VRF.ip_data_plane_learning",
            10: "resource.aci_vrf.demo-VRF.knw_mcast_act",
            11: "resource.aci_vrf.demo-VRF.name_alias",
            12: "resource.aci_vrf.demo-VRF.pc_enf_dir",
            13: "resource.aci_vrf.demo-VRF.pc_enf_pref",
            14: "resource.aci_vrf.demo-VRF.relation_fv_rs_ctx_to_bgp_ctx_af_pol.af",
            15: "resource.aci_vrf.demo-VRF.relation_fv_rs_ctx_to_bgp_ctx_af_pol.tn_bgp_ctx_af_pol_name",
        },
        "resourceValue": {
            0: "demo_tenant",
            1: "from terraform",
            2: "tag1",
            3: "local.demo-tenant",
            4: "aci_tenant.demo-test.id",
            5: "demo_vrf",
            6: "from terraform",
            7: "tag_vrf",
            8: "no",
            9: "enabled",
            10: "deny",
            11: "alias_vrf",
            12: "ingress",
            13: "unenforced",
            14: "ipv4-ucast",
            15: "aci_bgp_address_family_context.bgp-family-context-example.id",
        },
    }


@pytest.fixture
def df_results_dict():
    yield {
        "file": {
            1: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            2: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            3: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            4: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            5: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            6: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            7: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            8: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            9: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            10: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            11: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
            12: "/Users/machine/projects/aciTerraformServer/example/aci_vrf_demo.tf",
        },
        "resourceId": {
            1: "aci_vrf.demo-VRF.id",
            2: "aci_vrf.demo-VRF.id",
            3: "aci_vrf.demo-VRF.id",
            4: "aci_vrf.demo-VRF.id",
            5: "aci_vrf.demo-VRF.id",
            6: "aci_vrf.demo-VRF.id",
            7: "aci_vrf.demo-VRF.id",
            8: "aci_vrf.demo-VRF.id",
            9: "aci_vrf.demo-VRF.id",
            10: "aci_vrf.demo-VRF.id",
            11: "aci_vrf.demo-VRF.id",
            12: "aci_vrf.demo-VRF.id",
        },
        "resourceKey": {
            1: "resource.aci_vrf.demo-VRF.tenant_dn",
            2: "resource.aci_vrf.demo-VRF.name",
            3: "resource.aci_vrf.demo-VRF.description",
            4: "resource.aci_vrf.demo-VRF.annotation",
            5: "resource.aci_vrf.demo-VRF.bd_enforced_enable",
            6: "resource.aci_vrf.demo-VRF.ip_data_plane_learning",
            7: "resource.aci_vrf.demo-VRF.knw_mcast_act",
            8: "resource.aci_vrf.demo-VRF.name_alias",
            9: "resource.aci_vrf.demo-VRF.pc_enf_dir",
            10: "resource.aci_vrf.demo-VRF.pc_enf_pref",
            11: "resource.aci_vrf.demo-VRF.relation_fv_rs_ctx_to_bgp_ctx_af_pol.af",
            12: "resource.aci_vrf.demo-VRF.relation_fv_rs_ctx_to_bgp_ctx_af_pol.tn_bgp_ctx_af_pol_name",
        },
        "resourceType": {
            1: "aci_vrf",
            2: "aci_vrf",
            3: "aci_vrf",
            4: "aci_vrf",
            5: "aci_vrf",
            6: "aci_vrf",
            7: "aci_vrf",
            8: "aci_vrf",
            9: "aci_vrf",
            10: "aci_vrf",
            11: "aci_vrf",
            12: "aci_vrf",
        },
        "resourceValue": {
            1: "aci_tenant.demo-test.id",
            2: "demo_vrf",
            3: "from terraform",
            4: "tag_vrf",
            5: "no",
            6: "enabled",
            7: "deny",
            8: "alias_vrf",
            9: "ingress",
            10: "unenforced",
            11: "ipv4-ucast",
            12: "aci_bgp_address_family_context.bgp-family-context-example.id",
        },
    }
