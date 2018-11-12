#!/usr/bin/python3

import signal
import sys
#append .. to path to be able to find settings.py
sys.path.append("..") 
import socket
import settings
from PeerList import *

#process message from client
#should be GET, CONNECT, or DISCONNECT
def processMessage(msg, peerlist, addr):
   #split on white space
   words = msg.split();   
   if (len(words) == 0):
      return "BAD\n"
   if (words[0] == "GET"):
      return processGet(words, peerlist)
   elif (words[0] == "CONNECT" and len(words) == 2):
      return processConnect(peerlist, addr, words[1])
   elif (words[0] == "DISCONNECT" and len(words) == 2):
      return processDisconnect(peerlist, words[1])
   else:
      return "BAD\n"

#return to client the list of peers
#return either "BAD\n" or "OK\n" + list of peers
def processGet(words, peerlist):
   if (len(words) != 1 or words[0] != "GET"):
      return "BAD"
   else:
      return "OK\n" + peerlist.toString()

#add client to list of peers
#peerlist contains current list of peers
#addr contains ip and port tuple
#return "BAD" if failed or "OK" if successful
def processConnect(peerlist, addr, ID):
   hostIP = addr[0]
   port = addr[1]
   if (peerlist.peerInList(ID)):
      return "BAD";
   peerlist.add(hostIP, port, ID)
   return "OK\n" 

#remove client from list of peers
#peerlist contains current list of peers
#addr contains ip and port tuple
#return "BAD" if failed or "OK" if successful
def processDisconnect(peerlist, ID):
   if (not peerlist.peerInList(ID)):
      return "BAD\n";
   peerlist.remove(ID)
   return "OK\n" 

#signal handler that is executed if user types
#a ctrl-C
def handleSIGINT(sig, frame):
   print("Closing listening socket and terminating.")
   serverSocket.close();
   sys.exit(0);

#register signal handler
#if the user types a types a ctrl-c, the signal
#handler will be executed which will close the socket
signal.signal(signal.SIGINT, handleSIGINT)

#first create the listening socket for connection requests
serverPort = settings.centralServerPort
serverHost = settings.centralServerName
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(1)
print("The server is listening on " + str(serverPort))

peers = PeerList()

while True:
   #accept the connection request
   connectionSocket, addr = serverSocket.accept()

   #receive the message
   msg = connectionSocket.recv(1024);

   #build and send the response
   response = processMessage(msg.decode('utf-8'), peers, addr);
   connectionSocket.send(response.encode('utf-8'))

   #close the connection
   connectionSocket.close()

