CONFIGURATION = Release
CXX = g++
ifeq ($(CONFIGURATION), Debug)
	CXXFLAGS = -g -O2 -Wall
else
	CXXFLAGS = -O2 -Wall
endif
INCLUDES = -I.  -I/usr/local/include
OBJS = $(CONFIGURATION)/rtproc.o $(CONFIGURATION)/soundProcessor.o $(CONFIGURATION)/portAudioPipe.o
LDFLAGS = -lportaudio -lstdc++ -lncurses
APP = $(CONFIGURATION)/rtproc
.PHONY: all clean 

all:	$(CONFIGURATION) $(OBJS)
	$(CXX) -o $(APP) $(OBJS) $(LDFLAGS)

$(CONFIGURATION)/%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $(INCLUDES) -o $@ $<

$(CONFIGURATION):
	mkdir -p $(CONFIGURATION)
clean:
	@echo "Cleaning up.."
	-rm -f $(OBJS)
	-rm -f $(APP)
