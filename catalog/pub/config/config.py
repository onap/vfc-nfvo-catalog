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

# [MSB]

MSB_SERVICE_PROTOCOL = 'http'
MSB_SERVICE_IP = '127.0.0.1'
MSB_SERVICE_PORT = '443'
MSB_BASE_URL = "%s://%s:%s" % (MSB_SERVICE_PROTOCOL, MSB_SERVICE_IP, MSB_SERVICE_PORT)

# [REDIS]
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWD = ''

# [mysql]
DB_IP = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "nfvocatalog"
DB_USER = "nfvocatalog"
DB_PASSWD = "nfvocatalog"

# [MDC]
SERVICE_NAME = "catalog"
FORWARDED_FOR_FIELDS = ["HTTP_X_FORWARDED_FOR", "HTTP_X_FORWARDED_HOST",
                        "HTTP_X_FORWARDED_SERVER"]

# [register]
REG_TO_MSB_WHEN_START = True
REG_TO_MSB_REG_URL = "/api/microservices/v1/services"
REG_TO_MSB_REG_PARAM = [{
    "serviceName": "catalog",
    "version": "v1",
    "url": "/api/catalog/v1",
    "protocol": "REST",
    "visualRange": "1",
    "nodes": [{
        "ip": "127.0.0.1",
        "port": "8806",
        "ttl": 0
    }]
}, {
    "serviceName": "nsd",
    "version": "v1",
    "url": "/api/nsd/v1",
    "protocol": "REST",
    "visualRange": "1",
    "nodes": [{
        "ip": "127.0.0.1",
        "port": "8806",
        "ttl": 0
    }]
}, {
    "serviceName": "vnfpkgm",
    "version": "v1",
    "url": "/api/vnfpkgm/v1",
    "protocol": "REST",
    "visualRange": "1",
    "nodes": [{
        "ip": "127.0.0.1",
        "port": "8806",
        "ttl": 0
    }]
}]
MSB_SVC_CALALOG_URL = "/api/microservices/v1/services/catalog/version/v1"
MSB_SVC_NSD_URL = "/api/microservices/v1/services/nsd/version/v1"
MSB_SVC_VNFPKGM_URL = "/api/microservices/v1/services/vnfpkgm/version/v1"

# catalog path(values is defined in settings.py)
CATALOG_ROOT_PATH = None
CATALOG_URL_PATH = None

# [sdc config]
SDC_BASE_URL = "http://msb-iag/api"
SDC_USER = "aai"
SDC_PASSWD = "Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U"

# [aai config]
AAI_BASE_URL = "http://10.0.14.1:80/aai/v11"
AAI_USER = "AAI"
AAI_PASSWD = "AAI"
REPORT_TO_AAI = True

VNFD_SCHEMA_VERSION_DEFAULT = "base"
