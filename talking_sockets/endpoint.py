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

from talking_sockets.observer import Observable, Observer
from talking_sockets.utils import assert_bytes


class SourceEndpoint(Observable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buffer = bytearray()
        self._delimiter = None

    @property
    def input_delimiter(self):
        return self._delimiter

    def set_input_delimiter(self, delimiter):
        assert_bytes(delimiter)
        assert delimiter != bytes(), "Delimiter cannot be empty"
        self._delimiter = delimiter

    def process_data(self, data):
        assert_bytes(data)

        if len(data) == 0:
            return

        if self._delimiter is None:
            self.notify(data)
        else:
            self._buffer.extend(data)
            chunks = self._buffer.split(self._delimiter)
            if not self._buffer.endswith(self._delimiter):
                self._buffer = chunks[-1]
            else:
                self._buffer.clear()

            chunks.pop()
            for chunk in chunks:
                self.notify(chunk)


class SinkEndpoint(Observer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
