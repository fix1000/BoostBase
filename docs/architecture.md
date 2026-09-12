# BoostBase Architecture

BoostBase/
│
├── data/   #till firther notice: store .json data
├── docs/   #manuals
├── models/  #songs / setlist models
├── services/   #Init, song mgt, stelist mgt. <-- do the business logic work
├── tests/  #autotest
│
├── main.py  #start up!
├── requirements.txt
└── ...

## Overview

BoostBase is a Python application for managing the repertoire of a band.
The application is designed to separate data storage, business logic and application startup.

## Project Structure

### main.py

The application entry point.
Responsible for starting BoostBase and coordinating the application startup.

### models/

Contains the data models used by BoostBase.
Examples:
- Song
- Setlist

### services/

Contains the business logic of the application.
Examples:
- Application initialization
- Song management
- Setlist management

### data/

Contains persistent application data.
For the initial version, song data will be stored in JSON files.
The application is responsible for creating required data files if they do not exist.

### tests/

Contains automated tests for BoostBase.

### docs/

Contains project documentation, including requirements, architecture and roadmap.

## Initial Data Flow

The initial application flow is:
User
→ main.py
→ services
→ data
The models define the structure of the data used by the application.

## Future Architecture

The architecture may evolve as BoostBase grows.
Possible future components include:
- SQLite or another database
- REST API
- Web interface
- Spotify integration
- AI services
- Azure cloud services
