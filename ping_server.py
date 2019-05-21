#!/usr/bin/python3

import shlex
import subprocess
import sys
import time

VERSUCHE = 5


def ping_wlan(ip):
    """pingt die IP 2x an
    return (0 | !0) 0 wenn erreichbar"""
    befehl = "ping -c2 -W1 {}".format(ip)
    cmd = shlex.split(befehl)
    return subprocess.call(cmd)


def systemd_cat(message, identifier, priority):
    befehl = "/usr/bin/systemd-cat -t {identifier} -p {priority}".format(identifier=identifier, priority=priority)
    cmd = shlex.split(befehl)
    subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(message.encode())


def starte_ping_versuch(ip):
    for versuch in range(1, VERSUCHE+1):
        status = ping_wlan(ip)
        if status == 0:
            systemd_cat("[{}|{}] Ping an {} erfolgreich".format(versuch, VERSUCHE, ip), sys.argv[0], "info")
            sys.exit(0)
        else:
            systemd_cat("[{}|{}] Host {} nicht erreichbar".format(versuch, VERSUCHE, ip), sys.argv[0], "warning")
        time.sleep(5)
    systemd_cat("Zu viele Fehlversuche - Host {} nicht erreichbar".format(ip), sys.argv[0], "err")
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        starte_ping_versuch(sys.argv[1])
    else:
        systemd_cat("Keine IP angegeben", sys.argv[0], "err")


if __name__ == "__main__":
    main()
