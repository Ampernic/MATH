import socket
import select
import errno
from colorama import init, Fore, Back, Style
import socket
import threading
import os
import time

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
    Version: Alpha 1_0.6.5
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
host= input('    Set host IP: ')
port= int(input('    Set host port: '))
channel_name = "#" + input('    Set channel name: ')
ver= 'Alpha 1_0.6.5'

print("\33[90m" + """
    -----------------------------------"""+ Fore.WHITE)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

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
        nicknames.append(nickname)
        clients.append(client)
       

        # Print And Broadcast Nickname
        print("    Nickname is {}".format(nickname))
        # Checking Version
        if client_ver == ver:
            print("    Client version: " + client_ver)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            broadcast("[+] {} joined!".format(nickname).encode('utf-8'))
            client.send("[+] Connected to {}!".format(channel_name).encode('utf-8'))
        else:
            print("    Client version: " + client_ver + Fore.RED + " (TOO OLD!)" + Fore.WHITE)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)
            client.send("[-] You have been kicked from the server! Code 409".encode('utf-8'))
            
        # Check Version Of Client
        if client_ver == ver:
            # If All Is Good - Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            # If Old - Kick Him
            broadcast('[-] {} kicked from the server! Too old version.'.format(nickname).encode('utf-8'))
            print(Fore.YELLOW + "[-] {} kicked from the server! Too old version.".format(nickname) + Fore.WHITE)
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            print("\33[90m" + """    -----------------------------------"""+ Fore.WHITE)

#Start Listening
receive()


