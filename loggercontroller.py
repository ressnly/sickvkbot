from threading import Thread
import time


class LogController(Thread):
    def __init__(self, _logger):
        Thread.__init__(self)
        self.logger = _logger
        self.running = True

    def run(self):
        while self.logger.write_logs() and self.running:
            time.sleep(60)
        self.logger.close_files()
        print("Logger thread is closed")

    def close_thread(self):
        self.running = False
