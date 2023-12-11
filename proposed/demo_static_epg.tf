resource "aci_epg_to_static_path" "path-129-1-3-1000-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-1000"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-1000"
}

resource "aci_epg_to_static_path" "path-129-1-3-998-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-998"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-998"
}

resource "aci_epg_to_static_path" "path-129-1-3-997-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-997"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-997"
}

resource "aci_epg_to_static_path" "path-129-1-3-999-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-999"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-500"
}

resource "aci_epg_to_static_path" "path-129-1-3-500-r" {
  application_epg_dn  = aci_application_epg.demo-app.id
  tdn  = "topology/pod-1/paths-129/pathep-[eth1/3]"
  annotation = "annotation"
  encap  = "vlan-500"
  instr_imedcy = "lazy"
  mode  = "regular"
  primary_encap ="vlan-500"
}


