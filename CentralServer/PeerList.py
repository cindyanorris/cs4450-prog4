
class PeerList:

   #constructor
   def __init__(self):
      self.peerlist = []

   #add a peer (hostIP and port) to the list
   #of peers
   def add(self, hostIP, port, ID):
      newPeer = [hostIP, port, ID]
      if not self.peerInList(ID):
         self.peerlist.append(newPeer)  

   #returns True if the hostIP and port is
   #in the list of peers
   def peerInList(self, ID):
      for peer in self.peerlist:
          peerID = peer[2]
          if (peerID == ID):
             return True
      return False

   #removes the hostIP and port from the list of
   #peers
   def remove(self, ID):
      if self.peerInList(ID):
         for peer in self.peerlist:
            hostIP = peer[0]
            port = peer[1]
            peerID = peer[2]
            if (peerID == ID):
               self.peerlist.remove([hostIP, port, peerID])

   #return a string representation of the list of
   #peers
   def toString(self):
      peerStr = ""
      for peer in self.peerlist:
         peerStr += peer[0] + "," + str(peer[1]) + "," + peer[2] + "\n"         
      return peerStr

