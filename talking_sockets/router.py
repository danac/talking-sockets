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


class Router(Observer, Observable):

    def __init__(self):
        super().__init__()

    def add_observer(self, observer):
        raise NotImplementedError("This method should not be called directly, use add_sink_endpoint(endpoint) instead.")

    def add_sink_endpoint(self, endpoint):
        super().add_observer(endpoint)

    def add_source_endpoint(self, endpoint):
        endpoint.add_observer(self)

    def add_endpoint(self, endpoint):
        self.add_sink_endpoint(endpoint)
        self.add_source_endpoint(endpoint)

    def notify(self, message):
        raise NotImplementedError("This method should not be called from this class.")

    def update(self, emitter, message):
        for observer in self.observers:
            if observer is not emitter:
                observer.update(self, message)
