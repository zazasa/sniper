import alsaaudio, wave, numpy
import threading,time
from datetime import datetime


class CaptureMic():
    

    def __init__(self):
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        self.inp.setchannels(1)
        self.inp.setrate(44100)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE) 
        self.inp.setperiodsize(1024)
        self.on = False
        self.writeMode = False
        self.buffsize = 2048
        self.buffer = [(0,0) for i in range(self.buffsize)]

        self.w = wave.open('test.wav', 'w')
        self.w.setnchannels(1)
        self.w.setsampwidth(2)
        self.w.setframerate(44100)


    def start(self):
        self.on = True
        self.t = threading.Thread(target = self.capture)
        self.t.daemon = True
        self.t.start()


    def capture(self):
        while self.on:
                l, data = self.inp.read()
                a = numpy.fromstring(data, dtype='int16')
                a = numpy.abs(a).mean()
                self.buffer.pop(0)
                self.buffer.append((datetime.now().isoformat(),a))
                if self.writeMode:
                     self.w.writeframes(data)
                    

                  
    def getBuffer(self):
        return self.buffer        

    def stop(self):
        self.on = False
        self.t.join()

    def setWriteMode(self,flag):
        self.writeMode = flag

if __name__ == "__main__":
    mc = CaptureMic()
    mc.start()
    while 1:
        time.sleep(1)

    
