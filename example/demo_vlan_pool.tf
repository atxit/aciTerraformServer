resource "aci_vlan_pool" "demo-vlan-pool" {
  name  = "demo vlan pool"
  description = "From Terraform"
  alloc_mode  = "static"
  annotation  = "example"
  name_alias  = "example"
}


resource "aci_ranges" "pool-range-10-400" {
  vlan_pool_dn  = aci_vlan_pool.demo-vlan-pool.id
  description   = "From Terraform"
  from          = "vlan-10"
  to            = "vlan-400"
  alloc_mode    = "inherit"
  annotation    = "example"
  name_alias    = "name_alias"
  role          = "external"
}

