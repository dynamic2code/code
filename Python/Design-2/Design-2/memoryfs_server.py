import pickle, logging
import argparse
import time
import dbm
import os.path

global DELAYAT, Get_Put_REQUEST_COUNT, INITDBM, DBMFILE
# For locks: RSM_UNLOCKED=0 , RSM_LOCKED=1 
RSM_UNLOCKED = bytearray(b'\x00') * 1
RSM_LOCKED = bytearray(b'\x01') * 1
DELAYAT = None
Get_Put_REQUEST_COUNT = 0
INITDBM = 0
DBMFILE = None

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

class DiskBlocks():
  def __init__(self, total_num_blocks, block_size):
    # This class stores the raw block array
    self.block = []
    # Initialize raw blocks 
    for i in range (0, total_num_blocks):
      Putdata = bytearray(block_size)
      self.block.insert(i,Putdata)
      #self.block[i] = Putdata

if __name__ == "__main__":

  # Construct the argument parser
  ap = argparse.ArgumentParser()

  ap.add_argument('-nb', '--total_num_blocks', type=int, help='an integer value')
  ap.add_argument('-bs', '--block_size', type=int, help='an integer value')
  ap.add_argument('-port', '--port', type=int, help='an integer value')
  ap.add_argument('-delayat', '--delayat', type=int, help='an integer value')
  ap.add_argument('-initdbm', '--initdbm', type=int, help='an integer value')
  ap.add_argument('-dbmfile', '--dbmfile', type=str, help='a string value')

  args = ap.parse_args()

  if args.total_num_blocks:
    TOTAL_NUM_BLOCKS = args.total_num_blocks
  else:
    print('Must specify total number of blocks') 
    quit()

  if args.block_size:
    BLOCK_SIZE = args.block_size
  else:
    print('Must specify block size')
    quit()

  if args.port:
    PORT = args.port
  else:
    print('Must specify port number')
    quit()

  if args.delayat:
    DELAYAT = args.delayat

  if args.initdbm:
    INITDBM = args.initdbm

  if args.dbmfile:
    DBMFILE = args.dbmfile

  # initialize blocks
  RawBlocks = DiskBlocks(TOTAL_NUM_BLOCKS, BLOCK_SIZE)
  #global INITDBM, DBMFILE
  if DBMFILE:           
    storage = dbm.open(DBMFILE, 'c')
    if INITDBM == 1:
      for i in range (0, TOTAL_NUM_BLOCKS):
        #print (bytearray(0), type(bytearray(0)), bytes(bytearray(0)), bytes(0), len(bytes(0)), len(bytearray(0)))
        storage[f"{i}"] = bytes(0)
    #else: 
    #  for i in range (0, TOTAL_NUM_BLOCKS):
    #    #print (bytearray(0), type(bytearray(0)), bytes(bytearray(0)), bytes(0), len(bytes(0)), len(bytearray(0)))
    #    storage[f"{i}"] = bytes(0)
    #print (storage["1"])

  # Create server
  server = SimpleXMLRPCServer(("127.0.0.1", PORT), requestHandler=RequestHandler) 

  def sleep_10():
    global DELAYAT, Get_Put_REQUEST_COUNT
    if DELAYAT:
      Get_Put_REQUEST_COUNT += 1
      if DELAYAT == Get_Put_REQUEST_COUNT:
        time.sleep(10)
        Get_Put_REQUEST_COUNT = 0

  def Get(block_number):
    global DBMFILE
    sleep_10()
    result = RawBlocks.block[block_number]
    #print ("Get-----", result, block_number, type(result), type(block_number), len(result))
    if DBMFILE:
      result = storage[str(block_number)]
      #print ("Get len", len(result))
      if len(result) == 0:
        result = bytes(BLOCK_SIZE)
      #print ("Get-----", bytes(BLOCK_SIZE), block_number, type(result), type(block_number), len(result))
      #  print ("Get", RawBlocks.block[block_number], storage[str(block_number)])
    return result

  server.register_function(Get)

  def Put(block_number, data):
    sleep_10()
    RawBlocks.block[block_number] = data.data
    if DBMFILE:
      #print ("in Put", data.data, type(data.data), block_number)
      storage[str(block_number)] = data.data
    return 0

  server.register_function(Put)

  def RSM(block_number):
    result = RawBlocks.block[block_number]
    # RawBlocks.block[block_number] = RSM_LOCKED
    RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01'))
    if DBMFILE:
      #print ("RSM-----------------")
      result = storage[str(block_number)]
      if len(result) == 0:
        result = bytes(BLOCK_SIZE)      
      storage[str(block_number)] = bytes(bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01')))
    return result

  server.register_function(RSM)

  # Run the server's main loop
  print ("Running block server with nb=" + str(TOTAL_NUM_BLOCKS) + ", bs=" + str(BLOCK_SIZE) + " on port " + str(PORT))
  server.serve_forever()