# build helloworld executable when user executes "make"

volumecontrol: volumecontrol.o
	$(CC) $(LDFLAGS) -lasound volumecontrol.o -o volumecontrol
volumecontrol.o: volumecontrol.c
	$(CC) $(CFLAGS) -c volumecontrol.c

# remove object files and executable when user executes "make clean"
clean:
	rm *.o volumecontrol
	