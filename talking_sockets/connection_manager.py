#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Dana Christen
#
# This file is part of talking-sockets, a tool for connection routing.
#
# talking-sockets is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import abc
from talking_sockets.utils import assert_type


class ConnectionManager(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self._buffers = dict()
        self._delimiter = None

    @property
    def input_delimiter(self):
        return self._delimiter

    def set_input_delimiter(self, delimiter):
        assert_type(delimiter, bytes)
        assert delimiter != bytes(), "Delimiter cannot be empty"
        self._delimiter = delimiter

    def process_data(self, origin, data):
        assert_type(data, bytes)

        assert origin in self._buffers.keys(), "Origin not registered"

        if len(data) == 0:
            return

        if self._delimiter is None:
            self.message_ready(origin, data)
        else:
            self._buffers[origin].extend(data)
            chunks = self._buffers[origin].split(self._delimiter)
            if not self._buffers[origin].endswith(self._delimiter):
                self._buffers[origin] = chunks[-1]
            else:
                self._buffers[origin].clear()

            chunks.pop()
            for chunk in chunks:
                self.message_ready(origin, chunk)

    def register_connection(self, origin):
        self._buffers[origin] = bytearray()

    def unregister_connection(self, origin):
        self._buffers.pop(origin)

    @property
    def connections(self):
        return self._buffers.keys()

    @abc.abstractmethod
    def message_ready(self, origin, message):  # pragma: no cover
        pass
