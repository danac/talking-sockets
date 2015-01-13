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
from unittest import mock
from talking_sockets.buffered_reader import BufferedReader


class DummyStreamReader(BufferedReader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def message_ready(self, message):  # pragma: no cover
        pass


class TestBufferedReader:

    def setUp(self):
        self.reader = DummyStreamReader()

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
            message = os.urandom(10)
            self.reader.process_data(message)
            patched_message_ready.assert_called_once_with(message)

    def test_process_data_empty_message(self):
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader.process_data(bytes())
            assert patched_message_ready.called is False

    def test_process_data_delimited_one_packet_partial_chunk(self):
        message = b"part1|part2|half-part"
        delimiter = b"|"
        expected_notifications = message.split(delimiter)[:2]
        expected_calls = [mock.call(arg) for arg in expected_notifications]
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader.set_input_delimiter(delimiter)
            self.reader.process_data(message)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls)

    def test_process_data_delimited_two_packets_full_chunk(self):
        message1 = b"part1|part2|half-part"
        message2 = b"-second-half-part|part4|"
        delimiter = b"|"
        expected_notifications = [b"part1", b"part2", b"half-part-second-half-part", b"part4"]
        expected_calls = [mock.call(arg) for arg in expected_notifications]
        with mock.patch.object(self.reader, 'message_ready') as patched_message_ready:
            self.reader.set_input_delimiter(delimiter)
            self.reader.process_data(message1)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls[:2])
            self.reader.process_data(message2)
            nt.assert_equal(patched_message_ready.call_args_list, expected_calls)


    def test_process_data_wrong_data_type(self):
        nt.assert_raises(AssertionError, self.reader.process_data, None)
        nt.assert_raises(AssertionError, self.reader.process_data, str())
        nt.assert_raises(AssertionError, self.reader.process_data, int())
