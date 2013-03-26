#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "portaudio.h"
#include "soundProcessor.h"
#include "portAudioPipe.h"

#define DITHER_FLAG     (0) /**/

/*******************************************************************/
int main(void);
int main(void)
{
    // Instantiate a pipe between the 
    portAudioPipe m_Pipe;
    m_Pipe.Initial();
    m_Pipe.Start();
}

