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

from rest_framework import serializers


class ProblemDetailsSerializer(serializers.Serializer):
    type = serializers.CharField(
        help_text='A URI reference according to IETF RFC 3986 [10] that identifies the problem type. \
        It is encouraged that the URI provides human-readable documentation for the problem (e.g. using HTML) when dereferenced. \
        When this member is not present, its value is assumed to be "about:blank".',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    title = serializers.CharField(
        help_text='A short, human-readable summary of the problem type. \
        It should not change from occurrence to occurrence of the problem, except for purposes of localization. \
        If type is given and other than "about:blank", this attribute shall also be provided.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    title = serializers.IntegerField(
        help_text='The HTTP status code for this occurrence of the problem.',
        required=True,
        allow_null=False
    )
    detail = serializers.CharField(
        help_text='A human-readable explanation specific to this occurrence of the problem.',
        required=True,
        allow_null=False,
        allow_blank=False
    )
    instance = serializers.CharField(
        help_text='A URI reference that identifies the specific occurrence of the problem. \
        It may yield further information if dereferenced.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    additional_attributes = serializers.DictField(
        help_text='Any number of additional attributes, as defined in a specification or by an implementation.',
        child=serializers.CharField(help_text='Additional attribute', allow_blank=True),
        required=False,
        allow_null=True,
    )
