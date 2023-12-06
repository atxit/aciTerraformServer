resource "aci_application_epg" "demo-app" {
    application_profile_dn  = aci_application_profile.demo-app-profile.id
    name                    = "demo_epg"
    description             = "from terraform"
    annotation              = "tag_epg"
    exception_tag           = "0"
    flood_on_encap          = "disabled"
    fwd_ctrl                = "none"
    has_mcast_source        = "no"
    is_attr_based_epg       = "no"
    match_t                 = "AtleastOne"
    name_alias              = "alias_epg"
    pc_enf_pref             = "unenforced"
    pref_gr_memb            = "exclude"
    prio                    = "unspecified"
    shutdown                = "no"
    relation_fv_rs_bd       = aci_bridge_domain.demo-app-bd.id
}


resource "aci_bridge_domain" "demo-app-bd" {
    tenant_dn                   = aci_tenant.demo-test.id
    description                 = "from terraform"
    name                        = "demo_bd"
    optimize_wan_bandwidth      = "no"
    annotation                  = "tag_bd"
    arp_flood                   = "no"
    ep_clear                    = "no"
    ep_move_detect_mode         = "garp"
    host_based_routing          = "no"
    intersite_bum_traffic_allow = "yes"
    intersite_l2_stretch        = "yes"
    ip_learning                 = "yes"
    ipv6_mcast_allow            = "no"
    limit_ip_learn_to_subnets   = "yes"
    ll_addr                     = "::"
    mac                         = "00:22:BD:F8:19:FF"
    mcast_allow                 = "yes"
    multi_dst_pkt_act           = "bd-flood"
    name_alias                  = "alias_bd"
    bridge_domain_type          = "regular"
    unicast_route               = "no"
    unk_mac_ucast_act           = "flood"
    unk_mcast_act               = "flood"
    v6unk_mcast_act             = "flood"
    vmac                        = "not-applicable"
    relation_fv_rs_ctx          = aci_vrf.demo-VRF.id
}

resource "aci_subnet" "SUBNET-10-10-10-1-24" {
    parent_dn        = aci_bridge_domain.demo-app-bd.id
    description      = "subnet"
    ip               = "10.10.10.1/24"
    annotation       = "tag_subnet"
    ctrl             = ["querier", "nd"]
    name_alias       = "alias_subnet"
    preferred        = "no"
    scope            = ["private", "shared"]
    virtual          = "yes"
}


resource "aci_l3_domain_profile" "demo-l3-profile" {
  name  = "demo_l3_profile"
  annotation  = "l3_domain_profile_tag"
  name_alias  = "alias_name"
}


resource "aci_aaep_to_domain" "foo_aaep_to_domain" {
  attachable_access_entity_profile_dn = aci_attachable_access_entity_profile.demo-aaep-profile.id
  domain_dn                           = aci_l3_domain_profile.demo-l3-profile.id
}

