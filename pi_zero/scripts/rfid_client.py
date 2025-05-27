import socket
import time

# configure server info
IP = "192.168.1.128" # IP-adress of Pico W
PORT = 5000 # same port that Pico W listens to
BUFFER = 1024 # Max amount of bytes to receive for every transmission

# This is just simulation of RFID-data (replace this with real readings from the reader)

def get_rfid_data():
    return "rfid : RFID_TAG_ABC"

try: 
    # Create a TCP-client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print(f"Connected to the server on the adress: {IP}, PORT: {PORT}")
    while True:
        rfid_data = get_rfid_data()
        print(f"Sending RFID-data: {rfid_data}")
        client_socket.sendall(rfid_data.encode())
        
        response = client_socket.recv(BUFFER).decode()
        print(f"Response from the server: {response}")
        
        # Wait three seconds before next reading
        time.sleep(3)

except KeyboardInterrupt:
       print("\n[!] Interrupted by User.")

except ConnectionRefusedError:
    print(f"[X] Couldn't connect to the server on {IP}:{PORT}")

except Exception as e:
    print(f"[X] Error: {e}")

finally:
    client_socket.close()
    print("Connection to server closed.")


