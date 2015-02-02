#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Dana Christen
#
# This file is part of talking-sockets, a tool for connection routing.
#
# talking-sockets is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# talking-sockets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with talking-sockets. If not, see <http://www.gnu.org/licenses/>.
#

import os
import nose.tools as nt
from unittest import mock
from talking_sockets.connection_manager import ConnectionManager


class DummyReader(ConnectionManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def message_ready(self, message):  # pragma: no cover
        pass


class TestBufferedMultiReader:

    def setUp(self):
        self.reader = DummyReader()

    def test_delimiter(self):
        nt.assert_equal(self.reader.input_delimiter, None)
        delimiter = os.urandom(1)
        self.reader.set_input_delimiter(delimiter)
        nt.assert_equal(self.reader.input_delimiter, delimiter)

    def test_delimiter_wrong_data_type(self):
        nt.assert_raises(AssertionError, self.reader.set_input_delimiter, None)
        nt.assert_raises(AssertionError, self.reader.set_input_delimiter, str())
        nt.assert_raises(AssertionError, self.reader.set_input_delimiter, int())
        nt.assert_raises(AssertionError, self.reader.set_input_delimiter, bytes())

    def test_process_data_no_delimiter(self):
        nt.assert_equal(self.reader.input_delimiter, None)
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader._buffers[mock.sentinel.origin] = bytearray()
            message = os.urandom(10)
            self.reader.process_data(mock.sentinel.origin, message)
            patched_message_ready.assert_called_once_with(mock.sentinel.origin, message)

    def test_process_data_empty_message(self):
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader._buffers[mock.sentinel.origin] = bytearray()
            self.reader.process_data(mock.sentinel.origin, bytes())
            assert patched_message_ready.called is False

    def test_process_data_delimited_one_packet_partial_chunk(self):
        message = b"part1|part2|half-part"
        delimiter = b"|"
        expected_notifications = message.split(delimiter)[:2]
        expected_calls = [mock.call(mock.sentinel.origin, arg) for arg in expected_notifications]
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader._buffers[mock.sentinel.origin] = bytearray()
            self.reader.set_input_delimiter(delimiter)
            self.reader.process_data(mock.sentinel.origin, message)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls)

    def test_process_data_delimited_two_packets_full_chunk(self):
        message1 = b"part1|part2|half-part"
        message2 = b"-second-half-part|part4|"
        delimiter = b"|"
        expected_notifications = [b"part1", b"part2", b"half-part-second-half-part", b"part4"]
        expected_calls = [mock.call(mock.sentinel.origin, arg) for arg in expected_notifications]
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader._buffers[mock.sentinel.origin] = bytearray()
            self.reader.set_input_delimiter(delimiter)
            self.reader.process_data(mock.sentinel.origin, message1)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls[:2])
            self.reader.process_data(mock.sentinel.origin, message2)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls)


    def test_process_data_wrong_data_type(self):
        self.reader._buffers[mock.sentinel.origin] = bytearray()
        nt.assert_raises(AssertionError, self.reader.process_data, mock.sentinel.origin, None)
        nt.assert_raises(AssertionError, self.reader.process_data, mock.sentinel.origin, str())
        nt.assert_raises(AssertionError, self.reader.process_data, mock.sentinel.origin, int())
