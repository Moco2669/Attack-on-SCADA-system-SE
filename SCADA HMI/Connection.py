import socket
import threading
from threading import Thread
import time
import DataBase


class ConnectionHandler:
    def __init__(self, database: DataBase):
        self.database = database
        self.socket = None
        self.connection_running = True
        self.isConnected = False
        self.connection_lock = threading.RLock()
        self.connected, self.lostConnection = threading.Condition(self.connection_lock), threading.Condition(self.connection_lock)
        self.running_lock = threading.RLock()
        self.running_notify = threading.Condition(self.running_lock)
        self._connection_maintainer = Thread(target=self.connection_loop)
        self._connection_maintainer.start()

    def __del__(self):
        self.connection_running = False
        try:
            self.socket.close()
        except Exception as e:
            print(f"Error closing socket: {e}")
        self._connection_maintainer.join()


    def connection_loop(self):
        while self.connection_running:
            if not self.isConnected:
                with self.connection_lock:
                    try:
                        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                        self.socket.connect(('127.0.0.1', int(self.database.base_info["num_port"])))
                        self.isConnected = True
                        self.connected.notify_all()
                        self.lostConnection.wait()
                        self.isConnected = False
                    except Exception as e:
                        print(f"Connection error: {e}")
                        self.isConnected = False
                        time.sleep(0.5)

    def request(self, request):
        response = None
        with self.connection_lock:
            try:
                self.socket.send(request)
                response = self.socket.recv(1024)
            except:
                self.isConnected = False
                self.lostConnection.notify_all()
        return response

    def stop(self):
        self.connection_running = False
        self.isConnected = False
        with self.connection_lock:
            self.lostConnection.notify_all()
            self.connected.notify_all()
        try:
            self.socket.close()
        except:
            pass
        self._connection_maintainer.join()