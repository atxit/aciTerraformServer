resource "aci_vrf" "demo-VRF" {
  tenant_dn              = aci_tenant.demo-test.id
  name                   = "demo_vrf"
  description            = "from terraform"
  annotation             = "tag_vrf"
  bd_enforced_enable     = "no"
  ip_data_plane_learning = "enabled"
  knw_mcast_act          = "permit"
  name_alias             = "alias_vrf"
  pc_enf_dir             = "egress"
  pc_enf_pref            = "unenforced"
  relation_fv_rs_ctx_to_bgp_ctx_af_pol {
    af                     = "ipv4-ucast"
    tn_bgp_ctx_af_pol_name = aci_bgp_address_family_context.bgp-family-context-example.id
  }
}