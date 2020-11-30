import socket
import select
import errno
from colorama import init, Fore, Back, Style
import socket
import threading
import os
import time
import sys

init(convert=True)

print(Fore.CYAN +"""
                                _
                             ,:'/   _..._
                            // ( `""-.._.'
                            \| /    6\___
                            |     6      4
                            |            /
                            \_       .--'
                            (_'---'`)
                            / `'---`()
                          ,'        |
         ,            .'`          |
         )\       _.-'             ;
        / |    .'`   _            /
       /` /   .'       '.        , |
      /  /   /           \   ;   | |
      |  \  |            |  .|   | |
       \  `"|           /.-' |   | |
        '-..-\       _.;.._  |   |.;-.
              \    <`.._  )) |  .;-. ))
              (__.  `  ))-'  \_    ))'
                  `'--"`       `--"
                  
    ███╗   ███╗ █████╗ ████████╗██╗  ██╗
    ████╗ ████║██╔══██╗╚══██╔══╝██║  ██║
    ██╔████╔██║███████║   ██║   ███████║
    ██║╚██╔╝██║██╔══██║   ██║   ██╔══██║
    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  Ampernic`s fork (Psinamper server core)""" + Fore.WHITE)

time.sleep(2)
os.system('cls||clear')

print(Fore.CYAN + """
    ███╗   ███╗ █████╗ ████████╗██╗  ██╗
    ████╗ ████║██╔══██╗╚══██╔══╝██║  ██║
    ██╔████╔██║███████║   ██║   ███████║
    ██║╚██╔╝██║██╔══██║   ██║   ██╔══██║
    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """
    Version: Alpha 1_1.0.1
    Author: Wiskey666
    Forked by: Ampernic
    Mail: ampernic@list.ru
    DS: ampernic#9787""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """

    This is a console chat for special lovers of this shit.
    The chat will be improved (both the client side and the server side).
    Thank you for noticing and trying it!
""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """
    """+ Fore.WHITE)

# Connection Data
try:
    host = input('    Set host IP: ')
    if host == '':
        print(Fore.YELLOW + "\n    [!]  Please enter IP!")
        time.sleep(5)
        sys.exit() 
except:
    print(Fore.YELLOW + "\n    [!]  Invalid address format!")
    time.sleep(5)
    sys.exit() 

try:
    port = int(input('    Set host port: '))
except ValueError:
    print(Fore.YELLOW + "\n    [!]  Port must be an integer!")
    time.sleep(5)
    sys.exit() 
    
channel_name = "#" + input('    Set channel name: ')
ver= 'Alpha 1_1.0.1'

print("\33[90m" + """
    -----------------------------------"""+ Fore.WHITE)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((host, port))
except:
    print(Fore.YELLOW + "\n    [!]  The given IP or port is busy!")
    time.sleep(5)
    sys.exit() 
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Client Kick Function   
def close_client(client):
    clients.remove(client)
    client.close()

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('[-] {} left the server!'.format(nickname).encode('utf-8'))
            print(Fore.YELLOW + "[-] {} left the server!".format(nickname))
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(Fore.YELLOW +"[+] Connected with {}".format(str(address)) + Fore.WHITE)

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        client_ver = client.recv(1024).decode('utf-8')
        clients.append(client)
       
        # Checking Nickname
        if nickname in nicknames:
            print("    Nickname is {}".format(nickname) + Fore.RED + " (ALREADY EXISTS!)" + Fore.WHITE)
            # If Old - Kick Him
            if client in clients:
                client.send("[-] You have been kicked from the server! Code 401".encode('utf-8'))
                close_client(client)
            check_ver(client_ver, ver, client, clients, nickname, address)
            broadcast('[!] {} try to connect again... Already exist!'.format(nickname).encode('utf-8'))
            print(Fore.YELLOW + "[!] {} {} kicked from the server! Already exist.".format(nickname, str(address)) + Fore.WHITE)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
        else:
            print("    Nickname is {}".format(nickname))
            nicknames.append(nickname)
            is_normal = check_ver(client_ver, ver, client, clients, nickname, address)
            if is_normal == True:
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
                client.send("[+] Connected to {}!".format(channel_name).encode('utf-8'))
                broadcast("[+] {} joined!".format(nickname).encode('utf-8'))    
            
# Checking Version Function
def check_ver(client_ver, ver, client, clients, nickname, address):
        if client_ver == ver:
            # If All Is Good - Go Next
            print("    Client version: " + client_ver)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            return True
        else:
            print("    Client version: " + client_ver + Fore.RED + " (TOO OLD!)" + Fore.WHITE)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            # If Old - Kick Him
            if client in clients:
                print(Fore.YELLOW + "[-] {} {} kicked from the server! Too old version.".format(nickname, str(address)) + Fore.WHITE)
                client.send("[-] You have been kicked from the server! Code 409".encode('utf-8'))
                close_client(client)
                broadcast('[-] {} kicked from the server! Too old version.'.format(nickname).encode('utf-8'))
                print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            nicknames.remove(nickname)
            return False

#Start Listening
receive()


