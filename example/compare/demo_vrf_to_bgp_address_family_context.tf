resource "aci_vrf_to_bgp_address_family_context" "vrf-to-bgp-family-example" {
  vrf_dn  = aci_vrf.demo-VRF.id
  bgp_address_family_context_dn = aci_bgp_address_family_context.bgp-family-context-example.id
  address_family  = "ipv4-ucast"
}