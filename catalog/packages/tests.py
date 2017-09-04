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
from catalog.packages.ns_package import NsPackage
from catalog.packages.nf_package import NfPackage
from catalog.packages.nf_package import NfDistributeThread
from catalog.packages.nf_package import NfPkgDeleteThread
from django.test import Client
from catalog.pub.database.models import NSDModel, NfPackageModel, JobStatusModel, JobModel
from rest_framework import status


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.nsdata = None
        self.nfdata = None
        self.ns_csarId = 123
        self.nf_csarId = 456

        self.nsdata = {
            "csarId": str(self.ns_csarId)
        }

        self.csars= [
            {
                "csarId": "1",
                "nsdId": "1"
            },
            {
                "csarId": "2",
                 "nsdId": "2"
            }
        ]

        self.nfdata = {
            "csarId": str(self.nf_csarId)
        }

        self.vnfd_json = {
            "metadata": {
                "id": "456",
                "vendor": "zte",
                "version": "5.16.10",
                "vnfd_version": "1.1.0",
                "name": "zte_xgw",
                "domain_type": "CN",
                "vnf_type": "XGW",
                "is_shared": "false",
                "cross_dc": "false",
                "vmnumber_overquota_alarm": "false",
                "description": "",
                "vnf_extend_type": "driver&script",
                "plugin_info": "zte_cn_plugin_v6.16.10",
                "script_info": "script/cn.py",
                "adjust_vnf_capacity": "true",
                "custom_properties": "",
            },
            "reserved_total": {
                "vmnum": 10,
                "vcpunum": 20,
                "memorysize": 1000,
                "portnum": 30,
                "hdsize": 1024,
                "shdsize": 2048,
                "isreserve": 0,
            },
        }

        self.nsd_json = {

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
            "vnf_id": "456",
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
                "id": "456",
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
                "id": "456",
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
        NfPackageModel.objects.all().delete()
        NSDModel.objects.all().delete()
        JobStatusModel.objects.all().delete()

    @mock.patch.object(NsPackage, 'get_csars')
    def test_nspackages_get(self,mock_get_csars):
        mock_get_csars.return_value = [0,self.csars]
        response = self.client.get("/api/catalog/v1/nspackages")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)
        self.assertEquals(self.csars,response.data)

    @mock.patch.object(NsPackage,'get_nsd')
    def test_ns_distribute_2(self, mock_get_nsd):
        local_file_name = "/url/local/filename"
        nsd = json.JSONEncoder().encode(self.nsd_json)
        mock_get_nsd.return_value = self.nsd_json,local_file_name,nsd
        response = self.client.post("/api/catalog/v1/nspackages",self.nsdata)

        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assert_nsdmodel_result("VCPE_NS",  0)
        self.assertEqual("VNF package(456) is not distributed.", response.data["statusDescription"], response.content)
        NSDModel.objects.filter(id="VCPE_NS").delete()

    def test_nfpackages_get(self):
        response = self.client.get("/api/catalog/v1/vnfpackages")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

        nsdModel = NSDModel.objects.filter(nsd_id="VCPE_NS")
        self.assertSequenceEqual(nsdModel,[])


    @mock.patch.object(NfDistributeThread, 'get_vnfd')
    @mock.patch.object(NsPackage,'get_nsd')
    def test_ns_distribute(self, mock_get_nsd,mock_get_vnfd):
        # First distribute a VNF
        local_file_name = "/url/local/filename"
        vnfd = json.JSONEncoder().encode(self.vnfd_json)
        mock_get_vnfd.return_value = self.vnfd_json,local_file_name,vnfd
        NfDistributeThread(str(self.nf_csarId), ["1"], "1", "4").run()

        # Then distribute a NS associated with the below VNF
        local_file_name = "/url/local/filename"
        nsd = json.JSONEncoder().encode(self.nsd_json)
        mock_get_nsd.return_value = self.nsd_json,local_file_name,nsd
        response = self.client.post("/api/catalog/v1/nspackages",self.nsdata)
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assertEqual("CSAR(123) distributed successfully.", response.data["statusDescription"], response.content)
        self.assert_nsdmodel_result("VCPE_NS",  1)
        NfPackageModel.objects.filter(vnfdid=str(self.nf_csarId)).delete()
        NSDModel.objects.filter(nsd_id="VCPE_NS").delete()

    @mock.patch.object(NfDistributeThread, 'get_vnfd')
    def test_nf_distribute(self, mock_get_vnfd):
        local_file_name = "/url/local/filename"
        vnfd = json.JSONEncoder().encode(self.vnfd_json)
        mock_get_vnfd.return_value = self.vnfd_json,local_file_name,vnfd

        NfDistributeThread("dd", ["1"], "1", "5").run()
        self.assert_job_result("5", 100, "CSAR(dd) distribute successfully.")
        NfPackageModel.objects.filter(nfpackageid="dd").delete()

    @mock.patch.object(NfDistributeThread, 'get_vnfd')
    @mock.patch.object(NsPackage,'get_nsd')
    def test_ns_package_delete(self, mock_get_nsd,mock_get_vnfd):

        # First distribute a VNF
        local_file_name = "/url/local/filename"
        vnfd = json.JSONEncoder().encode(self.vnfd_json)
        mock_get_vnfd.return_value = self.vnfd_json,local_file_name,vnfd
        NfDistributeThread(str(self.nf_csarId), ["1"], "1", "4").run()
        self.assert_nfmodel_result(str(self.nf_csarId), 1)

        # Then distribute a NS associated with the below VNF
        local_file_name = "/url/local/filename"
        nsd = json.JSONEncoder().encode(self.nsd_json)
        mock_get_nsd.return_value = self.nsd_json,local_file_name,nsd
        response = self.client.post("/api/catalog/v1/nspackages",self.nsdata)
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assertEqual("CSAR(123) distributed successfully.", response.data["statusDescription"], response.content)
        self.assert_nfmodel_result(str(self.nf_csarId), 1)
        self.assert_nsdmodel_result("VCPE_NS",  1)

        # Finally delete ns package
        response = self.client.delete("/api/catalog/v1/nspackages/" + str(self.ns_csarId))
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assertEqual("Delete CSAR(123) successfully.", response.data["statusDescription"], response.content)
        self.assert_nsdmodel_result("VCPE_NS",  0)

    def test_nf_package_delete_error(self):
        # Delete it directly
        self.assert_nfmodel_result("bb",0)
        NfPkgDeleteThread("bb", "6", False).run()
        self.assert_job_result("6", 100, "Error! CSAR(bb) does not exist.")


    @mock.patch.object(NfDistributeThread, 'get_vnfd')
    def test_nf_package_delete(self,mock_get_vnfd):
        # First distribute a VNF
        local_file_name = "/url/local/filename"
        vnfd = json.JSONEncoder().encode(self.vnfd_json)
        mock_get_vnfd.return_value = self.vnfd_json,local_file_name,vnfd

        NfDistributeThread("bb", ["1"], "1", "5").run()
        self.assert_job_result("5", 100, "CSAR(bb) distribute successfully.")
        self.assert_nfmodel_result("bb",1)

        # Then delete it
        NfPkgDeleteThread("bb", "6", False).run()
        self.assert_nfmodel_result("bb",0)

    def assert_job_result(self, job_id, job_progress, job_detail):
        jobs = JobStatusModel.objects.filter(
            jobid=job_id,
            progress=job_progress,
            descp=job_detail)
        self.assertEqual(1, len(jobs))

    def assert_nsdmodel_result(self,nsd_id,size):
        nsdmodels = NSDModel.objects.filter(
            nsd_id = nsd_id
        )

        self.assertEquals(size, len(nsdmodels))

    def assert_nfmodel_result(self,csar_id,size):
        vnfdmodels = NfPackageModel.objects.filter(
            nfpackageid = csar_id
        )

        self.assertEquals(size, len(vnfdmodels))

    def test_nf_package_parser(self):
         reqdata={"csarId":"1"}
         #response = self.client.post("/api/catalog/v1/parservnfd",reqdata)
         #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)

    @mock.patch.object(NfDistributeThread, 'get_vnfd')
    @mock.patch.object(NsPackage,'get_nsd')
    def test_ns_distribute(self, mock_get_nsd,mock_get_vnfd):
        # First distribute a VNF
        local_file_name = "/resource/resource-TestFyx-template.yml"
        vnfd = json.JSONEncoder().encode(self.vnfd_json)
        mock_get_vnfd.return_value = self.vnfd_json,local_file_name,vnfd
        NfDistributeThread(str(self.nf_csarId), ["1"], "1", "4").run()
        self.assert_nfmodel_result(str(self.nf_csarId), 1)

        # Then distribute a NS associated with the below VNF
        local_file_name = "service-TestServiceFyx-template.yml"
        nsd = json.JSONEncoder().encode(self.nsd_json)
        mock_get_nsd.return_value = self.nsd_json,local_file_name,nsd
        response = self.client.post("/api/catalog/v1/nspackages",self.nsdata)
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        self.assertEqual("CSAR(123) distributed successfully.", response.data["statusDescription"], response.content)
        self.assert_nfmodel_result(str(self.nf_csarId), 1)
        self.assert_nsdmodel_result("VCPE_NS",  1)

        reqdata = {"csarId": "123", "inputs":""}
        response = self.client.post("/api/catalog/v1/parsernsd",reqdata)
        #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)