#This class handles connection requests from peer clients and
#returns the list of images in its image directory and
#an image from the image directory.
import threading
import socket
import select


#This class inherits from threading.Thread the the run method
#runs in a thread.
class PeerServer(threading.Thread):

   #Create a listening socket
   #Initialize data members: stopper, imageman, and serverSocket
   def __init__(self, myport, imageman):
      threading.Thread.__init__(self)
      self.stopper = threading.Event()
      self.imageman = imageman;
      self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.serverSocket.setblocking(0)
      try:
         self.serverSocket.bind(('', int(myport)))
         self.serverSocket.listen(5)
      except Exception as e:
         print("\nUnable to bind to " + myport)
         self.stopper.set()

   #This method runs in a loop until stopper is set.
   #It accepts connection requests, responds to the message
   #received from the client, and closes the connection
   def run(self):
      readList = [self.serverSocket]
      #loop until stopper is set
      while not self.stopper.is_set():
         timeout = 1
         #The call to select times out after 1 second.  If there
         #is a connection request, readable contains a self.serverSocket
         readable, writable, errored = select.select(readList, [], [], 1)
         for s in readable:
            if s is self.serverSocket:
               connectionSocket, addr = self.serverSocket.accept()
               msg = connectionSocket.recv(1024).decode('utf-8');
               words = msg.split();
               if (words[0] == "LIST"):  #list images
                  response = "OK\n" + self.imageman.listImages();
                  response = response.encode('utf-8');
               elif (words[0] == "GET"): #get an image
                  if (len(words) < 1 or not self.imageman.hasImage(words[1])):
                     response = "BAD\n".encode('utf-8');
                  else:               
                     response = "OK\n".encode('utf-8') + self.imageman.getImage(words[1]);
               else:  #bad request
                  response = "BAD\n".encode('utf-8');
               connectionSocket.send(response);
               connectionSocket.close()
      self.serverSocket.close()
            

   #called to terminate the thread
   def terminate(self):
      self.stopper.set()
         
      
