# Copyright 2017 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import mock
import catalog.pub.utils.restcall
import json
from catalog.packages.sdc_ns_package import SdcNsPackage
from catalog.packages import sdc_nf_package
from django.test import Client
from catalog.pub.database.models import NSDModel, NfPackageModel
from rest_framework import status


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.nsdata = None
        self.nfdata = None
        self.ns_csarId = 123
        self.nf_csarId = 456

        self.nsdata = {
            "csarId": self.ns_csarId
        }

        self.nfdata = {
            "csarId": self.nf_csarId
        }

        self.nsd_json = {
    "vnffgs": [
        {
            "vnffg_id": "vnffg1",
            "description": "",
            "members": [
                "path1",
                "path2"
            ],
            "properties": {
                "vendor": "zte",
                "connection_point": [
                    "m6000_data_in",
                    "m600_tunnel_cp",
                    "m6000_data_out"
                ],
                "version": "1.0",
                "constituent_vnfs": [
                    "VFW",
                    "VNAT"
                ],
                "number_of_endpoints": 3,
                "dependent_virtual_link": [
                    "sfc_data_network",
                    "ext_datanet_net",
                    "ext_mnet_net"
                ]
            }
        }
    ],
    "inputs": {
        "sfc_data_network": {
            "type": "string",
            "value": "sfc_data_network"
        },
        "externalDataNetworkName": {
            "type": "string",
            "value": "vlan_4004_tunnel_net"
        },
        "externalManageNetworkName": {
            "type": "string",
            "value": "vlan_4008_mng_net"
        },
        "NatIpRange": {
            "type": "string",
            "value": "192.167.0.10-192.168.0.20"
        },
        "externalPluginManageNetworkName": {
            "type": "string",
            "value": "vlan_4007_plugin_net"
        }
    },
    "pnfs": [
        {
            "pnf_id": "m6000_s",
            "cps": [],
            "description": "",
            "properties": {
                "vendor": "zte",
                "request_reclassification": "false",
                "pnf_type": "m6000s",
                "version": "1.0",
                "management_address": "111111",
                "id": "m6000_s",
                "nsh_aware": "false"
            }
        }
    ],
    "fps": [
        {
            "properties": {
                "symmetric": "false",
                "policy": {
                    "type": "ACL",
                    "criteria": {
                        "dest_port_range": "1-100",
                        "ip_protocol": "tcp",
                        "source_ip_range": [
                            "119.1.1.1-119.1.1.10"
                        ],
                        "dest_ip_range": [
                            {
                                "get_input": "NatIpRange"
                            }
                        ],
                        "dscp": 0,
                        "source_port_range": "1-100"
                    }
                }
            },
            "forwarder_list": [
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m6000_data_out"
                },
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m600_tunnel_cp"
                },
                {
                    "capability": "vnat_fw_inout",
                    "type": "vnf",
                    "node_name": "VNAT"
                }
            ],
            "description": "",
            "fp_id": "path2"
        },
        {
            "properties": {
                "symmetric": "true",
                "policy": {
                    "type": "ACL",
                    "criteria": {
                        "dest_port_range": "1-100",
                        "ip_protocol": "tcp",
                        "source_ip_range": [
                            "1-100"
                        ],
                        "dest_ip_range": [
                            "1-100"
                        ],
                        "dscp": 4,
                        "source_port_range": "1-100"
                    }
                }
            },
            "forwarder_list": [
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m6000_data_in"
                },
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m600_tunnel_cp"
                },
                {
                    "capability": "vfw_fw_inout",
                    "type": "vnf",
                    "node_name": "VFW"
                },
                {
                    "capability": "vnat_fw_inout",
                    "type": "vnf",
                    "node_name": "VNAT"
                },
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m600_tunnel_cp"
                },
                {
                    "capability": "",
                    "type": "cp",
                    "node_name": "m6000_data_out"
                }
            ],
            "description": "",
            "fp_id": "path1"
        }
    ],
    "routers": [],
    "vnfs": [
        {
            "vnf_id": "VFW",
            "description": "",
            "properties": {
                "plugin_info": "vbrasplugin_1.0",
                "vendor": "zte",
                "is_shared": "false",
                "adjust_vnf_capacity": "true",
                "name": "VFW",
                "vnf_extend_type": "driver",
                "csarVersion": "v1.0",
                "csarType": "NFAR",
                "csarProvider": "ZTE",
                "version": "1.0",
                "nsh_aware": "true",
                "cross_dc": "false",
                "vnf_type": "VFW",
                "vmnumber_overquota_alarm": "true",
                "vnfd_version": "1.0.0",
                "externalPluginManageNetworkName": "vlan_4007_plugin_net",
                "id": "vcpe_vfw_zte_1_0",
                "request_reclassification": "false"
            },
            "dependencies": [
                {
                    "key_name": "vfw_ctrl_by_manager_cp",
                    "vl_id": "ext_mnet_net"
                },
                {
                    "key_name": "vfw_data_cp",
                    "vl_id": "sfc_data_network"
                }
            ],
            "type": "tosca.nodes.nfv.ext.zte.VNF.VFW",
            "networks": []
        },
        {
            "vnf_id": "VNAT",
            "description": "",
            "properties": {
                "NatIpRange": "192.167.0.10-192.168.0.20",
                "plugin_info": "vbrasplugin_1.0",
                "vendor": "zte",
                "is_shared": "false",
                "adjust_vnf_capacity": "true",
                "name": "VNAT",
                "id": "vcpe_vnat_zte_1",
                "vnf_extend_type": "driver",
                "csarVersion": "v1.0",
                "csarType": "NFAR",
                "csarProvider": "ZTE",
                "version": "1.0",
                "nsh_aware": "true",
                "cross_dc": "false",
                "vnf_type": "VNAT",
                "vmnumber_overquota_alarm": "true",
                "vnfd_version": "1.0.0",
                "externalPluginManageNetworkName": "vlan_4007_plugin_net",
                "request_reclassification": "false"
            },
            "dependencies": [
                {
                    "key_name": "vnat_ctrl_by_manager_cp",
                    "vl_id": "ext_mnet_net"
                },
                {
                    "key_name": "vnat_data_cp",
                    "vl_id": "sfc_data_network"
                }
            ],
            "type": "tosca.nodes.nfv.ext.zte.VNF.VNAT",
            "networks": []
        }
    ],
    "ns_exposed": {
        "external_cps": [],
        "forward_cps": []
    },
    "policies": [
        {
            "file_url": "policies/abc.drl",
            "name": "aaa"
        }
    ],
    "vls": [
        {
            "route_id": "",
            "vl_id": "ext_mnet_net",
            "route_external": "false",
            "description": "",
            "properties": {
                "name": "vlan_4008_mng_net",
                "mtu": 1500,
                "location_info": {
                    "tenant": "admin",
                    "vimid": 2,
                    "availability_zone": "nova"
                },
                "ip_version": 4,
                "dhcp_enabled": "true",
                "network_name": "vlan_4008_mng_net",
                "network_type": "vlan"
            }
        },
        {
            "route_id": "",
            "vl_id": "ext_datanet_net",
            "route_external": "false",
            "description": "",
            "properties": {
                "name": "vlan_4004_tunnel_net",
                "mtu": 1500,
                "location_info": {
                    "tenant": "admin",
                    "vimid": 2,
                    "availability_zone": "nova"
                },
                "ip_version": 4,
                "dhcp_enabled": "true",
                "network_name": "vlan_4004_tunnel_net",
                "network_type": "vlan"
            }
        },
        {
            "route_id": "",
            "vl_id": "sfc_data_network",
            "route_external": "false",
            "description": "",
            "properties": {
                "name": "sfc_data_network",
                "dhcp_enabled": "true",
                "is_predefined": "false",
                "location_info": {
                    "tenant": "admin",
                    "vimid": 2,
                    "availability_zone": "nova"
                },
                "ip_version": 4,
                "mtu": 1500,
                "network_name": "sfc_data_network",
                "network_type": "vlan"
            }
        }
    ],
    "cps": [
        {
            "pnf_id": "m6000_s",
            "vl_id": "path2",
            "description": "",
            "cp_id": "m6000_data_out",
            "properties": {
                "direction": "bidirectional",
                "vnic_type": "normal",
                "bandwidth": 0,
                "mac_address": "11-22-33-22-11-44",
                "interface_name": "xgei-0/4/1/5",
                "ip_address": "176.1.1.2",
                "order": 0,
                "sfc_encapsulation": "mac"
            }
        },
        {
            "pnf_id": "m6000_s",
            "vl_id": "ext_datanet_net",
            "description": "",
            "cp_id": "m600_tunnel_cp",
            "properties": {
                "direction": "bidirectional",
                "vnic_type": "normal",
                "bandwidth": 0,
                "mac_address": "00-11-00-22-33-00",
                "interface_name": "gei-0/4/0/13",
                "ip_address": "191.167.100.5",
                "order": 0,
                "sfc_encapsulation": "mac"
            }
        },
        {
            "pnf_id": "m6000_s",
            "vl_id": "path2",
            "description": "",
            "cp_id": "m6000_data_in",
            "properties": {
                "direction": "bidirectional",
                "vnic_type": "normal",
                "bandwidth": 0,
                "mac_address": "11-22-33-22-11-41",
                "interface_name": "gei-0/4/0/7",
                "ip_address": "1.1.1.1",
                "order": 0,
                "sfc_encapsulation": "mac",
                "bond": "none"
            }
        },
        {
            "pnf_id": "m6000_s",
            "vl_id": "ext_mnet_net",
            "description": "",
            "cp_id": "m600_mnt_cp",
            "properties": {
                "direction": "bidirectional",
                "vnic_type": "normal",
                "bandwidth": 0,
                "mac_address": "00-11-00-22-33-11",
                "interface_name": "gei-0/4/0/1",
                "ip_address": "10.46.244.51",
                "order": 0,
                "sfc_encapsulation": "mac",
                "bond": "none"
            }
        }
    ],
    "metadata": {
        "invariant_id": "vcpe_ns_sff_1",
        "name": "VCPE_NS",
        "csarVersion": "v1.0",
        "csarType": "NSAR",
        "csarProvider": "ZTE",
        "version": 1,
        "vendor": "ZTE",
        "id": "VCPE_NS",
        "description": "vcpe_ns"
    }
}


    def tearDown(self):
        pass

    def test_nspackages_get(self):
        response = self.client.get("/api/catalog/v1/nspackages")
        print response
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)
        self.assertEquals([],response.data)

    @mock.patch.object(SdcNsPackage,'get_nsd')
    def test_ns_distribute(self, mock_get_nsd):


        local_file_name = "/url/local/filename"
        nsd = json.JSONEncoder().encode(self.nsd_json)
        mock_get_nsd.return_value = self.nsd_json,local_file_name,nsd
        response = self.client.post("/api/nfvocatalog/v1/nspackages",self.nsdata)


        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assertIsNotNone(NSDModel.objects.filter(id=self.ns_csarId))

    def test_nfpackages_get(self):
        response = self.client.get("/api/catalog/v1/vnfpackages")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

        nsdModel = NSDModel.objects.filter(nsd_id="VCPE_NS")
        self.assertSequenceEqual(nsdModel,[])
        #nsd_id = nsdModel.nsd_id
        #self.assertEqual(self.nsd_json["metadata"]["id"], nsdModel.nsd_id)
        #self.assertEqual(self.nsd_json["metadata"]["name"], nsdModel.name)
        #self.assertEqual(self.nsd_json["metadata"]["version"], nsdModel.version)
        #self.assertEqual(self.nsd_json["metadata"]["description"], nsdModel.description)
        #self.assertEqual(self.nsd_json["metadata"]["vendor"], nsdModel.vendor)

    def test_ns_distribute(self):
        response = self.client.post("/api/catalog/v1/nspackages",self.nsdata)
        #self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)


    def test_nf_distribute(self):
        #response = self.client.post("/api/catalog/v1/vnfpackages",self.nfdata)
        #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        pass

    def test_ns_package_delete(self):
        response = self.client.delete("/api/catalog/v1/nspackages/" + str(self.ns_csarId))
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)

    def test_nf_package_delete(self):
        #response = self.client.delete("/api/catalog/v1/vnfpackages/" + str(self.nf_csarId))
        #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        pass
