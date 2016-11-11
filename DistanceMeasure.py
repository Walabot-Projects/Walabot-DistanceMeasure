from __future__ import print_function
from sys import platform
from os import system
import WalabotAPI


class Walabot:

    def __init__(self):
        self.wlbt = WalabotAPI
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()
        self.isConnected = False
        self.isTargets = False

    def connect(self):
        try:
            self.wlbt.ConnectAny()
            self.isConnected = True
            self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_MTI)
            self.wlbt.SetArenaTheta(-0.1, 0.1, 10)
            self.wlbt.SetArenaPhi(-0.1, 0.1, 10)
            self.wlbt.SetArenaR(100, 1000, 5)
            self.wlbt.SetThreshold(100)
        except self.wlbt.WalabotError as err:
            if err.code != 19:  # 'WALABOT_INSTRUMENT_NOT_FOUND'
                raise err

    def start(self):
        self.wlbt.Start()

    def get_targets(self):
        self.wlbt.Trigger()
        return self.wlbt.GetSensorTargets()

    def stop(self):
        self.wlbt.Stop()

    def disconnect(self):
        self.wlbt.Disconnect()


def print_targets(targets):
    system("cls" if platform == "win32" else "clear")  # clear the screen
    if not targets:
        print("No targets")
        return
    d_min = min(targets, key=lambda t: t[2])[2]  # closest target
    d_amp = max(targets, key=lambda t: t[3])[2]  # "strongest" target
    if d_min == d_amp:
        print("THE DISTANCE IS {:3.0f}\n".format(d_min))
    else:
        print("CALCULATING...\n")


def main():
    wlbt = Walabot()
    wlbt.connect()
    if not wlbt.isConnected:
        print("Not Connected")
    else:
        print("Connected")
    wlbt.start()
    while True:
        print_targets(wlbt.get_targets())


if __name__ == '__main__':
    main()
