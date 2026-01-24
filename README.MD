### COMANDI DA USARE PER AVVIARE I CONTAINER ###
    
    -docker compose build
    -docker compose up OPPURE docker compose up -d (per avviare i container in background)\

### COMANDO DA USARE PER CONTROLLARE STATO DEI CONTAINER ###

    -docker ps

### COMANDO DA USARE PER INTERROMPERE I CONTAINER ###

    -docker compose down

### COMANDO PER POPOLARE IL DATABASE ###

    -python import_data.py (potrebbe essere necessario sostituire in db.py 
        -->
            from backend.db.db_interface import DatabaseInterface
            IN
            from db_interface import DatabaseInterface)

### ACCEDERE ALLA PAGINA ###

    Ora è possibile accedere alla pagina web da 'localhost:8888'
