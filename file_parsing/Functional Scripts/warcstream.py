import io
import gzip

class WarcStream(object):
    def __init__(self, filename):
        self.file = filename
        self.buffer = None
        self.finished = False
    
    def open(self):
        gz = gzip.open(self.file, 'rb')
        self.buffer = io.BufferedReader(gz)
        return self.buffer

    def header(self, data):
        return self.buffer.read(1024).decode('utf8', errors='ignore').split('\r\n\r\n')[0]

    # def readline(self, end):
    #     self.stream.readline().decode('utf8')

    def read(self, size):
        if self.buffer.read() == b'':
            self.finished = True
            return
        else:
            return self.buffer.read(size).decode('utf8', errors='ignore')
