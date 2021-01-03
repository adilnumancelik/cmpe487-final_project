import socket
import os
import threading
import _thread
import server.utils

MY_IP = a
MY_PORT = b

def server_thread_tcp():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    server.bind((MY_IP, MY_PORT)) 
    server.listen()
    while(1):
      conn, addr = server.accept() 
      with conn:
        data = conn.recv(1024)
        if not data:
          continue

        message = utils.byte_to_string(data)
        threading.Thread(target=respond_function, args=(message, ), daemon=True).start()