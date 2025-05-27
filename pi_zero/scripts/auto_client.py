import socket

def start_client():
    # Create a socket connection for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the TCP-servers IP-adress and portnumber
    server_ip = "192.168.1.128" 
    server_port = 5000 
    
    # Try to connect to the server
    try:
        client_socket.connect((server_ip, server_port))
        
        # Send a message automatically when the TCP-server connects
        client_socket.sendall(b"Hello from auto_client!")
        
        # Receive data from TCP
        data = client_socket.recv(1024)
        print(f"TCP: Hello Client!, your message was received, thank you.")

    except ConnectionRefusedError:   
        print("Couldn't connect to the server.")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client() 
