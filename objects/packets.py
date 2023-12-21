import sys
sys.path.append("..")
import settings
import struct
import random
class Packet:
    '''
    Packet object, initialize with (source, destination, data)
    source: IPv4 address string, e.g, "127.0.0.1"
    destination: IPv4 address string, e.g., "53.23.0.21"
    data: random data within 65495 bytes.
    '''
    def __init__(self, src, dst, data):
        self.version = 4
        self.headL = 5
        self.serviceType = 0
        self.totalL = 0
        self.identification = 0
        self.DF = 1
        self.MF = 0
        self.fragmentOffset = 0
        self.TTL = settings.TTL
        self.proc = 6
        self.checksum = 0
        self.source = src
        self.destination = dst
        #self.options = 0 # No options or padding
        #self.padding = 0
        self.data = data
        self.packet = None
    def packetization(self):
        header = bytes()
        header += struct.pack("!c", (self.version * 16 + self.headL).to_bytes(1, byteorder='big'))
        self.totalL = len(self.data) + self.headL * 4
        self.identification = random.randint(0, 65536)
        header += struct.pack("!cHHH", self.serviceType.to_bytes(1, byteorder="big"), self.totalL, self.identification, 64)
        header += struct.pack("!cc", self.TTL.to_bytes(1, byteorder="big"), self.proc.to_bytes(1, byteorder="big"))
        
        src = bytes(map(int, self.source.split('.')))
        dst = bytes(map(int, self.destination.split('.')))

        self.checksum = self.cal_checksum(header + src + dst)
        header += struct.pack("!H", self.checksum)
        header += src
        header += dst
        
        header += self.data
        return header


    # calculate checksum
        
    def cal_checksum(self, data):
        words = [data[i:i+2] for i in range(0, len(data), 2)]
        checksum = 0

        # Iterate through each 16-bit word
        for word in words:
            # Convert the 16-bit word to an integer
            value = int.from_bytes(word, byteorder='big')
            
            # Add the value to the checksum
            checksum += value

        # Take the one's complement of the checksum
        checksum = checksum & 0xFFFF  # Keep only the 16 least significant bits
        checksum = ~checksum & 0xFFFF  # Take the one's complement

        return checksum


myobj = Packet("127.0.0.1", "237.132.222.8", "hello world".encode(encoding='utf-8'))
packet = myobj.packetization()
print(packet)
