resource "aci_tenant" "demo-test" {
  name        = "demo_tenant"
  description = "from terraform"
  annotation  = "tag1"
  name_alias  = local.demo-tenant
}

