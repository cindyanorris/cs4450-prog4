#This class is incomplete.

#The peer client class contains the code that allows a
#user to communicate with other peers, getting the list of
#images and getting images.

import threading
import socket
import os
import signal

#This classes inherits from threading.Thread and the run
#method runs in a thread.
class PeerClient(threading.Thread):
   def __init__(self, centralServer, myport, imageman):
      threading.Thread.__init__(self)
      self.centralServer = centralServer
      self.imageman = imageman
      self.myIPAddr = socket.gethostname()
      hostname = socket.gethostname()    
      IPAddr = socket.gethostbyname(hostname)    
      self.myIPAddr = IPAddr
      self.myport = myport

   #prints usage information
   def printUsage(self):
      print("peers - list the peers")
      print("images <n> - list the images on peer <n>")
      print("get <image> <n> - get the images from peer <n>")
      print("quit")

   #run method executes code in a loop 
   #until the user enters quit.  It
   #display the prompt, reads the user's input, and
   #response to the user's input.
   def run(self):
      self.printUsage()
