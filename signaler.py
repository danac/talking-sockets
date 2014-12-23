import asyncio
import concurrent.futures


class BroadcastServer(asyncio.Protocol):
    clients = dict()

    def __init__(self):
        self.transport = None
        self.fd = None
        self.peer_name = None

    def connection_made(self, transport):
        self.transport = transport
        self.peer_name = transport.get_extra_info("peername")
        self.fd = self.peer_name[1]
        print("connection_made: {}".format(self.peer_name))
        self.clients[self.fd] = self

    def connection_lost(self, ex):
        print("connection_lost: {}".format(self.peer_name))
        self.clients.pop(self.fd)


class Signaler:
    def __init__(self, port=1234):
        self.loop = asyncio.get_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.value = b"tick\n"
        self.port = port

        self.loop.run_until_complete(self._initialize_server())

    @asyncio.coroutine
    def _initialize_server(self):
        server = yield from self.loop.create_server(BroadcastServer, port=self.port)
        for socket in server.sockets:
            print("serving on {}".format(socket.getsockname()))

    @asyncio.coroutine
    def _serve(self):
        while True:
            input_value = yield from self.loop.run_in_executor(self.executor, input, "Send?")
            if input_value == '0':
                break

            for fd, client in BroadcastServer.clients.items():
                client.transport.write(self.value)

    def run(self):
        print("starting up..")

        try:
            self.loop.run_until_complete(self._serve())
        except KeyboardInterrupt:
            pass
        finally:
            print("shutting down..")
            self.loop.close()


if __name__ == '__main__':
    Signaler().run()