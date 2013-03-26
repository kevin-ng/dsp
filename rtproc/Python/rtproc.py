# The code in this file is ported from the C++ code originally written by
# Paolo Prandoni and Martin Vetterli of the Ecole Polytechnique Federale
# de Lausanne.

import PortAudioPipe

if __name__ == '__main__':
    p = PortAudioPipe.PortAudioPipe()
    p.initialize()
    p.start()
