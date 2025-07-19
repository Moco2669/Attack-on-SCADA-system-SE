import csv
import socket
import threading
from abc import ABC, abstractmethod

class ModbusMockServer(ABC):
    def __init__(self, host='127.0.0.1', port=25252):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.server_thread = None
        self.client_thread = None
        self.write_requests = []
        self.write_requests_lock = threading.RLock()
        self.write_requests_condition = threading.Condition(self.write_requests_lock)

        self.analog_read = 0x04
        self.digital_read = 0x01
        self.digital_write = 0x05

    @abstractmethod
    def handle_request(self, request):
        pass

    def client_handler(self, conn):
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break

                response = self.handle_request(data)
                if response:
                    conn.sendall(response)
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            print("Client disconnected.")
            conn.close()

    def start(self):
        self.write_requests = []
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Mock server started on {self.host}:{self.port}")
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()


    def run_server(self):
        try:
            print("Waiting for client connection...")
            conn, addr = self.server_socket.accept()
            print("Client connected from:", addr)
            self.client_thread = threading.Thread(target=self.client_handler, args=(conn,))
            self.client_thread.start()
        except:
            if self.running:
                raise

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.server_thread:
            self.server_thread.join()
        if self.client_thread:
            self.client_thread.join()
        print("Mock server FULLY stopped.")

    def store(self, request):
        with self.write_requests_lock:
            self.write_requests.append(request)
            self.write_requests_condition.notify_all()

class NormalTemperature(ModbusMockServer):
    def handle_request(self, request):
        if len(request) < 8:
            return b''

        function_code = request[7]

        if function_code == self.analog_read:
            response = bytearray(request[:5])
            response.extend(b'\x05d\x04\x02\x01\x1a')
            return bytes(response)
        elif function_code == self.digital_read:
            response = bytearray(request[:5])
            response.extend(b'\x04d\x01\x01\x00')
            return bytes(response)
        elif function_code == self.digital_write:
            self.store(request)
            response = bytearray(request)
            return bytes(response)

        return b''

class HighTemperature(ModbusMockServer):
    def handle_request(self, request):
        if len(request) < 8:
            return b''

        function_code = request[7]

        if function_code == self.analog_read:
            response = bytearray(request[:5])
            response.extend(b'\x05d\x04\x02\x01m')
            return bytes(response)
        elif function_code == self.digital_read:
            response = bytearray(request[:5])
            response.extend(b'\x04d\x01\x01\x01')
            return bytes(response)
        elif function_code == self.digital_write:
            self.store(request)
            response = bytearray(request)
            return bytes(response)

        return b''

class LowTemperature(ModbusMockServer):
    def handle_request(self, request):
        if len(request) < 8:
            return b''

        function_code = request[7]

        if function_code == self.analog_read:
            response = bytearray(request[:5])
            response.extend(b'\x05d\x04\x02\x00-')
            return bytes(response)
        elif function_code == self.digital_read:
            response = bytearray(request[:5])
            response.extend(b'\x04d\x01\x01\x00')
            return bytes(response)
        elif function_code == self.digital_write:
            self.store(request)
            response = bytearray(request)
            return bytes(response)

        return b''

class NormalState(ModbusMockServer):
    def __init__(self):
        super().__init__()
        self.temperature = 260

    def handle_request(self, request):
        if len(request) < 8:
            return b''

        function_code = request[7]

        if function_code == self.analog_read:
            self.temperature += 5
            response = bytearray(request[:5])
            response.extend(b'\x05d\x04\x02')
            packed_bytes = bytearray([
                (self.temperature >> 8) & 0xFF,
                self.temperature & 0xFF
            ])
            response.extend(packed_bytes)
            return bytes(response)
        elif function_code == self.digital_read:
            response = bytearray(request[:5])
            response.extend(b'\x04d\x01\x01\x00')
            return bytes(response)
        elif function_code == self.digital_write:
            response = bytearray(request)
            return bytes(response)

        return b''

class CommandInjection(ModbusMockServer):
    def __init__(self):
        super().__init__()
        self.temperature = 350
        self.control_rods = 1

    def handle_request(self, request):
        if len(request) < 8:
            return b''

        function_code = request[7]

        if function_code == self.analog_read:
            self.temperature += 5
            response = bytearray(request[:5])
            response.extend(b'\x05d\x04\x02')
            packed_bytes = bytearray([
                (self.temperature >> 8) & 0xFF,
                self.temperature & 0xFF
            ])
            response.extend(packed_bytes)
            return bytes(response)
        elif function_code == self.digital_read:
            response = bytearray(request[:5])
            response.extend(b'\x04d\x01\x01\x00')
            return bytes(response)
        elif function_code == self.digital_write:
            response = bytearray(request)
            return bytes(response)

        return b''
