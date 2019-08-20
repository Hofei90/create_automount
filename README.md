# create_automount
Hilfsskript zum Erstellen aller notwendigen Skripte nach der Anleitung im Deutschen Raspberry Pi Forum

Das vollständige Tutorial zum Einbinden von Netzwerkfreigaben mit Hilfe einer Systemd Mount Unit findet sich im 
Deutschen Raspberry Pi Forum unter folgendem Link:
     
     https://forum-raspberrypi.de/forum/thread/40061-netzwerkfreigabe-mounten-mit-systemd-mount-unit/

## Vorbereitungen
Zur erfolgreichen Ausführung des Skriptes wird mindestens _Python 3.5_ oder höher benötigt.

### Module installieren
Das Skript benötigt folgendes Modul:
* toml

Zum Installieren des Moduls folgenden Befehl ausführen:

    pip3 install -r requirements.txt
    
## Verwendung
Das Skript benötigt zur erfolgreichen Ausführung root Rechte.
Achtung! Generell gilt: Blindes Ausführen von Skripten mit root Rechten kann das System schädigen oder kompromittieren.
Die Verwendung des Skriptes erfolgt auf eigene Gefahr.

### Ausführung
Es gibt zwei Möglichkeiten, das Skript zu starten.
Variante 1 bietet eine geführte Eingabeaufforderung zum Eintrag der notwendigen Daten. Anschließend besteht die Möglichkeit, diese Daten in einer Datei zu speichern. 
Variante 2: Bei einer erneuten Einrichtung des selben bzw. weiteren Raspberry Pi können die Daten aus der unter Variante 1 erstellten Datei eingelesen werden. Dies spart Zeit und ist weniger fehleranfällig. 

Variante 1:  

    python3 create_auto_mount.py
    
Variante 2:

    python3 create_auto_mount.py <dateiname_cfg.toml>

### Kompatibilität:
Die Funktionalität des Skriptes wurde mit folgenden Betriebsystemen getestet:
* Raspbian Stretch 4.14.79-v7+
* Raspbian Buster 4.19.58-v7l+

## Weiteres
Das Skript soll die Einrichtung beschleunigen und vereinfachen. Es kann jedoch nicht das nötige Wissen im Umgang mit Linux bezüglich Rechteverwaltung, Systemd, Service Units und Benutzerverwaltung etc. ersetzen.
