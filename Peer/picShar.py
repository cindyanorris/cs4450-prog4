#!/usr/bin/python3

from ContactCentralServer import *
from ImageManager import *
from PeerClient import *
from PeerServer import *
import os    
import sys
#append .. to path to be able to find settings.py
sys.path.append("..")
import socket
import signal
import settings

#Takes the name of the image directory to be used
#by the peer and the seed directory containing the
#starting images.
#Deletes the images from the image directory and
#copies the images in the seed directory to the
#image directory.
def restart(imagedir, seeddir):
   #delete all of the images 
   print("Deleting images in the " + imagedir + " directory.")
   print("Copying images in the " + seeddir + " directory to the " + imagedir + " directory.")
   cont = input("Continue (y/n)? ")
   cont = cont.lower()
   if (cont != "y" and cont != "yes"):
      print("Aborting restart\n")
      sys.exit(0);
   imageman = ImageManager(imagedir, seeddir)
   imageman.restart()

#Contacts the central server to register the peer.
#Creates the peer client and the peer server which will run
#in separate threads.
def communicateWithPeers(centralServerName, centralServerPort, peerServerPort, \
                         peerServerID, imagedir):
   global centralServer
   global peerServer
   #connect to central server to add host and port to peer list
   centralServer = ContactCentralServer(centralServerName, centralServerPort, \
                                        peerServerPort, peerServerID)
   response = centralServer.connect()
   if (response.find("BAD") != -1):
      print(response[4:])
      print("Exiting")
      sys.exit(0)
   #Create an image manager object that will be passed to
   #both the peer client and the peer server.
   #The peer client will request images from a peer server.
   #The peer server will return requested images to a peer client.
   imageman = ImageManager(imagedir, "")
   peerClient = PeerClient(centralServer, peerServerPort, imageman)
   print("Peer server listening on port " + peerServerPort + ".\n")
   peerClient.start()  # start peer client thread
   peerServer = PeerServer(peerServerPort, imageman)
   peerServer.start()  # start peer server thread
   return peerClient

#print usage information
def printUsage():
   print("\nUsage: picShar.py <imagedir> [ <seeddir> restart | [<port>]]");
   print("<imagedir> - directory that contains the images to be shared");
   print("             and the images obtained from peers.");
   print("<port> - port number for server portion of picShar");
   print("         if port omitted, an ephemeral port is chosen by the OS");
   print("<seeddir> - directory that contains the peers original images");
   print("restart - removes the images from the <imagedir> directory");
   print("           copies images from <seeddir> directory to <imagedir> directory");
   print("Examples: ");
   print("picShar.py Images1 15001")
   print("picShar.py Images1");
   print("picShare.py Images1 Seed1 restart\n")

#check to see if a directory exists
def validDirectory(dirName):
   if (not os.path.exists(dirName)):
      print(dirName + " does not exist.")
      return False
   else:
      return True

#ask the OS for a free port
def getFreePort():
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
   sock.bind(('', 0))
   sock.listen(socket.SOMAXCONN)
   ipaddr, port = sock.getsockname()
   sock.close();
   return str(port)

#The user entered a restart command.
#Check to make sure the two directories exist and
#perform the restart.
def doRestart(args):
   #must be a restart command
   imagedir = args[1]
   seeddir = args[2]
   if (not validDirectory(imagedir) or not validDirectory(seeddir) or \
       args[3] != "restart"):
      printUsage()
      return
   else:
      restart(imagedir, seeddir)

#Get a port for the peer server port.
#Validate the image directory parameter.
#Start up the peer client and the peer server.
def doClientServer(args):
   if (len(args) == 2): 
       peerServerPort = getFreePort()
   else:
       peerServerPort = args[2]
   imagedir = args[1]
   #create an identifier to associate with the peer server
   peerServerID = socket.gethostname() + "_" + peerServerPort
   peerClient = communicateWithPeers(settings.centralServerName, \
                                     settings.centralServerPort, \
                                     peerServerPort, peerServerID, \
                                     imagedir)
   #wait until the peer client terminates
   peerClient.join()
   #Send a sigint signal to program so it will clean up the sockets
   os.kill(os.getpid(), signal.SIGINT) 


def main():
   if (len(sys.argv) == 4):
      #must be a restart command
      doRestart(sys.argv)
   elif (len(sys.argv) == 2 or len(sys.argv) == 3):  
      #must be a command to start the peer 
      doClientServer(sys.argv)
   else:
      printUsage()

#if the user types ctrl-C or quit at the > prompt, this
#signal handler will be executed which will disconnect this
#peer from the central server and close the peer server socket
def handleSIGINT(sig, frame):
   print("Closing listening socket and disconnecting from central server.")
   centralServer.disconnect()
   peerServer.terminate();
   sys.exit(0);

if __name__ == "__main__":
   #install the signal handler
   signal.signal(signal.SIGINT, handleSIGINT)
   main()          
