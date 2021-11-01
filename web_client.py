from twisted.internet.selectreactor import SelectReactor
from twisted.internet.protocol import Protocol,ClientFactory
from twisted.protocols.basic import LineReceiver
import os
from struct import *
 
reactor = SelectReactor()
protocol = Protocol()
prepare = 0
filename = ""
sourceDir = 'client'
recvBuffer = ''
 
def delete_file_folder(src):
  '''delete files and folders'''
  if os.path.isfile(src):
    try:
      os.remove(src)
    except:
      pass
  elif os.path.isdir(src):
    for item in os.listdir(src):
      itemsrc = os.path.join(src,item)
      delete_file_folder(itemsrc) 
    try:
      os.rmdir(src)
    except:
      pass
 
def clean_file_folder(src):
  '''delete files and child folders'''
  delete_file_folder(src)
  os.mkdir(src)
 
def writefile(filename,data):
  print ('write file size:::::::::',len(data))
  fp = open(filename,'a+b')
  fp.write(data)
  fp.close()
 
class QuickDisconnectedProtocol(Protocol):
  def connectionMade(self):
    print ("Connected to %s."%self.transport.getPeer().host)
    self.transport.write("Hello server, I am the client!\r\n")
  def dataReceived(self, line):
    global prepare
    global filename
    global sourceDir
    global recvBuffer
 
    recvBuffer = recvBuffer + line
    self.processRecvBuffer()
 
  def processRecvBuffer(self):
    global prepare
    global filename
    global sourceDir
    global recvBuffer
 
    while len(recvBuffer) > 0 :
      index1 = recvBuffer.find('CMB_BEGIN')
      index2 = recvBuffer.find('CMB_END')
 
      if index1 >= 0 and index2 >= 0:
        line = recvBuffer[index1+9:index2]
        recvBuffer = recvBuffer[index2+7:]
 
        if line == 'Sync':
          clean_file_folder(sourceDir)
 
        if line[0:3] == "End":
          prepare = 0
        elif line[0:5] == "File:":
          name = line[5:]
          filename = os.path.join(sourceDir, name)
          print ('mk file:',filename)
          prepare = 1
        elif line[0:7] == "Folder:":
          name = line[7:]
          filename = os.path.join(sourceDir, name)
          print ('mkdir:',filename)
          os.mkdir(filename)
        elif prepare == 1:
          writefile(filename,line)
      else:
        break 
 
class BasicClientFactory(ClientFactory):
  protocol=QuickDisconnectedProtocol
  def clientConnectionLost(self,connector,reason):
    print ('Lost connection: %s'%reason.getErrorMessage())
    reactor.stop()
  def clientConnectionFailed(self,connector,reason):
    print ('Connection failed: %s'%reason.getErrorMessage())
    reactor.stop()
 
reactor.connectTCP('localhost',1234,BasicClientFactory())
reactor.run()