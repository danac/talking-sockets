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
from talking_sockets.router import Router
from talking_sockets.observer import LoggingObserver, Observable


class ObservableLogger(LoggingObserver, Observable):
    pass


class TestRouter:

    @classmethod
    def setUpClass(cls):
        cls.message = os.urandom(10)

    def setUp(self):
        self.router = Router()
        self.sink_endpoint = LoggingObserver()
        self.source_endpoint = Observable()
        self.endpoint = ObservableLogger()

    @nt.raises(NotImplementedError)
    def test_add_observer(self):
        self.router.add_observer(self.sink_endpoint)

    @nt.raises(NotImplementedError)
    def test_notify(self):
        self.router.notify(bytes())

    def test_add_sink_endpoint(self):
        self.router.add_sink_endpoint(self.sink_endpoint)
        assert self.sink_endpoint in self.router.observers

    def test_add_source_endpoint(self):
        self.router.add_source_endpoint(self.source_endpoint)
        assert self.router in self.source_endpoint.observers

    def test_add_endpoint(self):
        self.router.add_endpoint(self.endpoint)
        assert self.endpoint in self.router.observers

    def test_update_source_to_sink(self):
        self.router.add_sink_endpoint(self.sink_endpoint)
        self.router.add_source_endpoint(self.source_endpoint)

        nt.assert_equal(len(self.sink_endpoint.messages), 0)
        self.source_endpoint.notify(self.message)

        nt.assert_equal(len(self.sink_endpoint.messages), 1)
        nt.assert_equal(self.sink_endpoint.messages[0], (self.router, self.message))

    def test_update_endpoint_to_sink(self):
        self.router.add_endpoint(self.endpoint)
        self.router.add_sink_endpoint(self.sink_endpoint)

        nt.assert_equal(len(self.endpoint.messages), 0)
        nt.assert_equal(len(self.sink_endpoint.messages), 0)
        self.endpoint.notify(self.message)

        nt.assert_equal(len(self.endpoint.messages), 0)
        nt.assert_equal(len(self.sink_endpoint.messages), 1)
        nt.assert_equal(self.sink_endpoint.messages[0], (self.router, self.message))