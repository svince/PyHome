import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import mainwindow_auto
import urllib.request
import json
import time

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    running_since = "Just started.."

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.updateBusTimes()
        self.running_since = str(time.ctime())
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateBusTimes)
        self.timer.start(5000)

    def updateBusTimes(self):
        times = getStationTimes("thuijastrasse", 5)
        text = ""
        for t in times:
            text += t[0] + " " + t[1] + " " + t[2] + "\n"
        text += "\nUpdated at: " + str(time.ctime())
        text += "\nRunning since: " + self.running_since
        self.label.setText(text)

def getStationTimes(station_name, limit):
    request = "http://transport.opendata.ch/v1/stationboard?station="
    request += station_name + "&limit=" + str(limit)
    response_bytes = urllib.request.urlopen(request).read()
    response_json = response_bytes.decode("utf-8")
    response = json.loads(response_json)
    board = response["stationboard"]
    times = []
    for entry in board:
        name = entry["name"]
        to = entry["to"]
        stop = entry["stop"]
        departure = stop["departure"]
        departure_time_pre = departure.split("T")[1]
        departure_time = departure_time_pre.split("+")[0]
        times.append([name, to, departure_time])
    return times      

def test_sbb_access():
    times = getStationTimes("thujastrasse", 5)
    for time in times:
        print(time[0] + " " + time[1] + " " + time[2])

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
        
