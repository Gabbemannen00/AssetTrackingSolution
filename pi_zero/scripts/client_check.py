import socket #Import the socket-module for the networkcommunication 

# Configure variables
SERVER_IP = "192.168.1.128" # IP-adress to the server stored on Pico W
SERVER_PORT = 5000 # The portnumber that the server is listening to
BUFFER_SIZE = 1024 # Max amount of data to receive each time sent, in bytes
MESSAGES = ["Hello Pico W!",",nice to see you.","Im Pi Zero."] # Messages

try:
    # Create a TCP-socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server with its IP-adress and portnumber
    client_socket.connect((SERVER_IP, SERVER_PORT))
    # Print the Servers ip-adress and portnumber when connected
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    print("")
    
    # Send messages from the list one after the other
    for message in MESSAGES:
        # convert the string to bytes and send it to the server
        client_socket.sendall(message.encode())

        # Print the message that was sent from client 
        print(f"Sent to Pico W: {message}")
       
        # Wait for a response from the server
        response = client_socket.recv(BUFFER_SIZE).decode()
        # when response occur, print the response from the server
        print(f"Received from Pico W: {response}")
        print("") # Make some space between each send and receive moment for a more readable code

except ConnectionRefusedError:
    # handles errors if the server isnt available
    print(f"Could not connect to the server at {SERVER_IP}:{SERVER_PORT}")

except Exception as e:
    # handles other unexpected errors
    print(f"Error: {e}")

finally:
    # Shut the connection when everything is done
    client_socket.close()
    print("Connection closed.")
