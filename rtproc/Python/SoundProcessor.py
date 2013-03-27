# The code in this file is ported from the C++ code originally written by
# Paolo Prandoni and Martin Vetterli of the Ecole Polytechnique Federale
# de Lausanne.

from math import pi, cos

BUF_LEN=60000
BUF_MASK=BUF_LEN
    
class SoundProcessor:
    def __init__(self, SR=44100, Ix=0, Iy=0, effect=0):
        self._SR = SR
        self._Ix = Ix
        self._Iy = Iy
        self._effect = effect
        
        self._pX = [0.0] * BUF_LEN
        self._pY = [0.0] * BUF_LEN
        
    def _core_process(self):
        y = 0.0
        if self._effect == '1':
            y = self._echo()
        elif self._effect == '2':
            y = self._IIR_echo()
        elif self._effect == '3':
            y = self._natural_echo()
        elif self._effect == '4':
            y = self._reverb()
        elif self._effect == '5':
            y = self._bi_quad()
        elif self._effect == '6':
            y = self._fuzz()
        elif self._effect == '7':
            y = self._flanger()
        elif self._effect == '8':
            y = self._wah()
        elif self._effect == '9':
            y = self._tremolo()
        else:
            y = self._delta()
        
        return y
        
    def SetFunction(self, effect):
        self._effect = effect
        self._Ix = 0
        self._Iy = 0
        self._pX = [0] * BUF_LEN
        self._pY = [0] * BUF_LEN   
        
    def Process(self, sample):
        # push input sample up input buffer
        self._pX[self._Ix] = sample
        
        y = self._core_process()
        
        # push output sample up output buffer
        self._pY[self._Iy] = y
        
        # increment indices
        self._Ix = (self._Ix + 1) % BUF_MASK
        self._Iy = (self._Iy + 1) % BUF_MASK
        
        return y
    
    def _delta(self):
        return self._pX[self._Ix]
    
    def _echo(self):
        # Set up the "static" method variables
        if "a" not in self._echo.__dict__:
            self._echo.__dict__['a'] = 1.0
        if "b" not in self._echo.__dict__:
            self._echo.__dict__['b'] = 0.7
        if "c" not in self._echo.__dict__:
            self._echo.__dict__['c'] = 0.5
        if "norm" not in self._echo.__dict__:
            self._echo.__dict__['norm'] = 1.0 / \
                (self._echo.__dict__['a'] + self._echo.__dict__['b'] + self._echo.__dict__['c'])
        if "N" not in self._echo.__dict__:
            self._echo.__dict__['N'] = int(0.3 * self._SR)
            
        # y[n] = (ax[n] + bx[n-N] + cx[n-2N]) / (a+b+c)
        return self._echo.__dict__['norm'] * \
            ( self._echo.__dict__['a'] * \
                self._pX[self._Ix] + \
              self._echo.__dict__['b'] * \
                self._pX[(self._Ix + BUF_LEN - self._echo.__dict__['N']) % BUF_MASK] + \
              self._echo.__dict__['c'] * \
                self._pX[(self._Ix + BUF_LEN - 2*self._echo.__dict__['N']) % BUF_MASK] )

    def _IIR_echo(self):
        # Set up the "static" method variables
        if "a" not in self._IIR_echo.__dict__:
            self._IIR_echo.__dict__['a'] = 0.7
        if "norm" not in self._IIR_echo.__dict__:
            self._IIR_echo.__dict__['norm'] = 1.0 - \
                self._IIR_echo.__dict__['a'] * self._IIR_echo.__dict__['a']
        if "N" not in self._IIR_echo.__dict__:
            self._IIR_echo.__dict__['N'] = int(0.3 * self._SR)
            
        # y[n] = x[n] * ay[n-N]
        return self._IIR_echo.__dict__['norm'] * \
            ( self._pX[self._Ix] + \
              self._IIR_echo.__dict__['a'] * \
                self._pY[(self._Iy + BUF_LEN - self._IIR_echo.__dict__['N']) % BUF_MASK])
               
    def _natural_echo(self):
        # Set up the "static" method variables
        if "a" not in self._natural_echo.__dict__:
            self._natural_echo.__dict__['a'] = 0.7
        if "norm" not in self._natural_echo.__dict__:
            self._natural_echo.__dict__['norm'] = 1.0 / (1.0 + self._natural_echo.__dict__['a'])
        if "N" not in self._natural_echo.__dict__:
            self._natural_echo.__dict__['N'] = int(0.3 * self._SR)
            
        # y[n] = x[n] + y[n-N] * h[n], h[n] leaky integrator
        return self._natural_echo.__dict__['norm'] * \
            ( self._pX[self._Ix] - \
            self._natural_echo.__dict__['a'] * \
                self._pX[(self._Ix + BUF_LEN - 1) % BUF_MASK] + \
            self._natural_echo.__dict__['a'] * \
                self._pY[(self._Iy + BUF_LEN - 1) % BUF_MASK] + \
            (1.0 - self._natural_echo.__dict__['a']) * \
                self._pY[(self._Iy + BUF_LEN - self._natural_echo.N) % BUF_MASK] )
                
    def _reverb(self):
        # Set up the "static" method variables
        if "a" not in self._reverb.__dict__:
            self._reverb.__dict__['a'] = 0.8
        if "norm" not in self._reverb.__dict__:
            self._reverb.__dict__['norm'] = 1.0
        if "N" not in self._reverb.__dict__:
            self._reverb.__dict__['N'] = int(0.02 * self._SR)
            
        # y[n] = -ax[n] x[n-N] + ay[n-N]
        return self._reverb.__dict__['norm'] * \
            ( -self._reverb.__dict__['a'] * 
                self._pX[self._Ix] + \
              self._pX[(self._Ix + BUF_LEN - self._reverb.__dict__['N']) % BUF_MASK] + \
              self._reverb.__dict__['a'] * \
                self._pY[(self._Iy + BUF_LEN - self._reverb.__dict__['N']) % BUF_MASK] )
            
    def _bi_quad(self):
        # Set up the "static" method variables
        if "pm" not in self._bi_quad.__dict__:
            self._bi_quad.__dict__['pm'] = 0.98                # pole magnitude
        if "pp" not in self._bi_quad.__dict__:
            self._bi_quad.__dict__['pp'] = 0.1 * pi            # pole phase
        if "zm" not in self._bi_quad.__dict__:
            self._bi_quad.__dict__['zm'] = 0.9                 # zero magnitude
        if "zp" not in self._bi_quad.__dict__:
            self._bi_quad.__dict__['zp'] = 0.06 * pi           # zero phase
        if "norm" not in self._bi_quad.__dict__:
            self._bi_quad.__dict__['norm'] = 0.5
                    
        # y[n] = x[n] + b_1x[n-1] + b_2x[n-2] - a_1y[n-1] - a_2y[n-2]
        b1 = -2.0 * self._bi_quad.__dict__['zm'] * cos(self._bi_quad.__dict__['zp'])
        b2 = self._bi_quad.__dict__['zm'] * self._bi_quad.__dict__['zm']
        a1 = -2.0 * self._bi_quad.__dict__['pm'] * cos(self._bi_quad.__dict__['pp'])
        a2 = self._bi_quad.__dict__['pm'] * self._bi_quad.__dict__['pm']
        
        return self._bi_quad.__dict__['norm'] * \
            ( self._pX[self._Ix] + \
              b1 * self._pX[(self._Ix + BUF_LEN - 1) % BUF_MASK] + \
              b2 * self._pX[(self._Ix + BUF_LEN - 2) % BUF_MASK] - \
              a1 * self._pX[(self._Iy + BUF_LEN - 1) % BUF_MASK] - \
              a2 * self._pX[(self._Iy + BUF_LEN - 2) % BUF_MASK] )
             
    def _fuzz(self):
        # Set up the "static" method variables
        if "T" not in self._fuzz.__dict__:
            self._fuzz.__dict__['T'] = 500.0
        if "G" not in self._fuzz.__dict__:
            self._fuzz.__dict__['G'] = 5.0
        if "limit" not in self._fuzz.__dict__:
            self._fuzz.__dict__['limit'] = 32767.0 * self._fuzz.__dict__['T']
                    
        # y[n] = a trunc(x[n] / a)
        y = self._pX[self._Ix]
        if y > self._fuzz.__dict__['limit']:
            y = self._fuzz.__dict__['limit']
        if y < -self._fuzz.__dict__['limit']:
            y = -self._fuzz.__dict__['limit']
            
        return self._fuzz.__dict__['G'] * y
    
    def _tremolo(self):
        # Set up the "static" method variables
        if "phi" not in self._tremolo.__dict__:
            self._tremolo.__dict__['phi'] = 5.0 * 2.0 * pi / self._SR    # 1Hz LFO
        if "omega" not in self._tremolo.__dict__:
            self._tremolo.__dict__['omega'] = 0.0
                        
        # y[n] = (1 + cos(wn)x[n])
        self._tremolo.__dict__['omega'] = \
            self._tremolo.__dict__['omega'] + self._tremolo.__dict__['phi']
        return (1.0 + cos(self._tremolo.__dict__['omega']) / 2.0) * self._pX[self._Ix]

    def _flanger(self):
        # Set up the "static" method variables
        if "N" not in self._flanger.__dict__:
            self._flanger.__dict__['N'] = int(0.002 * self._SR)
        if "FD" not in self._flanger.__dict__:
            self._flanger.__dict__['FD'] = 2.0
        if "phi" not in self._flanger.__dict__:
            self._flanger.__dict__['phi'] = 1.0 * 2.0 * pi / self._SR
        if "omega" not in self._flanger.__dict__:
            self._flanger.__dict__['omega'] = 0.0
                    
        d = int(self._flanger.__dict__['N'] * \
                self._flanger.__dict__['FD'] * \
                (1.0 + cos(self._flanger.__dict__['omega'])) / 2.0)
        self._flanger.__dict__['omega'] = self._flanger.__dict__['omega'] + \
            self._flanger.__dict__['phi']
        return 0.5 * \
            (self._pX[self._Ix] + self._pX[(self._Ix + BUF_LEN - d) % BUF_MASK])
         
    def _wah(self):
        # Set up the "static" method variables
        if "delta" not in self._wah.__dict__:
            self._wah.__dict__['delta'] = 0.3 * pi                 # max pole deviation
        if "phi" not in self._wah.__dict__:
            self._wah.__dict__['phi'] = 3.0 * 2.0 * pi / self._SR  # LFO frequency
        if "omega" not in self._wah.__dict__:
            self._wah.__dict__['omega'] = 0.0
        if "pm" not in self._wah.__dict__:
            self._wah.__dict__['pm'] = 0.99                        # pole magnitude
        if "pp" not in self._wah.__dict__:
            self._wah.__dict__['pp'] = 0.04 * pi                   # pole phase
        if "zm" not in self._wah.__dict__:
            self._wah.__dict__['zm'] = 0.9                         # zero magnitude
        if "zp" not in self._wah.__dict__:
            self._wah.__dict__['zp'] = 0.06 * pi                   # zero phase
                        
        d = self._wah.__dict__['delta'] * \
            (1.0 + cos(self._wah.__dict__['omega'])) / 2.0
        self._wah.__dict__['omega'] = self._wah.__dict__['omega'] + \
            self._wah.__dict__['phi']
        
        b1 = -2.0 * self._wah.__dict__['zm'] * cos(self._wah.__dict__['zp'] + d)
        b2 = self._wah.__dict__['zm'] * self._wah.__dict__['zm']
        a1 = -2.0 * self._wah.__dict__['pm'] * cos(self._wah.__dict__['pp'] + d)
        a2 = self._wah.__dict__['pm'] * self._wah.__dict__['pm']
        norm = 0.8
        
        return norm * \
            ( self._pX[self._Ix] + \
              b1 * self._pX[(self._Ix + BUF_LEN - 1) % BUF_MASK] + \
              b2 * self._pX[(self._Ix + BUF_LEN - 2) % BUF_MASK] - \
              a1 * self._pX[(self._Iy + BUF_LEN - 1) % BUF_MASK] - \
              a2 * self._pX[(self._Iy + BUF_LEN - 2) % BUF_MASK] )
