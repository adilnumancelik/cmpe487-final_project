import sender
import utils

SERVER_IP = "52.203.72.10"
PORT = 12345

message = "keko değilsin"
sender.send_message(SERVER_IP, PORT, message)