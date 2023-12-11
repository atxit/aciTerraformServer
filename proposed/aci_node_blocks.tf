resource "aci_node_block" "node-101" {
  switch_association_dn   = aci_leaf_selector.leaf-selector.id
  name                    = "node-101"
  annotation              = "node-101"
  description             = "from terraform"
  from_                   = "101"
  name_alias              = ""
  to_                     = "101"
}

resource "aci_node_block" "node-102" {
  switch_association_dn   = aci_leaf_selector.leaf-selector.id
  name                    = "node-102"
  annotation              = ""
  description             = "from terraform"
  from_                   = "102"
  name_alias              = ""
  to_                     = "102"
}

resource "aci_node_block" "node-103" {
  switch_association_dn   = aci_leaf_selector.leaf-selector.id
  name                    = "node-103"
  annotation              = ""
  description             = "from terraform"
  from_                   = "103"
  name_alias              = ""
  to_                     = "103"
}



