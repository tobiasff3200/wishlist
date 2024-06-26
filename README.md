# Wunschliste

## Features

- Eine Wunschliste für Jeden
- Es können versteckte Wünsche zu den Listen der anderen hinzufügen werden.
- Wünsche können reserviert werden
- Passwortschutz

## Installation

### Docker Compose

Die Datei [docker-compose.yml](https://gitlab.fachschaften.org/tobiasff3200/wishlist/-/blob/main/docker-compose.yml)
herunterladen und mit `docker compose up -d` starten.

## Konfiguration

### Adminkonto erstellen

Als Erstes muss ein Benutzerkonto angelegt werden. Mit dem Befehl `docker exec -it wishlist bash` wechseln wir in den
eben gestarteten Container.

Mit `source venv/bin/activate` und `python /app/manage.py createsuperuser` wird das erste Konto erstellt.

Mit `exit` wird der Container wieder verlassen.

### Weitere Benutzer\*innen hinzufügen

Weitere Benutzer\*innen können auf der Administrationsseite angelegt werden. Diese ist erreichbar
unter `https://<ip oder domain>/admin`. Die Passwörter können später geändert werden.

## Benutzung

### Sichtbarkeit von Wünschen

Wünsche, die von einem selbst erstellt wurden, können bearbeitet oder gelöscht werden, egal auf welcher Wunschliste.

Man kann die Wünsche der anderen reservieren, damit ein Geschenk nicht mehrfach besorgt wird. Dabei wird die
Reservierung allen angezeigt, außer der Person, die den Wunsch geäußert hat. Man kann bei seinen eigenen Wünschen nicht
sehen, ob sie reserviert wurden.

Fügt man einen Wunsch zu der Liste einer anderen Person hinzu, so ist er für alle sichtbar, außer für die Person, die
das Geschenk bekommen soll. Dadurch kann man selbst den Überblick behalten und vergisst Geschenkideen nicht.

### Gruppen

Auf der Administrationsseite können Benutzer\*innen in Gruppen organisiert werden. Dazu können beliebig viele `Groups`
unter der Überschrift `app` angelegt werden. **Wichtig:** Wenn eine Gruppe angelegt ist, können alle Benutzer\*innen nur
noch die Listen von denen sehen, die in mindestens einer Gruppe zusammen sind. Benutzer\*innen, die in keiner Gruppe
sind, sehen dann nur noch ihre eigene Wunschliste.

## Fehler oder Anregungen

Bitte meldet gefundene Fehler per [Email](mailto:tobiasff3200-wishlist-1161-issue-@gitlab.fachschaften.org) oder
als [Issue](https://gitlab.fachschaften.org/tobiasff3200/wishlist/-/issues).

Gerne können auch Änderungswünsche oder neue Funktionen vorgeschlagen werden.

## Credits

[Wishlist icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/wishlist)
