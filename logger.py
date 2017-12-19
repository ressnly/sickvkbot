import os.path
import time


class DataLogger:
    def __init__(self, logs_directory):
        self.logs_directory = logs_directory
        self.files = list()
        self.work = True

    def log_message(self, adds, msg, event_name):
        print("event[%s] address[%s] message[%s]" % (event_name, adds, msg))
        logfile = None
        for item in self.files:
            if item.get('id') == adds:
                logfile = item
                break
        if logfile is None:
            try:
                filename = os.path.dirname(os.path.realpath(__file__))+"/resources/" + \
                           self.logs_directory+"/"+str(adds)+".txt"
                if os.path.exists(filename):
                    file = open(filename, 'a+')
                else:
                    file = open(filename, 'w')
                logfile = dict(id=adds, file=file, path=filename)
                self.files.append(logfile)
            except IOError as e:
                print("Some troubles with open log file: ", e)
                return
        logfile['file'].write("event[%s] address[%s] message[%s] time[%s]\n" % (event_name, adds, msg, time.asctime()))

    def write_logs(self):
        for item in self.files:
            (item['file']).close()
            try:
                item['file'] = open(item['path'], 'a+')
            except IOError as e:
                print("Cant refresh log file: ", e)
        return self.work

    def close_files(self):
        self.work = False
        for item in self.files:
            file = item.get('file')
            if file is not None:
                file.close()

