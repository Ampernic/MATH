# Imports
import sys
import socket
import select
import errno
from colorama import init, Fore, Back, Style
import socket
import threading
import time
import os

from win10toast import ToastNotifier

# Inits
toaster = ToastNotifier()
init(convert=True)

# Logo
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
    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  Ampernic`s fork (Psinamper client)""" + Fore.WHITE)

time.sleep(2)
os.system('cls||clear')

# Info
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

# Client Settings
IP = input('    IP: ')
PORT = int(input('    Port: '))
ver = "Alpha 1_0.6.5"

# Choosing Nickname
nickname = input('    Username: ')

print("""
    -----------------------------------    
""")
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')
            
            #Version Check
            #If Server Sends Conflict Code - Kick
            if "Code 409" in message:
                print(Fore.GREEN +'░' + Fore.YELLOW + '░' + Fore.GREEN + '░ ' + Fore.WHITE + message)
                client.close()
                break
            else:
                # If 'NICK' Send Nickname
                if message == 'NICK':
                    client.send(nickname.encode('utf-8'))
                    client.send(ver.encode('utf-8'))
                else:
                    print(Fore.GREEN +'░' + Fore.YELLOW + '░' + Fore.GREEN + '░ ' + Fore.WHITE + message)
                    #Check For New Messages
                    if "<"+ nickname +">" in message or "[+]" in message or "[-]" in message:
                        continue
                    else:
                       toaster.show_toast("MATH", message, threaded=True)
        except:
            # Close Connection When Error 
            print(Fore.GREEN +'>' + Fore.YELLOW + '>' + Fore.GREEN + '> ' + Fore.RED + "[-] An error occured!")
            client.close()
            break
        
# Sending Messages To Server
def write():
    while True:
        try:
            message_text = input('')
            # Check for blank massage
            if message_text == '':
                continue
            else:
                message = '<{}> {}'.format(nickname, message_text)
                client.send(message.encode('utf-8'))
        except:
            pass

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

