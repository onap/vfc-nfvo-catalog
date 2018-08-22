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

from django.conf.urls import url

from catalog.packages.views.vnfpkg_views import package_content, upload_from_uri, vnf_package, vnf_packages
from catalog.packages.views import (catalog_views, ns_descriptor_views,
                                    nsd_content_views, pnf_descriptor_views,
                                    pnfd_content_views)


urlpatterns = [
    url(r'^api/catalog/v1/nspackages$', catalog_views.nspackages_rc, name='nspackages_rc'),
    url(r'^api/catalog/v1/nspackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', catalog_views.ns_rd_csar, name='nspackage_rd'),
    url(r'^api/catalog/v1/vnfpackages$', catalog_views.nfpackages_rc, name='nfpackages_rc'),
    url(r'^api/catalog/v1/vnfpackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', catalog_views.nf_rd_csar, name='nfpackage_rd'),
    url(r'^api/catalog/v1/parsernsd$', catalog_views.ns_model_parser, name='nsmodelparser_rc'),
    url(r'^api/catalog/v1/parservnfd$', catalog_views.vnf_model_parser, name='vnfmodelparser_rc'),

    # NSD
    url(r'^api/nsd/v1/ns_descriptors$', ns_descriptor_views.create_ns_descriptors, name='ns_descriptors_rc'),
    url(r'^api/nsd/v1/ns_descriptors$', ns_descriptor_views.query_ns_descriptors, name='ns_info_rd'),
    url(r'^api/nsd/v1/ns_descriptors/(?P<nsdInfoId>[0-9a-zA-Z\-\_]+)/nsd_content$', nsd_content_views.upload_nsd_content, name='nsd_content_ru'),

    # PNF
    url(r'^api/nsd/v1/pnf_descriptors$', pnf_descriptor_views.create_pnf_descriptors, name='pnf_descriptors_rc'),
    url(r'^api/nsd/v1/pnf_descriptors/(?P<pnfdInfoId>[0-9a-zA-Z\-\_]+)/pnfd_content$', pnfd_content_views.upload_pnfd_content, name='pnfd_content_ru'),
    # TODO SOL005 & SOL003

    # url(r'^api/nsd/v1/pnf_descriptors/(?P<pnfdInfoId>[0-9a-zA-Z\-\_]+)$', pnfd_info.as_view(), name='pnfd_info_rd'),

    # url(r'^api/nsd/v1/subscriptions', nsd_subscriptions.as_view(), name='subscriptions_rc'),
    # url(r'^api/nsd/v1/subscriptions/(?P<subscriptionId>[0-9a-zA-Z\-\_]+)$', nsd_subscription.as_view(), name='subscription_rd'),
    url(r'^api/vnfpkgm/v1/vnf_packages', vnf_packages.as_view(), name='vnf_packages_rc'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)$', vnf_package.as_view(), name='vnf_package_rd'),
    # url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/vnfd$', vnfd.as_view(), name='vnfd_r'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/package_content$',
        package_content.as_view(), name='package_content_ru'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/package_content/upload_from_uri$',
        upload_from_uri.as_view(), name='upload_from_uri_c'),
    # url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/artifacts/artifactPath$', artifacts.as_view(), name='artifacts_r'),
    # url(r'^api/vnfpkgm/v1/subscriptions', vnfpkg_subscriptions.as_view(), name='subscriptions_rc'),
    # url(r'^api/vnfpkgm/v1/subscriptions/(?P<subscriptionId>[0-9a-zA-Z\-\_]+)$', vnfpkg_subscription.as_view(), name='subscription_rd'),
]
