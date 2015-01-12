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

import nose.tools as nt
from unittest import mock
from talking_sockets.observer import Observable, Observer


class DummyObserver(Observer):

    def update(self, emitter, message):
        pass


class TestObservable:

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.observable = Observable()
        self.observer = DummyObserver()

    def tearDown(self):
        pass

    def test_add_observer(self):
        self.observable.add_observer(self.observer)
        assert self.observer in self.observable.observers

    def test_remove_observer(self):
        self.observable.observers.append(self.observer)
        self.observable.remove_observer(self.observer)
        assert self.observer not in self.observable.observers

    @nt.raises(AssertionError)
    def test_add_invalid_observer(self):
        class FakeObserver:
            pass

        fake_observer = FakeObserver()
        self.observable.add_observer(fake_observer)

    @nt.raises(AssertionError)
    def test_remove_missing_observer(self):
        self.observable.remove_observer(self.observer)

    def test_notify(self):
        self.observable.observers.append(self.observer)
        with mock.patch.object(DummyObserver, 'update') as patched_update:
            message = mock.sentinel.message
            self.observable.notify(message)
            patched_update.assert_called_once_with(self.observable, message)



class TestObserver:

    @nt.raises(TypeError)
    def test_abstract_update(self):

        class InvalidObserver(Observer):
            pass

        InvalidObserver()

