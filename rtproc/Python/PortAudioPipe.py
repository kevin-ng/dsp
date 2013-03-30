# The code in this file is ported from the C++ code originally written by
# Paolo Prandoni and Martin Vetterli of the Ecole Polytechnique Federale
# de Lausanne.

import pyaudio
import select
import sys
import os
import struct
import wave
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
    def __init__(self, sound_file=None):
        self._sound_file = None
        self._pa = None
        self._istream = None
        self._ostream = None
        self._sample_block = 0.0
        self._sound_processor = None
        self._effect = None
        self._err = 0
        self._sound_file = sound_file
        self._frames_per_buffer = FRAMES_PER_BUFFER
 
    def initialize(self):
        # Initialize the PortAudio library
        self._pa = pyaudio.PyAudio()
        
        # If we have a sound file, set up the parameters here 
        if not self._sound_file == None:
            self._istream = wave.open(self._sound_file, 'rb')
            self._sample_rate = self._istream.getframerate()
            self._sample_size = 1
            self._frames_per_buffer = 1
            self._num_channels = self._istream.getnchannels()
            self._format = self._pa.get_format_from_width(self._istream.getsampwidth())
            if self._format == pyaudio.paUInt8:
                self._pack_format = 'B'
            elif self._format == pyaudio.paInt8:
                self._pack_format = 'b'                
            elif self._format == pyaudio.paInt16:
                self._pack_format = 'h'
            elif self._format == pyaudio.paInt24:
                # TODO
                pass
            elif self._format == pyaudio.paInt32:
                self._pack_format = 'i'
            elif self._format == pyaudio.paFloat32:
                self._pack_foramt = 'f'
        else:   
            self._sample_rate = 44100
            self._sample_size = 2
            self._frames_per_buffer = 4
            self._num_channels = 1
            self._format = pyaudio.paInt32
            self._pack_format = 'i'     
            self._istream = self._pa.open(
                                    channels=self._num_channels,
                                    format=self._format,
                                    rate=self._sample_rate,
                                    frames_per_buffer=self._frames_per_buffer,
                                    input=True)  
                        
        self._ostream = self._pa.open(
                            channels=self._num_channels,
                            format=self._format,
                            rate=self._sample_rate,
                            frames_per_buffer=self._frames_per_buffer,
                            output=True) 
        self._sample_block = [0.0] * self._frames_per_buffer * self._num_channels * self._sample_size
 
        # Set up the SoundProcessor
        self._sound_processor = SoundProcessor.SoundProcessor(SR=self._sample_rate)

    def _play_sample(self):
        try:
            if not self._sound_file == None:
                sample_block = self._istream.readframes(self._frames_per_buffer)
            else:
                sample_block = self._istream.read(self._frames_per_buffer)
            current_block = []
            for j in range(0,len(sample_block),self._frames_per_buffer):
                aux = long(struct.unpack(self._pack_format, sample_block[j:j+self._frames_per_buffer])[0])
                current_block = current_block + \
                    [struct.pack(self._pack_format, self._sound_processor.Process(float(aux)))]
            self._ostream.write(''.join(current_block), self._frames_per_buffer)
        except IOError as e:
            self._err = e.errno
            self.xrun()
        except struct.error:
            # Occasionally, a sample goes out of range for the struct.pack
            # function.  Rather than fail out, allow the processing to
            # continue, effectively throwing this sample out
            pass
        
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
                
        # Start the streams
        if self._sound_file == None:
            self._istream.start_stream()
        self._ostream.start_stream()
        
        # Loop until we're told to quit
        while True:
            key, _, _ = select.select([sys.stdin], [], [], 0)
            if key == []:
                self._play_sample()
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
                    if not self._sound_file == None:
                        self._istream.rewind()
        
    def stop(self):
        if not self._istream == None:
            if self._sound_file == None:
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
