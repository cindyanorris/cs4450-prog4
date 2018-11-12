
import socket

#This class allows the peer to:
#1) connect to the central server to add peer to list of peers
#2) disconnect from the central server to remove peer from list of peers
#3) get a list of peers from the central server
class ContactCentralServer:
   def __init__(self, centralServerName, centralServerPort, \
                      peerServerPort, peerServerID):
      self.centralServerName = centralServerName
      self.centralServerPort = centralServerPort
      self.peerServerPort = peerServerPort
      self.peerServerName = socket.gethostname()
      self.peerServerID = peerServerID

   #Sends a connect message to the central server with the host name
   #of this peer and the port it is listening on
   def connect(self):
      #connect
      try:
         #use the port that the server will listen on
         centralServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         centralServerSocket.bind(('', int(self.peerServerPort)))
         centralServerSocket.connect((self.centralServerName, self.centralServerPort))
      except Exception as e:
         return "BAD\nUnable to reach central server"
      #Send message and receive response.
      #The message contains an ID for the peer server.
      #The server itself determines the address of the client.
      msg = "CONNECT\n" + self.peerServerID + "\n"
      centralServerSocket.send(msg.encode('utf-8'))
      response = centralServerSocket.recv(1024).decode('utf-8')
      centralServerSocket.close() 
      if (response == "BAD"):
         return "BAD\nBad port number. Perhaps it is already in use."
      else:
         return "OK\n" 

   #Sends a disconnect message to the central server with the ID
   #of the peer server to remove
   def disconnect(self):
      #connect
      try:
         centralServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         centralServerSocket.connect((self.centralServerName, self.centralServerPort))
      except Exception as e:
         return "BAD\nUnable to reach central server"
      #send message and receive response
      msg = "DISCONNECT\n" + self.peerServerID + "\n"
      centralServerSocket.send(msg.encode('utf-8'))
      response = centralServerSocket.recv(1024).decode('utf-8')
      centralServerSocket.close() 
      return "OK\n"

   #Sends a get message to the central server in order to get a list
   #of the peers. Each peer is identified by a hostname, the
   #the port it is listening on, and the peer server ID.
   def getPeers(self):
      #connect
      try:
         centralServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         centralServerSocket.connect((self.centralServerName, self.centralServerPort))
      except Exception as e:
         return "BAD\nUnable to reach central server"
      #send message and receive response
      msg = "GET\n"
      centralServerSocket.send(msg.encode('utf-8'))
      responseAll = ""
      while 1:
         response = centralServerSocket.recv(1024).decode('utf-8')
         if not response: break
         responseAll += response;
      return self.parseResponse(responseAll)

   #Parse the response received from the central server.
   #Returns a list of each peer server IP and port, excluding
   #the peer with the ID self.peerServerID
   def parseResponse(self, responseAll):
      response = "OK\n"
      peers = responseAll.split()
      for peer in peers:
         if (peer != "OK" and peer.find(self.peerServerID) == -1):
            pieces = peer.split(",")
            response += pieces[0] + "," + pieces[1] + "\n"
      return response

