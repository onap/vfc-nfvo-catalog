# Copyright 2018 ZTE Corporation.
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

import copy
import json
import mock
import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalog.packages.biz.ns_descriptor import NsDescriptor
from catalog.packages.const import PKG_STATUS
from catalog.packages.tests.const import nsd_data
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import NSPackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.utils import toscaparser


class TestNsDescriptor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_defined_data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }
        self.expected_nsd_info = {
            'id': None,
            'nsdId': None,
            'nsdName': None,
            'nsdVersion': None,
            'nsdDesigner': None,
            'nsdInvariantId': None,
            'vnfPkgIds': [],
            'pnfdInfoIds': [],
            'nestedNsdInfoIds': [],
            'nsdOnboardingState': 'CREATED',
            'onboardingFailureDetails': None,
            'nsdOperationalState': 'DISABLED',
            'nsdUsageState': 'NOT_IN_USE',
            'userDefinedData': self.user_defined_data,
            '_links': None
        }
        self.nsdModel = {
            "pnfs": [{"properties": {"id": "m6000_s"}}],
            "vnfs": [{"properties": {"id": "123"}}]
        }

    def tearDown(self):
        pass

    def test_nsd_create_normal(self):
        reqest_data = {'userDefinedData': self.user_defined_data}
        expected_reponse_data = {
            'nsdOnboardingState': 'CREATED',
            'nsdOperationalState': 'DISABLED',
            'nsdUsageState': 'NOT_IN_USE',
            'userDefinedData': self.user_defined_data,
            '_links': None
        }

        response = self.client.post(
            '/api/nsd/v1/ns_descriptors',
            data=reqest_data,
            format='json'
        )
        response.data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_multiple_nsds_normal(self):
        expected_reponse_data = [
            copy.deepcopy(self.expected_nsd_info),
            copy.deepcopy(self.expected_nsd_info)
        ]
        expected_reponse_data[0]['id'] = '0'
        expected_reponse_data[0]['nsdId'] = '0'
        expected_reponse_data[1]['id'] = '1'
        expected_reponse_data[1]['nsdId'] = '1'

        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        for i in range(2):
            NSPackageModel(
                nsPackageId=str(i),
                onboardingState='CREATED',
                operationalState='DISABLED',
                usageState='NOT_IN_USE',
                userDefinedData=user_defined_data,
                nsdId=str(i)
            ).save()

        response = self.client.get('/api/nsd/v1/ns_descriptors', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_reponse_data, response.data)

        expected_reponse_data = [
            copy.deepcopy(self.expected_nsd_info)
        ]
        expected_reponse_data[0]['id'] = '1'
        expected_reponse_data[0]['nsdId'] = '1'
        response = self.client.get('/api/nsd/v1/ns_descriptors?nsdId=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_single_nsd_normal(self):
        expected_reponse_data = copy.deepcopy(self.expected_nsd_info)
        expected_reponse_data['id'] = '22'

        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        NSPackageModel(
            nsPackageId='22',
            onboardingState='CREATED',
            operationalState='DISABLED',
            usageState='NOT_IN_USE',
            userDefinedData=user_defined_data,
            nsdModel=json.JSONEncoder().encode(self.nsdModel)
        ).save()

        response = self.client.get('/api/nsd/v1/ns_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_single_when_ns_not_exist(self):
        response = self.client.get('/api/nsd/v1/ns_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_nsd_normal(self):
        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        NSPackageModel(
            nsPackageId='21',
            operationalState='DISABLED',
            usageState='NOT_IN_USE',
            userDefinedData=user_defined_data,
            nsdModel='test'
        ).save()

        response = self.client.delete("/api/nsd/v1/ns_descriptors/21", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, response.data)

    def test_delete_when_ns_not_exist(self):
        response = self.client.delete("/api/nsd/v1/ns_descriptors/21", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_nsd_content_upload_normal(self, mock_parse_nsd):
        user_defined_data_json = json.JSONEncoder().encode(self.user_defined_data)
        mock_parse_nsd.return_value = json.JSONEncoder().encode(nsd_data)
        VnfPackageModel(
            vnfPackageId="111",
            vnfdId="vcpe_vfw_zte_1_0"
        ).save()

        PnfPackageModel(
            pnfPackageId="112",
            pnfdId="m6000_s"
        ).save()

        NSPackageModel(
            nsPackageId='22',
            operationalState='DISABLED',
            usageState='NOT_IN_USE',
            userDefinedData=user_defined_data_json,
        ).save()

        with open('nsd_content.txt', 'wt') as fp:
            fp.write('test')
        with open('nsd_content.txt', 'rt') as fp:
            resp = self.client.put(
                "/api/nsd/v1/ns_descriptors/22/nsd_content",
                {'file': fp},
            )
        file_content = ''
        with open(os.path.join(CATALOG_ROOT_PATH, '22/nsd_content.txt')) as fp:
            data = fp.read()
            file_content = '%s%s' % (file_content, data)
        ns_pkg = NSPackageModel.objects.filter(nsPackageId="22")
        self.assertEqual("VCPE_NS", ns_pkg[0].nsdId)
        self.assertEqual(PKG_STATUS.ONBOARDED, ns_pkg[0].onboardingState)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, resp.data)
        self.assertEqual(file_content, 'test')
        os.remove('nsd_content.txt')

    def test_nsd_content_upload_failure(self):
        with open('nsd_content.txt', 'wt') as fp:
            fp.write('test')
        with open('nsd_content.txt', 'rt') as fp:
            response = self.client.put(
                "/api/nsd/v1/ns_descriptors/22/nsd_content",
                {'file': fp},
            )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_nsd_content_download_normal(self):
        with open('nsd_content.txt', 'wt') as fp:
            fp.writelines('test1')
            fp.writelines('test2')
        NSPackageModel.objects.create(
            nsPackageId='23',
            onboardingState='ONBOARDED',
            localFilePath='nsd_content.txt'
        )
        response = self.client.get(
            "/api/nsd/v1/ns_descriptors/23/nsd_content", format='json'
        )
        file_content = ""
        for data in response.streaming_content:
            file_content = '%s%s' % (file_content, data.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("test1test2", file_content)
        os.remove('nsd_content.txt')

    def test_nsd_content_download_when_ns_not_exist(self):
        response = self.client.get("/api/nsd/v1/ns_descriptors/23/nsd_content", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nsd_content_download_failed(self):
        NSPackageModel.objects.create(
            nsPackageId='23',
            onboardingState='CREATED',
            localFilePath='nsd_content.txt'
        )
        response = self.client.get("/api/nsd/v1/ns_descriptors/23/nsd_content", format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_nsd_content_partial_download_normal(self):
        with open('nsd_content.txt', 'wt') as fp:
            fp.writelines('test1')
            fp.writelines('test2')
        NSPackageModel(
            nsPackageId='23',
            onboardingState='ONBOARDED',
            localFilePath='nsd_content.txt'
        ).save()

        response = self.client.get(
            "/api/nsd/v1/ns_descriptors/23/nsd_content",
            HTTP_RANGE='5-10',
            format='json'
        )
        partial_file_content = ''
        for data in response.streaming_content:
            partial_file_content = '%s%s' % (partial_file_content, data.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("test2", partial_file_content)
        os.remove('nsd_content.txt')

    @mock.patch.object(NsDescriptor, 'create')
    def test_nsd_create_when_catch_exception(self, mock_create):
        reqest_data = {'userDefinedData': self.user_defined_data}
        mock_create.side_effect = TypeError("integer type")
        response = self.client.post('/api/nsd/v1/ns_descriptors', data=reqest_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(NsDescriptor, 'query_single')
    def test_query_single_when_catch_exception(self, mock_query_single):
        mock_query_single.side_effect = TypeError("integer type")
        response = self.client.get('/api/nsd/v1/ns_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(NsDescriptor, 'query_multiple')
    def test_query_multiple_when_catch_exception(self, mock_query_multipe):
        mock_query_multipe.side_effect = TypeError("integer type")
        response = self.client.get('/api/nsd/v1/ns_descriptors', format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(NsDescriptor, 'delete_single')
    def test_delete_when_catch_exception(self, mock_delete_single):
        mock_delete_single.side_effect = TypeError("integer type")
        response = self.client.delete("/api/nsd/v1/ns_descriptors/21", format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(NsDescriptor, 'upload')
    def test_upload_when_catch_exception(self, mock_upload):
        mock_upload.side_effect = TypeError("integer type")
        with open('nsd_content.txt', 'wt') as fp:
            fp.write('test')
        with open('nsd_content.txt', 'rt') as fp:
            response = self.client.put("/api/nsd/v1/ns_descriptors/22/nsd_content", {'file': fp})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        os.remove('nsd_content.txt')

    @mock.patch.object(NsDescriptor, 'download')
    def test_download_when_catch_exception(self, mock_download):
        mock_download.side_effect = TypeError("integer type")
        response = self.client.get("/api/nsd/v1/ns_descriptors/23/nsd_content", format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
