#ENCRYPTED CODE!
import socket
import threading

import rsa

#asking user choice to either host or to connect to a chat.
public_key, private_key = rsa.newkeys(1024) # we don't really have to create public n private key pair in every session
public_partner = None



choice = input("Would you make this terminal to host(1) or to connect(2)? Enter your Choice: ")

if choice == "1":
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(("192.168.0.203", 9999)) # Here change the ip-address to your system's ipaddress (in cmd ipconfig)
	server.listen()



	client, _= server.accept()
	#hosting client sends the key first
	client.send(public_key.save_pkcs1("PEM"))
	#receiveing key 
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("192.168.0.203", 9999))
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
	client.send(public_key.save_pkcs1("PEM"))
else:
	exit()


def sending_messages(c):
	while True:
		message = input("")
		c.send(rsa.encrypt(message.encode(), public_partner))
		print("You messaged: " + message)
		

def receiving_messages(c):
	while True:
		
		print("Your PARTNER messaged: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()



