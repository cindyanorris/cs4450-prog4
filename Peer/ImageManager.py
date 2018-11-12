import os     #for list directory and removing files
import shutil #for copying files

class ImageManager:
  
   #Create an ImageManager object providing an
   #image directory and a seed directory
   #The seed directory might be an empty string.
   #It is only needed if a restart is being performed.
   def __init__(self, imageDir, seedDir):
      self.imageDir = imageDir
      self.seedDir = seedDir

   #Restart cleans up the image directory by
   #deleting what is in there and copying the
   #files in the seed directory into the Images
   #directory.
   def restart(self):
      self.removeImages()
      self.copyImages()

   #Deletes the images in the image directory.
   def removeImages(self):
      files = os.listdir(self.imageDir)
      for f in files:
         os.unlink(self.imageDir + "/" + f)

   #Copies the images in the seed directory
   #into the images directory.
   def copyImages(self):
      files = os.listdir(self.seedDir)
      for f in files:
         shutil.copy(self.seedDir + "/" + f, self.imageDir)

   #Returns a string that is the concatenation of
   #the names of the files in the images directory.
   def listImages(self):
      files = os.listdir(self.imageDir)
      resultStr = ""
      for f in files:
         resultStr += f + "\n"
      if resultStr == "":
         resultStr = "No images\n"
      return resultStr

   #Returns true if the image directory contains
   #the file whose name is imagefile
   def hasImage(self, imagefile):
      path = self.imageDir + "/" + imagefile
      try:
         infile = open(path, "rb")
         infile.close()
         return True
      except Exception as e:
         return False

   #Returns the contents of an image in
   #the image directory or "" if the image
   #doesn't exist.
   def getImage(self, imagefile):
      path = self.imageDir + "/" + imagefile
      try:
         infile = open(path, "rb")
      except Exception as e:
         print("Unable to open " + path)
         return "".encode('utf-8')   
      body = infile.read()
      infile.close()
      return body

   #Stores the contents of an image in
   #the image directory
   def putImage(self, imagefile, content):
      path = self.imageDir + "/" + imagefile
      print("Writing to " + path)
      try:
         infile = open(path, "wb")
      except Exception as e:
         print("Unable to open " + path)
         return
      infile.write(content)
      infile.close()
