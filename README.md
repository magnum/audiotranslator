# AudioTranslator

## Per testare:
      avviare il server backend via terminale --> "python [percorso]/backTrans.py"
      avviare il frontend via terminale --> "python [percorso]/run_frontend_server.py"

## Prerequisiti:
### Configurazione dell'Ambiente
#### Impostare la Variabile d'Ambiente:
Ogni utente che esegue l'applicazione dovrà configurare la variabile di ambiente GOOGLE_APPLICATION_CREDENTIALS sul proprio computer. Questa variabile deve puntare al file JSON che contiene le credenziali per l'account di servizio di Google Cloud. Queste credenziali devono avere i permessi per accedere alle API di Speech-to-Text, Translate e Text-to-Speech.

#### Abilitare le API di Google Cloud:
Ogni utente deve avere un progetto su Google Cloud Console con le API di Speech-to-Text, Translate e Text-to-Speech abilitate. Questo può essere fatto andando nella sezione "Libreria API" della Google Cloud Console e abilitando ciascuna di queste API per il proprio progetto.

### Dipendenze
#### Installare le Dipendenze:
L'utente deve installare tutte le dipendenze richieste dal progetto, incluse le librerie Python necessarie (Flask, pydub, google-cloud-speech, google-cloud-translate, google-cloud-texttospeech, flask-cors) e FFmpeg.  
Per installere dipendenze eseguire
```
pip install -r requirements.txt
```
