def string_to_byte(message):
  message_as_bytes = str.encode(message)
  type(message_as_bytes)
  return message_as_bytes 

def byte_to_string(message):
  respond = message.decode()
  type(respond) # ensure it is string representation
  return respond

def test(xd):
  print(xd)