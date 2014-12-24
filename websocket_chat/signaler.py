import asyncio
import concurrent.futures


class ClientManager:
    """
    Interface allowing a child class to register itself in a static register,
    which can then be used to loop over all registered instances.
    """

    #: Class-wide dictionary containing the registered instances, indexed by ``id()``.
    clients = dict()

    @classmethod
    def send_to_clients(cls, message):
        """
        Calls the ``send_message`` method on all registered clients,
        passing them the message.

        :param bytes message: Bytes to send
        """
        for client in cls.clients.values():
            client.send_message(message)

    def _register_connection(self):
        """
        Registers the instance in the class-wide register.
        """
        key = id(self)
        ClientManager.clients[key] = self

    def _unregister_connection(self):
        """
        Removes the instance from the class-wide register.
        """
        key = id(self)
        ClientManager.clients.pop(key)


class TCPBroadcastServerFactory(asyncio.Protocol, ClientManager):
    """
    Async TCP server factory that automatically (un-)registers client connections.
    """

    def __init__(self):
        self.transport = None
        self.peer_name = None

    def connection_made(self, transport):
        """
        New connection callback.
        """
        self.transport = transport
        self.peer_name = transport.get_extra_info("peername")
        print("connection_made: {}".format(self.peer_name))
        self._register_connection()

    def connection_lost(self, exc):
        """
        End of connection callback.
        """
        print("connection_lost: {}".format(self.peer_name))
        self._unregister_connection()

    def send_message(self, message):
        """
        Write to the client connection.

        :param bytes message: Bytes to send
        """
        self.transport.write(message)


class Signaler:
    """
    Connect a user input prompt to a server, broadcasting a message to the client whenever
    the user hits return. To prevent blocking the event loop, the user prompt runs in a separate
    thread.
    """

    def __init__(self, server_factory=TCPBroadcastServerFactory, port=1234):
        self.loop = asyncio.get_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.value = b"tick\n"
        self.port = port
        self.server_factory = server_factory

        self.loop.run_until_complete(self._initialize_server())

    @asyncio.coroutine
    def _initialize_server(self):
        """
        Co-routine used to create the server.
        """
        yield from self.loop.create_server(self.server_factory, port=self.port)

        print("serving on port {}".format(self.port))

    @asyncio.coroutine
    def _serve(self):
        """
        Start the user input prompt in a separate thread and notify the server.
        """
        while True:
            input_value = yield from self.loop.run_in_executor(self.executor, input, "Send?")
            if input_value == '0':
                break

            self.server_factory.send_to_clients(self.value)

    def run(self):
        """
        Start the event loop
        """
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