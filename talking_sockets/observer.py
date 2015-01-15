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


class Observer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, emitter, message):  # pragma: no cover
        pass


class Observable:

    def __init__(self, **kwargs):
        self.observers = []

    def add_observer(self, observer):
        assert issubclass(observer.__class__, Observer)
        self.observers.append(observer)

    def remove_observer(self, observer):
        assert issubclass(observer.__class__, Observer),\
            "Observer object doesn't implement the right interface."
        try:
            self.observers.remove(observer)
        except ValueError:
            raise AssertionError("Observer not registered.")

    def notify(self, message):
        for observer in self.observers:
            observer.update(self, message)
    