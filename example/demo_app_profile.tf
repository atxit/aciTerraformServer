resource "aci_application_profile" "demo-app-profile" {
  tenant_dn  = aci_tenant.demo-test.id
  name       = "demo_app_profile"
  annotation = "tag"
  description = "from terraform"
  prio       = "level1"
}