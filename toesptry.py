import socket
import time

# Replace with the ESP8266's IP address on your network
esp8266_ip = "192.168.1.11"
esp8266_port = 8080

def on(s):
      # Send commands or data
      command = "ON ON ON ON"  # Example command
      s.sendall(command.encode())


def off(s):
    # Send commands or data
    command = "OFF OFF OFF OFF"  # Example command
    s.sendall(command.encode())

def listen(s):
  response = s.recv(1024)
  print(response)
  print("Received response:", response.decode())
  while "DDD" not in response:
    response = s.recv(1024)
    print(response)
    print("Received response:", response.decode())



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((esp8266_ip, esp8266_port))
  for i in range(10):
    on(s)
    # listen(s)
    time.sleep(1.1)
    off(s)
    # listen(s)
    time.sleep(1.1)

