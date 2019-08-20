#!/usr/bin/python3

import getpass
import os
import platform
import shlex
import shutil
import subprocess
import sys

import toml

SKRIPTPFAD = os.path.abspath(os.path.dirname(__file__))
SPEICHERORT_ZUGANGSDATEN = "/etc/smbcredentials"
PFAD_PING_SERVER_SERVICE = "/etc/systemd/system/ping_server.service"
PFAD_PING_SERVER = "/usr/local/sbin/ping_server.py"
PFAD_SYSTEMD_SERVICE_UNIT = "/etc/systemd/system"


def pfadeingabe():
    ordner = input("Name für neuen Mountordner: ")
    pfad = input("Wenn leer: -> /media ")
    if pfad == "":
        pfad = "/media"
    return os.path.join(pfad, ordner)


def zugangsdaten_eingeben():
    print("Zugangsdaten für das einzuhängende Gerät - Zugang muss am anderen Gerät freigeben/erstellt werden.")
    username = input("Benutzername: ")
    pw = getpass.getpass("Passwort: ")
    return {"username": username, "pw": pw}


def adresse_eingeben():
    return input("Externe Adresse eingeben: ")


def optionen_eingeben():
    uid = "uid={}".format(input("uid: Bsp. 1000 "))
    gid = "gid={}".format(input("gid: Bsp. 1000 "))
    eingabe_liste = [uid, gid]
    eingabe = True
    while eingabe:
        eingabe = input("Weitere Optionen eingeben - Bsp: vers=1.0, weiter mit leerer Eingabe: ")
        if eingabe:
            eingabe_liste.append(eingabe)
    optionen = ",".join(eingabe_liste)
    return optionen


def zugangsdaten_erstellen(zugangsdaten):
    with open(SPEICHERORT_ZUGANGSDATEN, "w") as file:
        file.write("username={username}\npassword={pw}".format(username=zugangsdaten["username"],
                                                               pw=zugangsdaten["pw"]))
    shutil.chown(SPEICHERORT_ZUGANGSDATEN, "root", "root")
    os.chmod(SPEICHERORT_ZUGANGSDATEN, 600)
    print("Zugangsdaten erstellt - Pfad: {}".format(SPEICHERORT_ZUGANGSDATEN))


def ordner_erstellen(pfad):
    if os.path.exists(pfad):
        print("Pfad existiert schon!")
    else:
        os.mkdir(pfad)
        if os.path.exists(pfad):
            print("Ordner {} erstellt".format(pfad))
        else:
            raise BaseException("Ordner konnte nicht erstellt werden")


def inhalt_systemd_service_mount_unit_generieren(mount_pfad, adresse, optionen, type_="cifs"):
    mount_unit = """[Unit]
Description=Mount von {mount_pfad}
Requires=ping_server.service
After=ping_server.service
Conflicts=shutdown.target
ConditionPathExists={mount_pfad}
[Mount]
What={adresse}
Where={mount_pfad}
Options=credentials={zugangsdaten},{optionen}
Type={type}
[Install]
WantedBy=multi-user.target
""".format(mount_pfad=mount_pfad, adresse=adresse, zugangsdaten=SPEICHERORT_ZUGANGSDATEN, optionen=optionen, type=type_)
    return mount_unit


def name_mount_unit_ermitteln(mount_pfad):
    cmd = shlex.split("systemd-escape --suffix=mount --path {}".format(mount_pfad))
    instanz = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    filename = instanz.stdout.read().decode("utf-8").strip()
    return filename


def mount_unit_erstellen(inhalt, mount_pfad):
    filename = name_mount_unit_ermitteln(mount_pfad)
    pfad = os.path.join(PFAD_SYSTEMD_SERVICE_UNIT, filename)

    with open(pfad, "w") as file:
        file.write(inhalt)
    shutil.chown(pfad, "root", "root")
    os.chmod(pfad, 644)
    print("Datei {} erstellt".format(pfad))
    return filename


def ping_server_kopieren():
    src = os.path.join(SKRIPTPFAD, "ping_server.py")
    shutil.copy(src, PFAD_PING_SERVER)
    shutil.chown(PFAD_PING_SERVER, "root", "root")
    os.chmod(PFAD_PING_SERVER, 755)
    print("Datei {} erstellt".format(PFAD_PING_SERVER))


def ip_pingziel_eingeben():
    ip_pingziel = input("IP Pingziel zur Überprüfung der Netwerkverfügbarkeit eingeben: ")
    return ip_pingziel


def ping_server_service_erstellen(ip_pingziel):
    inhalt = """[Unit]
Description=serverctl.service:   Waiting for Network or Server to be up
After=network.target
[Service]
Type=oneshot
TimeoutStartSec=95
ExecStart=/usr/local/sbin/ping_server.py {}
[Install]
WantedBy=multi-user.target""".format(ip_pingziel)

    with open(PFAD_PING_SERVER_SERVICE, "w") as file:
        file.write(inhalt)
    shutil.chown(PFAD_PING_SERVER_SERVICE, "root", "root")
    os.chmod(PFAD_PING_SERVER_SERVICE, 644)
    print("Datei {} erstellt".format(PFAD_PING_SERVER_SERVICE))


def mount_unit_aktivieren(mount_unit):
    cmd = shlex.split("systemctl start {}".format(mount_unit))
    start = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print(start.stdout.read())

    befehl = input("Unit aktivieren? (j|n)")
    if befehl == "j":
        cmd = shlex.split("systemctl enable {}".format(mount_unit))
        start = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        print(start.stdout.read())
    else:
        print("Hinweis, wird eine Service Unit verändert muss anschließend 'systemctl daemon-reload' ausgeführt werden")


def eingabe_sichern(pfad_mountpunkt, zugangsdaten, adresse, optionen, ip_pingziel):
    ausgabe = {"pfad_mountpunkt": pfad_mountpunkt,
               "zugangsdaten": zugangsdaten,
               "adresse": adresse,
               "optionen": optionen,
               "ip_pingziel": ip_pingziel}
    ausgabe_toml = toml.dumps(ausgabe)
    name = input("Configname eingeben: ")
    filename = "{}_cfg.toml".format(name)
    pfad = os.path.join(SKRIPTPFAD, filename)
    with open(pfad, "w") as file:
        file.write(ausgabe_toml)
    shutil.chown(pfad, "root", "root")
    os.chmod(pfad, 600)
    print("Datei {} erstellt".format(pfad))


def lade_daten(cfg):
    if "cfg.toml" in cfg:
        datei = os.path.join(SKRIPTPFAD, cfg)
        with open(datei) as file:
            config = toml.loads(file.read())
        return config
    else:
        raise ValueError("Dateiformat falsch")


def willkommen():
    text = """Dieses Skript soll die Einrichtung zum Einhängen von Netzwerkfreigaben beschleunigen.
    Es kann nicht das notwendige Wissen zu den einzelnen Punkten während der Erstellung ersetzen.
    Verwendung und Benutzung auf eigene Gefahr!"""
    print(text)


def main():
    willkommen()
    if platform.system() == "Linux":
        if len(sys.argv) > 1:
            daten = lade_daten(sys.argv[1])
            pfad_mountpunkt = daten["pfad_mountpunkt"]
            zugangsdaten = daten["zugangsdaten"]
            adresse = daten["adresse"]
            optionen = daten["optionen"]
            ip_pingziel = daten["ip_pingziel"]
        else:
            pfad_mountpunkt = pfadeingabe()
            zugangsdaten = zugangsdaten_eingeben()
            adresse = adresse_eingeben()
            optionen = optionen_eingeben()
            ip_pingziel = ip_pingziel_eingeben()
            print("Die Konfigruationsdatei enthält wenn sie gespeichert wird alle Eingaben einschließlich Passwörter "
                  "in Klartext!")
            eingabe = input("Eingaben sichern? (j|n)")
            if eingabe == "j":
                eingabe_sichern(pfad_mountpunkt, zugangsdaten, adresse, optionen, ip_pingziel)

        ordner_erstellen(pfad_mountpunkt)
        zugangsdaten_erstellen(zugangsdaten)
        mount_unit = mount_unit_erstellen(inhalt_systemd_service_mount_unit_generieren(pfad_mountpunkt, adresse,
                                                                                       optionen),
                                          pfad_mountpunkt)
        ping_server_kopieren()
        ping_server_service_erstellen(ip_pingziel)
        mount_unit_aktivieren(mount_unit)

    else:
        print("Falsches Betriebssystem")


if __name__ == "__main__":
    main()
