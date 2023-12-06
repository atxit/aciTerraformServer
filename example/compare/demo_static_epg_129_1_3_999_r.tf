resource "aci_epg_to_static_path" "path-129-1-3-999-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-999"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-500"
}