import pytest
from source.web_server import app


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
    yield {'file': {1: 'test'}, 'resourceType': {1: 'failed to import'}, 'resourceId': {1: 'failed to import'}, 'resourceKey': {1: 'failed to import'}, 'resourceValue': {1: 'failed to import'}}


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
