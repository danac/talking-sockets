#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Dana Christen
#
# This file is part of XpenseMate, a tool for managing shared expenses and
# hosted at https://github.com/danac/xpensemate.
#
# XpenseMate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import nose.tools as nt
from talking_sockets.observer import Observable, Observer


class DummyObserver(Observer):

    def __init__(self):
        self.emitter = None
        self.message = None
        self.updated = False

    def update(self, emitter, message):
        self.updated = True
        self.emitter = emitter
        self.message = message


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
        self.observable.notify("")

        assert self.observer.updated is True

    def test_remove_observer(self):
        self.observable.add_observer(self.observer)
        self.observable.remove_observer(self.observer)
        self.observable.notify("")

        assert self.observer.updated is False

    @nt.raises(AssertionError)
    def test_add_invalid_observer(self):
        class FakeObserver:
            pass

        fake_observer = FakeObserver()

        self.observable.add_observer(fake_observer)

    @nt.raises(AssertionError)
    def test_remove_missing_observer(self):
        self.observable.remove_observer(self.observer)

    def test_notify_emitter(self):
        pass

    def test_notify_message(self):
        pass
