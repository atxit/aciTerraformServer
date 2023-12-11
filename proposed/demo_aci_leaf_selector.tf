resource "aci_leaf_selector" "leaf-selector" {
  leaf_profile_dn         = aci_leaf_profile.leaf-profile.id
  name                    = "example_leaf_selector"
  switch_association_type = "range"
  annotation              = "orchestrator:terraform"
  description             = "from terraform"
  name_alias              = "tag_leaf_selector"
}

resource "aci_leaf_profile" "leaf-profile" {
  name        = "leaf"
  description  = "From Terraform"
  annotation  = "example"
  name_alias  = "example"
  leaf_selector {
    name                    = "one"
    switch_association_type = "range"
    node_block {
      name  = "blk1"
      from_ = "101"
      to_   = "102"
    }
    node_block {
      name  = "blk2"
      from_ = "103"
      to_   = "104"
    }
  }
}