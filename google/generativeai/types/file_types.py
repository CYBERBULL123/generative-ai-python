# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import datetime
from typing import Union
from typing_extensions import TypedDict

from google.generativeai.client import get_default_file_client

import google.ai.generativelanguage as glm


class File:
    def __init__(self, proto: glm.File | File | dict):
        if isinstance(proto, File):
            proto = proto.to_proto()
        self._proto = glm.File(proto)

    def to_proto(self):
        return self._proto

    @property
    def name(self) -> str:
        return self._proto.name

    @property
    def display_name(self) -> str:
        return self._proto.display_name

    @property
    def mime_type(self) -> str:
        return self._proto.mime_type

    @property
    def size_bytes(self) -> int:
        return self._proto.size_bytes

    @property
    def create_time(self) -> datetime.datetime:
        return self._proto.create_time

    @property
    def update_time(self) -> datetime.datetime:
        return self._proto.update_time

    @property
    def expiration_time(self) -> datetime.datetime:
        return self._proto.expiration_time

    @property
    def sha256_hash(self) -> bytes:
        return self._proto.sha256_hash

    @property
    def uri(self) -> str:
        return self._proto.uri

    @property
    def state(self) -> glm.File.State:
        return self._proto.state

    def delete(self):
        client = get_default_file_client()
        client.delete_file(name=self.name)


class FileDataDict(TypedDict):
    mime_type: str
    file_uri: str


FileDataType = Union[FileDataDict, glm.FileData, glm.File, File]


def to_file_data(file_data: FileDataType):
    if isinstance(file_data, dict):
        if "file_uri" in file_data:
            file_data = glm.FileData(file_data)
        else:
            file_data = glm.File(file_data)

    if isinstance(file_data, File):
        file_data = file_data.to_proto()

    if isinstance(file_data, glm.File):
        file_data = glm.FileData(
            mime_type=file_data.mime_type,
            file_uri=file_data.uri,
        )

    if isinstance(file_data, glm.FileData):
        return file_data
    else:
        raise TypeError(f"Could not convert a {type(file_data)} to `FileData`")
