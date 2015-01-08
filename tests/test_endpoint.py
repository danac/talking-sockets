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

import os
import nose.tools as nt
from talking_sockets.observer import LoggingObserver
from talking_sockets.endpoint import SourceEndpoint


class TestSourceEndpoint:

    def setUp(self):
        self.source = SourceEndpoint()
        self.observer = LoggingObserver()

    def test_delimiter(self):
        nt.assert_equal(self.source.input_delimiter, None)
        delimiter = os.urandom(1)
        self.source.set_input_delimiter(delimiter)
        nt.assert_equal(self.source.input_delimiter, delimiter)

    def test_delimiter_wrong_data_type(self):
        nt.assert_raises(AssertionError, self.source.set_input_delimiter, None)
        nt.assert_raises(AssertionError, self.source.set_input_delimiter, str())
        nt.assert_raises(AssertionError, self.source.set_input_delimiter, int())
        nt.assert_raises(AssertionError, self.source.set_input_delimiter, bytes())

    def test_process_data_no_delimiter(self):
        self.source.add_observer(self.observer)
        nt.assert_equal(self.source.input_delimiter, None)
        message = os.urandom(100)
        self.source.process_data(message)
        nt.assert_equal(len(self.observer.messages), 1)
        nt.assert_equal(self.observer.messages[0], (self.source, message))

    def test_process_data_empty_message(self):
        self.source.process_data(bytes())

    def _process_message(self, message, delimiter):
        self.source.add_observer(self.observer)
        message_parts = message.split(delimiter)
        self.source.set_input_delimiter(delimiter)
        nt.assert_equal(self.source.input_delimiter, delimiter)
        self.source.process_data(message)
        nt.assert_equal(len(self.observer.messages), 2)
        nt.assert_equal(self.observer.messages[0], (self.source, message_parts[0]))
        nt.assert_equal(self.observer.messages[1], (self.source, message_parts[1]))

    def test_process_data_delimited_partial_chunk(self):
        message = b"part1|part2|half-part"
        delimiter = b"|"
        self._process_message(message, delimiter)

    def test_process_data_delimited_full_chunk(self):
        message = b"part1|part2|"
        delimiter = b"|"
        self._process_message(message, delimiter)

    def test_process_data_wrong_data_type(self):
        nt.assert_raises(AssertionError, self.source.process_data, None)
        nt.assert_raises(AssertionError, self.source.process_data, str())
        nt.assert_raises(AssertionError, self.source.process_data, int())
