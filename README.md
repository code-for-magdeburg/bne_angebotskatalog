# BNE Angebotskatalog Magdeburg

Eine interaktive Variante des Angebotskataloges 'Bildung für nachhaltige Entwicklung' der Stadt Magdeburg

## Über das Projekt

Dieses Projekt bietet eine interaktive Webanwendung für den Angebotskatalog 'Bildung für nachhaltige Entwicklung' der Stadt Magdeburg. Es ermöglicht Benutzern, Bildungsangebote durchsuchen, filtern und anzeigen zu können.

## Technologie-Stack

- **Backend**: Python FastAPI
- **Datenbank**: MariaDB
- **Frontend**: HTML/CSS/JavaScript (im `public` Ordner)
- **Containerisierung**: Docker & Docker Compose

## Projektstruktur

```
├── backend/          # FastAPI Anwendung
│   ├── app/          # API Endpunkte und Logik
│   ├── public/       # Statische Frontend-Dateien
│   ├── Dockerfile    # Backend Container Konfiguration
│   └── requirements.txt # Python Abhängigkeiten
├── database/         # Datenbankschema und Initialisierung
├── docker-compose.yml # Komplett-Umgebungskonfiguration
└── README.md         # Diese Datei
```

## Voraussetzungen

- Docker und Docker Compose
- Git

## Installation und Setup

1. Repository klonen:
   ```bash
   git clone <repository-url>
   cd bne_angebotskatalog_magdeburg
   ```

2. Umgebung mit Docker Compose starten:
   ```bash
   docker-compose up -d
   ```

3. Auf die Anwendung zugreifen:
   - API: http://localhost:8000
   - Frontend: http://localhost:8000/public

## Entwicklung

### Backend Entwicklung

Das Backend läuft auf Port 8000 mit automatischem Reload bei Änderungen.

API Dokumentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Datenbank

Die MariaDB-Datenbank ist auf Port 3306 verfügbar mit den folgenden Zugangsdaten:
- Host: localhost:3306
- Datenbank: app_db
- Benutzer: app_user
- Passwort: example_user_password

## Nützliche Endpunkte

- `/api/institutions` - Institutionen abrufen
- `/api/offers` - Bildungsangebote abrufen
- `/health` - Systemstatus prüfen

## Projektwartung

Um die Container zu stoppen:
```bash
docker-compose down
```

Um die Container neu zu bauen und zu starten:
```bash
docker-compose up --build
```
