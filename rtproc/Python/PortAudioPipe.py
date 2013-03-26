import pyaudio
import select
import sys
import os
import struct
import SoundProcessor

FRAMES_PER_BUFFER = 4
NUM_CHANNELS = 1
SAMPLE_SIZE = 2
SAMPLE_RATE = 44100
PA_SAMPLE_TYPE = pyaudio.paInt32

effects = {
            "0" : "Delta",
            "1" : "Echo",
            "2" : "IIR echo",
            "3" : "Natural Echo",
            "4" : "Reverb",
            "5" : "Biquad",
            "6" : "Fuzz",
            "7" : "Flanger",
            "8" : "Wah",
            "9" : "Tremolo"
           }

class PortAudioPipe:
    def __init__(self):
        self._pa = None
        self._istream = None
        self._ostream = None
        self._sample_block = 0.0
        self._sound_processor = None
        self._effect = None
        self._err = 0
            
    def initialize(self):
        self._sample_block = [0.0] * FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE
        
        # Initialize the PortAudio library
        self._pa = pyaudio.PyAudio()
        
        # Set up the SoundProcessor
        self._sound_processor = SoundProcessor.SoundProcessor(SR=SAMPLE_RATE)
        
    def start(self):        
        legal = False
        while not legal:
            self._print_options()
            effect = raw_input()
            if effect in effects.keys():
                self._effect = effect
                self._sound_processor.SetFunction(effect)
                self._print_options()
                legal = True
            else:
                print
                print "Please make a legal selection..."
                print
                print
        
        # Start the stream
        self._istream = self._pa.open(
                                channels=NUM_CHANNELS,
                                format=PA_SAMPLE_TYPE,
                                rate=SAMPLE_RATE,
                                frames_per_buffer=FRAMES_PER_BUFFER,
                                input=True)
        self._ostream = self._pa.open(
                                channels=NUM_CHANNELS,
                                format=PA_SAMPLE_TYPE,
                                rate=SAMPLE_RATE,
                                frames_per_buffer=FRAMES_PER_BUFFER,
                                output=True)
                
        self._istream.start_stream()
        self._ostream.start_stream()
        
        # Loop until we're told to quit
        while True:
            key, _, _ = select.select([sys.stdin], [], [], 0)
            if key == []:
                try:
                    sample_block = self._istream.read(FRAMES_PER_BUFFER)
                    current_block = []
                    for j in range(0,len(sample_block),FRAMES_PER_BUFFER):
                        aux = long(struct.unpack('i', sample_block[j:j+FRAMES_PER_BUFFER])[0])
                        current_block = current_block + [struct.pack('i', self._sound_processor.Process(float(aux)))]
                    self._ostream.write(''.join(current_block), FRAMES_PER_BUFFER)
                except IOError as e:
                    self._err = e.errno
                    self.xrun()
            else:
                effect = sys.stdin.read(1)
                if effect.upper() == 'Q':
                    print "Thanks for playing!"
                    self.stop()
                    break
                if effect in effects.keys():
                    self._effect = effect
                    self._sound_processor.SetFunction(effect)
                    self._print_options()
        
    def stop(self):
        if not self._istream == None:
            self._istream.stop_stream()
            self._istream.close()
        if not self._ostream == None:
            self._ostream.stop_stream()
            self._ostream.close()            
        if not self._pa == None:
            self._pa.terminate()
        
    def _print_options(self):
        def print_selector():
            print '[*]',

        os.system('cls' if os.name == 'nt' else 'clear')

        if self._effect == '0': print_selector()
        print "(0) " + effects['0']
        if self._effect == '1': print_selector()
        print "(1) " + effects['1']
        if self._effect == '2': print_selector()
        print "(2) " + effects['2']
        if self._effect == '3': print_selector()
        print "(3) " + effects['3']
        if self._effect == '4': print_selector()
        print "(4) " + effects['4']
        if self._effect == '5': print_selector()
        print "(5) " + effects['5']
        if self._effect == '6': print_selector()
        print "(6) " + effects['6']
        if self._effect == '7': print_selector()
        print "(7) " + effects['7']
        if self._effect == '8': print_selector()
        print "(8) " + effects['8']
        if self._effect == '9': print_selector()
        print "(9) " + effects['9']
        print "(Q) Quit"
        print
        print "Please make a selection: "
        
    def xrun(self):
        self.stop()
        if self._err == pyaudio.paInputOverflow:
            print "Input Overflow."
        if self._err == pyaudio.paOutputUnderflow:
            print "output Underflow."
