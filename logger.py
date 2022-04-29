import datetime
timedate = datetime.datetime.now()

def makeLog(msg):
    time = ("%s" % timedate)
    output = (f"{time}> {msg} \n")

    log_file = open("log.txt", "a")
    log_file.write(output)
    log_file.close

    print(output)

def makeTelegramLog(msg, user):
    time = ("%s" % timedate)
    output = (f"{time} - {user} - {msg} \n")

    log_file = open("log.txt", "a")
    log_file.write(output)
    log_file.close

    print(output)