import socket
import threading
import _thread
import utils
import requests

f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)
print(MY_IP)
MY_PORT = 12345


def server_thread_tcp(MY_IP, MY_PORT):
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
        print(message)

server_thread_tcp(MY_IP, MY_PORT)