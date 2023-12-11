resource "aci_aaep_to_domain" "foo_aaep_to_domain" {
  attachable_access_entity_profile_dn = aci_attachable_access_entity_profile.demo-aaep-profile.id
  domain_dn                           = aci_l3_domain_profile.demo-domain-profile.id
}

resource "aci_attachable_access_entity_profile" "demo-aaep-profile" {
  description = "AAEP description"
  name        = "demo_entity_prof"
  annotation  = "tag_entity"
  name_alias  = "alias_entity"
}

resource "aci_l3_domain_profile" "demo-domain-profile" {
  name  = "demo domain profile"
  annotation  = "l3_domain_profile_tag"
  name_alias  = "alias_name"
}
