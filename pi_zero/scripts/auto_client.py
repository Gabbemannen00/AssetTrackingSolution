import socket
import time

def start_client():
    
    # Define the TCP-servers IP-adress and portnumber
    server_ip = "192.168.1.128" 
    server_port = 5000 
    while True:
        try:
            # Create a socket connection for the client
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            # Bind the port and the ip-adress  
            client_socket.connect((server_ip, server_port))
        
            # Send a message automatically when the TCP-server connects
            client_socket.sendall(b"auto_client responding!")
        
            # Receive data from TCP
            data = client_socket.recv(1024)
            print(f"TCP: Hello Client!, your message was received, thank you.")           
            break 

        except ConnectionRefusedError:   
            print("Couldn't connect to the server. Retrying in 3s...")
            time.sleep(3)
    
        finally:
            client_socket.close()

if __name__ == "__main__":
    time.sleep(1.5) # wait a little before running again
    start_client() 
