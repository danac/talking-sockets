import asyncio
import concurrent.futures


class ClientManager:
    """
    Implement a static interface to a register of references to objects.
    """

    #: Class-wide dictionary containing the registered objects, indexed by ``id()``.
    clients = dict()

    @classmethod
    def send_to_all(cls, message):
        """
        Calls the ``send_message`` method on all registered clients,
        passing them the message.

        :param bytes message: Bytes to send
        """
        for client in cls.clients.values():
            client.send_message(message)

    @classmethod
    def register(cls, instance):
        """
        Registers an object in the class-wide register.

        :param instance: Any object
        """
        key = id(instance)
        cls.clients[key] = instance

    @classmethod
    def unregister(cls, instance):
        """
        Removes an object from the class-wide register.

        :param instance: Any object
        """
        key = id(instance)
        cls.clients.pop(key)


class TCPBroadcastServerFactory(asyncio.Protocol):
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
        ClientManager.register(self)

    def connection_lost(self, exc):
        """
        End of connection callback.
        """
        print("connection_lost: {}".format(self.peer_name))
        ClientManager.unregister(self)

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

        # Create the server
        create_server_coro = self.loop.create_server(server_factory, port=port)
        self.loop.run_until_complete(create_server_coro)
        print("serving on port {}".format(port))

    @asyncio.coroutine
    def _serve(self):
        """
        Start the user input prompt in a separate thread and notify the server.
        """
        while True:
            input_value = yield from self.loop.run_in_executor(self.executor, input, "Send?")
            if input_value == '0':
                break

            ClientManager.send_to_all(self.value)

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