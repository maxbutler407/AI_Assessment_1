# Written by: Max Butler

import time
import tracemalloc

class Testing():
    
    def __init__(self):
        
        self.startTime = 0
        
    # start a timer (milliseconds) for testing purposes
    def startMSTimer(self):
        
        # start timer
        self.startTime = time.time()
    
    # end the timer and print out the elapsed time
    def endMSTimer(self):
        
        # Get time after execution
        endTime = time.time()
        
        # Convert seconds to milliseconds and print elapsed time
        elapsedTime = (endTime - self.startTime) * 1000
        print(f"Elapsed time: {elapsedTime:.3f} ms")
        
    # starts memory tracker in MB
    def startMemoryTracker(self):
        tracemalloc.start()
    
    # ends memory tracker and prints out memory usage
    def endMemoryTracker(self):
        
        # gets memory usage in bytes
        current, peak = tracemalloc.get_traced_memory()
        
        # stops the tracing
        tracemalloc.stop()

        # prints out the current and peak memory usage
        print(f"Current memory usage: {current / 1024 / 1024:.3f} MB")
        print(f"Peak memory usage: {peak / 1024 / 1024:.3f} MB")