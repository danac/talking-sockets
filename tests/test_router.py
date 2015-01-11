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
from talking_sockets.router import Router
from talking_sockets.observer import Observable


class TestRouter:

    @classmethod
    def setUpClass(cls):
        cls.message = os.urandom(10)

    def setUp(self):
        self.router = Router()

    @nt.raises(NotImplementedError)
    def test_add_observer(self):
        self.router.add_observer(mock.sentinel.something)

    @nt.raises(NotImplementedError)
    def test_notify(self):
        self.router.notify(mock.sentinel.something)

    def test_add_sink_endpoint(self):
        with mock.patch.object(Observable, 'add_observer') as patched_add_observer:
            self.router.add_sink_endpoint(mock.sentinel.sink_endpoint)
            patched_add_observer.assert_called_once_with(mock.sentinel.sink_endpoint)

    def test_add_source_endpoint(self):
        source_endpoint = mock.Mock()
        self.router.add_source_endpoint(source_endpoint)
        source_endpoint.add_observer.assert_called_once_with(self.router)

    def test_add_endpoint(self):
        with mock.patch.object(Router, 'add_source_endpoint') as patched_add_source, \
                mock.patch.object(Router, 'add_sink_endpoint') as patched_add_sink:
            self.router.add_endpoint(mock.sentinel.endpoint)
            patched_add_source.assert_called_once_with(mock.sentinel.endpoint)
            patched_add_sink.assert_called_once_with(mock.sentinel.endpoint)

    def test_update_observer_updated(self):
        observer1 = mock.Mock()
        observer2 = mock.Mock()
        self.router.observers.append(observer1)
        self.router.observers.append(observer2)

        self.router.update(mock.sentinel.emitter, mock.sentinel.message)

        observer1.update.assert_called_once_with(mock.sentinel.emitter, mock.sentinel.message)
        observer2.update.assert_called_once_with(mock.sentinel.emitter, mock.sentinel.message)

    def _test_update_observable_itself_not_updated(self):
        observer1 = mock.Mock()
        observer2 = mock.Mock()
        self.router.observers.append(observer1)
        self.router.observers.append(observer2)

        self.router.update(observer1, mock.sentinel.message)

        assert observer1.update.called is False
        observer2.update.assert_called_once_with(mock.sentinel.emitter, mock.sentinel.message)
