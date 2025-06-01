import socket
import time
import sys
import logging
import os

# 🧹 Function for cleaning loggs automatically
def truncate_log_file(log_path, max_lines=20):
    if not os.path.isfile(log_path):
        return
    with open(log_path, "r") as f:
        lines = f.readlines()
    if len(lines) > max_lines:
        with open(log_path, "w") as f:
            f.writelines(lines[-max_lines:]) 

# 📄 Configure logging to file
logging.basicConfig(
    filename='/home/pi/RnD/Gabbemannen00/pi_zero/scripts/auto_client.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function that search for TCP-Connection
def search_for_TCP(server_ip, server_port, timeout=30):
    logging.info("⏳ Waiting for the server to become available...")
    start_time = time.time() # start timer
    attempts = 0
    while True: 
        try:
            sock = socket.create_connection((server_ip, server_port), timeout=2)
            sock.close()
            logging.info("✅ TCP-server is available!")
            return True
        # after 30 seconds of attempting to connect, Return False
        except (ConnectionRefusedError, OSError):
            if time.time() - start_time > timeout:
                logging.error("❌ TCP-server did not respond after 30 seconds of waiting.")
                return False
            # Track how many times the loop restarts
            attempts+=1
            time.sleep(1)

# Function that starts the client
def start_client():
    # call the clean log function to clean big amount of logs from previous executions
    truncate_log_file("/home/pi/RnD/Gabbemannen00/pi_zero/scripts/auto_client.log", max_lines=20)
    
    # Define the TCP-servers IP-adress and portnumber
    server_ip = "192.168.1.128" 
    server_port = 5000 
    # exit the program if a connection hasn't happened before the timeout
    if not search_for_TCP(server_ip, server_port):
        sys.exit(1) # ❌ Exit the program with errorcode 1    
        
    try: 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        time.sleep(1) # wait a one second before sending the message to TCP, for better flow.
        client_socket.sendall(b"client functional!")
        data = client_socket.recv(1024)
        logging.info("✅ TCP: message was received!")
        logging.info("💬 TCP: %s", data.decode())
        client_socket.close()
        sys.exit(0) # Exit the program with code 0
    except Exception as e:
        logging.error("❌ Connection error: %s", str(e))    
        sys.exit(1) # Error during the connection, quit with errorcode 1
if __name__ == "__main__":
    start_client() 
