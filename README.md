# Organizzatore MP3

Script Python per organizzare automaticamente file MP3 in sottocartelle basate sui tag ID3.

## Funzionalità

- ✅ Organizza file MP3 in sottocartelle per compilation/album
- ✅ Limite di 600MB (configurabile) per cartella
- ✅ Aggiunge numerazione sequenziale ai file (001_, 002_, ecc.)
- ✅ Legge il nome della compilation dal tag ID3 (TALB - Album)
- ✅ Gestisce automaticamente cartelle multiple per compilation grandi
- ✅ **Interfaccia grafica intuitiva**
- ✅ **Selezione cartelle origine e destinazione**
- ✅ **Log in tempo reale**

## Utilizzo Rapido (Windows)

### Metodo 1: Doppio Click (Consigliato)
1. Fai doppio click su `avvia_organizzatore.bat`
2. L'interfaccia grafica si aprirà automaticamente
3. Seleziona le cartelle e avvia l'organizzazione

### Metodo 2: Eseguibile Standalone
1. Fai doppio click su `crea_eseguibile.bat`
2. Attendi la creazione dell'eseguibile
3. Troverai `MP3_Organizer.exe` nella cartella `dist`
4. Copia l'eseguibile ovunque e usalo senza Python!

## Installazione Manuale

1. Installa Python 3.7 o superiore
2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Utilizzo da Linea di Comando

### Versione con GUI:
```bash
python organizza_mp3_gui.py
```

### Versione Console:
```bash
python organizza_mp3.py
```

## Esempio

**Prima:**
```
/Music/
  ├── song1.mp3
  ├── song2.mp3
  ├── song3.mp3
  └── song4.mp3
```

**Dopo:**
```
/Music/
  ├── Best Hits 2024/
  │   ├── 001_song1.mp3
  │   └── 002_song2.mp3
  └── Rock Classics/
      ├── 001_song3.mp3
      └── 002_song4.mp3
```

## Note

- Lo script legge il tag TALB (Album) dai metadati ID3
- Se il tag non è presente, usa "Sconosciuto" come nome cartella
- I caratteri speciali nei nomi vengono sostituiti con underscore
- Se una compilation supera il limite, viene divisa in Part1, Part2, ecc.

## Requisiti

- Python 3.7+
- mutagen (per leggere i tag ID3)
"# organizza-mp3" 
