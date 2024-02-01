import threading
import socket
from config import DISCOVERY_PORT

servers_addr_list = []
servers_sk_list = []
leader_index = {"leader": None}

def create_client_socket(ip, port):
    remote_addr = (ip, int(port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(remote_addr)
    return client_socket


def discover_hosts():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(('0.0.0.0', DISCOVERY_PORT))
    try:
        print("Listening for broadcasts...")
        while True:
            data, addr = client_socket.recvfrom(1024)
            if data.decode() not in servers_addr_list:
                servers_addr_list.append(data.decode())
                sk = create_client_socket(data.decode().split(' ')[0], int(data.decode().split(' ')[1]))
                servers_sk_list.append(sk)
                print(servers_sk_list)
    except:
        pass

    finally:
        client_socket.close()


if __name__ == '__main__':
    discover_hosts_thread = threading.Thread(target=discover_hosts)
    discover_hosts_thread.start()





































# import threading
# import time
# import logging
# import socket
# import config

# logging.basicConfig(level=logging.getLevelName(config.LOG_LEVEL), format=config.LOG_FORMAT)

# class HeartbeatChecker:
#     def __init__(self):
#         self.server_heartbeats = {}
#         self.lock = threading.Lock()

#     def update_server_heartbeat(self, server_socket):
#         with self.lock:
#             self.server_heartbeats[server_socket] = time.time()
#             logging.info(f"Server heartbeat updated for {server_socket.getpeername()}")

#     def check_heartbeats(self):
#         current_time = time.time()
#         with self.lock:
#             to_remove_servers = [server_socket for server_socket, timestamp in self.server_heartbeats.items()
#                                  if current_time - timestamp > config.LEADER_HEARTBEAT_TIMEOUT]
#             for server_socket in to_remove_servers:
#                 logging.warning(f"Server {server_socket.getpeername()} timed out.")
#                 self.remove_server(server_socket)

#     def remove_server(self, server_socket):
#         with self.lock:
#             if server_socket in self.server_heartbeats:
#                 del self.server_heartbeats[server_socket]
#                 logging.info(f"Server {server_socket.getpeername()} removed from heartbeat tracking")

#     def is_leader_heartbeat_missing(self):
#         current_time = time.time()
#         with self.lock:
#             for _, timestamp in self.server_heartbeats.items():
#                 if current_time - timestamp <= config.LEADER_HEARTBEAT_TIMEOUT:
#                     return False
#             return True

#     def start_heartbeat_checking(self):
#         while True:
#             self.check_heartbeats()
#             time.sleep(config.HEARTBEAT_INTERVAL)

# def send_heartbeat(server_socket):
#     logging.info("Server heartbeat thread started")
#     while True:
#         try:
#             server_socket.sendall(b'HEARTBEAT')
#             time.sleep(config.HEARTBEAT_INTERVAL)
#         except (ConnectionResetError, BrokenPipeError, OSError) as e:
#             logging.error(f"Disconnected from the server. Stopping heartbeat. Error: {e}")
#             break
