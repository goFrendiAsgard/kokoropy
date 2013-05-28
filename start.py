#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# CONFIGURATION (Feel free to modify it)
###########################################################################
HOST                = 'localhost'
PORT                = 8080
DEBUG               = True
RELOADER            = False
SERVER              = 'kokoro' # or wsgiref or whatever
APP_DIRECTORY       = 'applications'

###########################################################################
# RUN THE SERVER
###########################################################################
def main_process():
    import os
    from kokoropy import kokoro_init
    PWD = os.path.dirname(os.path.abspath(__file__))
    APPLICATION_PATH    = os.path.join(PWD, APP_DIRECTORY)
    kokoro_init(application_path = APPLICATION_PATH, debug=DEBUG,
                port=PORT, reloader=RELOADER, host=HOST, server=SERVER)

import threading, time
threadLock = threading.Lock()

class Counter (threading.Thread):
    def __init__(self, threadID, name, max_count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.max_count = max_count
        self.counter = max_count
        
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        threadLock.acquire()
        # do the action        
        while self.counter>0:
            print self.counter
            self.counter -= 1
            time.sleep(1)
            if self.counter == 0:
                self.counter = self.max_count
        # Free lock to release next thread
        threadLock.release()

class Runner (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        threadLock.acquire()
        # do the action        
        main_process()
        # Free lock to release next thread
        threadLock.release()

if __name__ == '__main__':
    main_process()
    '''
    try:
        counter = Counter(1,'Counter A',10)
        runner = Runner(2,'Runner A')
        counter.daemon=True
        runner.daemon=True
        counter.start()
        runner.start()
        
        threads = []
        # Add threads to thread list
        threads.append(counter)
        threads.append(runner)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        print "Exiting Main Thread"
        while True:
            time.sleep(100)
    except(KeyboardInterrupt, SystemExit):
        pass
    '''
    