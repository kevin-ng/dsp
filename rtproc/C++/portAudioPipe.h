// Created by Paolo Prandoni and Martin Vetterli of the Ecole Polytechnique
// Federale de Lausanne

#ifndef PORTAUDIOPIPE_H
#define PORTAUDIOPIPE_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#ifdef WIN32
#include <conio.h>
#include "PortAudio.h"
#define PRINTOPTION printf
#ifndef initscr
#define initscr
#endif
#ifndef endwin
#define endwin
#endif
#else
#include <ncurses.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#ifndef __int16
#define __int16 int16_t
#define _getch getch
#define PRINTOPTION printw
#endif
#endif
#include "portaudio.h"
#include "soundProcessor.h"
#define SAMPLE_RATE  (44100)
#define FRAMES_PER_BUFFER (4)
#define NUM_CHANNELS    (1)
#define NUM_SECONDS     (15)
/* @todo Underflow and overflow is disabled until we fix priming of blocking write. */
#define CHECK_OVERFLOW  (0)
#define CHECK_UNDERFLOW  (0)

/* Select sample format. */
#if 0
#define PA_SAMPLE_TYPE  paFloat32
#define SAMPLE_SIZE (4)
#define SAMPLE_SILENCE  (0.0f)
#define CLEAR(a) memset( (a), 0, FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE )
#define PRINTF_S_FORMAT "%.8f"
#elif 1
#define PA_SAMPLE_TYPE  paInt16
#define SAMPLE_SIZE (2)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset( (a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE )
#define PRINTF_S_FORMAT "%d"
#elif 0
#define PA_SAMPLE_TYPE  paInt24
#define SAMPLE_SIZE (3)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset( (a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE )
#define PRINTF_S_FORMAT "%d"
#elif 0
#define PA_SAMPLE_TYPE  paInt8
#define SAMPLE_SIZE (1)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset( (a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE )
#define PRINTF_S_FORMAT "%d"
#else
#define PA_SAMPLE_TYPE  paUInt8
#define SAMPLE_SIZE (1)
#define SAMPLE_SILENCE  (128)
#define CLEAR( a ) { \
    int i; \
    for( i = 0; i < FRAMES_PER_BUFFER*NUM_CHANNELS; i++ ) \
        ((unsigned char *)a)[i] = (SAMPLE_SILENCE); \
}
#define PRINTF_S_FORMAT "%d"
#endif
class portAudioPipe
{
public:
    portAudioPipe();
    virtual ~portAudioPipe();
    void Initial();
    void Start();
    void Stop();
    void printOptions(int option);
    void error();
    void xrun();
public:
    soundProcessor m_soundProcessor;
    int option;

private:
    PaStreamParameters inputParameters, outputParameters;
    PaStream *stream;
    PaError err;
    char *sampleBlock, *samplePointer;
    char *currentBlock;
};

#endif // PORTAUDIOPIPE_H

