import socket
import threading
from threading import Thread
import time
import DataBase
from Connection.Connected import Connected
from Connection.Disconnected import Disconnected


class ConnectionHandler:
    def __init__(self, database: DataBase):
        self.database = database
        self.socket = None
        self._running = True
        self.connection_lock = threading.RLock()
        self.connected, self.lostConnection = threading.Condition(self.connection_lock), threading.Condition(self.connection_lock)
        self._connection_maintainer = Thread(target=self.connection_loop)
        self._connection_maintainer.start()
        self.setup_handlers()

    def setup_handlers(self):
        @self.database.event("stop")
        def handle_stop():
            self.stop()

    def __del__(self):
        self.stop()

    def connection_loop(self):
        while self._running:
            if not self.database.scada_connected:
                with self.connection_lock:
                    try:
                        self.connect()
                        self.connected.notify_all()
                        self.lostConnection.wait()
                        self.disconnect()
                    except Exception as e:
                        print(f"Connection error: {e}")
                        self.disconnect()
                        time.sleep(0.5)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.socket.connect(('127.0.0.1', int(self.database.base_info["num_port"])))
        self.database.update_connection_status(Connected())

    def request(self, request):
        response = None
        with self.connection_lock:
            try:
                self.socket.send(request)
                response = self.socket.recv(1024)
            except:
                self.disconnect()
                self.lostConnection.notify_all()
        return response

    def disconnect(self):
        try:
            self.socket.close()
        except:
            pass
        self.database.update_connection_status(Disconnected())

    def stop(self):
        self._running = False
        with self.connection_lock:
            self.lostConnection.notify_all()
            self.connected.notify_all()
        try:
            self.socket.close()
        except:
            pass
        self._connection_maintainer.join()