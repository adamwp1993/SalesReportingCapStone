import datetime


class Logger():


    @staticmethod
    def write_log(text):
        log_file = open("logs", 'a')
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(dt_string + " " + text + "\n")
        log_file.close()


