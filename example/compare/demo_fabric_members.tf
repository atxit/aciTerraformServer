resource "aci_fabric_node_member" "member-101" {
  name        = "spine-1"
  serial      = "1"
  annotation  = "example"
  description = "from terraform"
  ext_pool_id = "0"
  fabric_id   = "1"
  name_alias  = "example"
  node_id     = "101"
  node_type   = "spine"
  pod_id      = "1"
  role        = "unspecified"
}

resource "aci_fabric_node_member" "member-201" {
  name        = "spine-2"
  serial      = "1"
  annotation  = "example"
  description = "from terraform"
  ext_pool_id = "0"
  fabric_id   = "1"
  name_alias  = "example"
  node_id     = "201"
  node_type   = "spine"
  pod_id      = "1"
  role        = "unspecified"
}
