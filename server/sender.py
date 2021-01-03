import socket
import threading
import _thread
import utils

def send_message_thread(receiver_ip_send, message):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
      server.settimeout(5.0)
      server.connect((receiver_ip_send, 12345))
      print("Send: " + message)
      server.sendall(utils.string_to_byte(message))
      print("Sent Successfully")
    except:
     # remove(receiver_ip_send)
      server.close()
      print(":(")

send_message_thread("188.3.160.244", "keko2")
