resource "aci_tenant" "demo-test" {
  name        = "demo_tenant"
  description = "from terraform"
  annotation  = "tag"
  name_alias  = local.demo-tenant
}

