# create_automount
Hilfsskript zum erstellen aller notwendigen Skripte nach der Tutorialanleitung im Raspberry Pi Forum.

Das vollständige Tutorial zum einbinden von Netzwerkfreigaben mit Hilfe einer Systemd Mount Unit findet sich im 
Deutschen Raspberry Pi Forum und folgendem Link:
     
     https://forum-raspberrypi.de/forum/thread/40061-netzwerkfreigabe-mounten-mit-systemd-mount-unit/

## Vorbereitungen
Zur erfolgreichen Ausführungen des Skriptes wird mindestens _Python 3.5_ oder höher benötigt.

### Module installieren
Das Skript benötigt folgende Module 
* toml

Zum installieren der Module folgenden Befehl ausführen:

    pip3 install -r requirements.txt
    
## Verwendung
Das Skript benötigt zur erfolgreichen Ausführung root-Rechte.
Achtung! Generell gilt: Blindes Ausführen von Skripten mit root Rechten kann das System schädigen oder kompremetieren.
Die Verwendung des Skriptes erfolgt auf eigene Gefahr.

### Ausführung
Es gibt 2 Möglichkeiten das Skript zu starten.
Variante 1 bietet eine geführte Eingabeaufforderung aller nötigen Daten. Anschließend wird man gefragt ob man die
eingegebenen Daten in einer Datei speichern möchte. Dies hat den Vorteil, dass man bei einer erneuten Einrichtung des 
Pi's oder auf anderen Pi's die Daten nicht mehr selbst eingeben muss, sondern dass sich das Skript die Daten aus der 
Datei einließt. Dies spart Zeit und Fehler. Das ist Variante 2.

Variante 1:  

    python3 create_auto_mount.py
    
Variante 2:

    python3 create_auto_mount.py <dateiname_cfg.toml>

### Kompatiblität:
Die Funktionalität des Skriptes wurde mit folgendem Betriebsystem getestet:
* Raspbian Stretch 4.14.79-v7+

## Weiteres
Das Skript soll die Einrichtung beschleunigen und vereinfachen. Es kann jedoch nicht das nötige Wissen ersetzen, welches
man sich im Umgang mit Linux bezüglich Rechteverwaltung, Systemd, Service Untis und Benutzerverwaltung
aneignen sollte.
