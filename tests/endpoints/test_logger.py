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

from talking_sockets.endpoints.logger import Logger
from unittest import mock
import nose.tools as nt


class TestLogger:

    def _udpate_n_times(self, n):
        logging_observer = Logger()
        nt.assert_equal(len(logging_observer.messages), 0)

        for i in range(n-1):
            emitter_attribute = getattr(mock.sentinel, 'emitter' + str(i))
            message_attribute = getattr(mock.sentinel, 'message' + str(i))

            logging_observer.update(emitter_attribute, message_attribute)

            nt.assert_equal(len(logging_observer.messages), i+1)
            nt.assert_equal(logging_observer.messages[i], (emitter_attribute, message_attribute))

    def test_update_n_times(self):
        for i in range(2):
            yield self._udpate_n_times, i+1