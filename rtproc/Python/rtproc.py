# The code in this file is ported from the C++ code originally written by
# Paolo Prandoni and Martin Vetterli of the Ecole Polytechnique Federale
# de Lausanne.

import PortAudioPipe
import sys

if __name__ == '__main__':
    sound_file = None
    if len(sys.argv) > 1:
        sound_file = sys.argv[1]

    p = PortAudioPipe.PortAudioPipe(sound_file)
    p.initialize()
    p.start()
