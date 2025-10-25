# 🎵 MP3 Organizer

Organizzatore automatico di file MP3 con interfaccia grafica. Organizza la tua collezione musicale in cartelle ordinate con numerazione sequenziale.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Funzionalità

- 🎯 **Interfaccia grafica intuitiva** - Facile da usare, nessuna riga di comando
- 📁 **Due modalità di organizzazione**:
  - Raggruppa per Album/Compilation (usa tag ID3)
  - Crea cartelle da max 600MB (ignora tag)
- 🔢 **Numerazione automatica** - Aggiunge prefisso 001_, 002_, ecc.
- ⚙️ **Dimensione configurabile** - Imposta il limite MB per cartella
- 📊 **Log in tempo reale** - Vedi cosa sta succedendo
- 🎨 **Gestione tag ID3** - Legge album/compilation dai metadati
- 💾 **Copia o sposta** - Preserva i file originali se usi cartelle diverse

## 📸 Screenshot

```
┌─────────────────────────────────────────┐
│      🎵 Organizzatore MP3               │
├─────────────────────────────────────────┤
│ Cartella Origine:  [Browse...]          │
│ Cartella Dest:     [Browse...]          │
│ Max Size: 600 MB                        │
│ ☐ Raggruppa per Album (tag ID3)        │
│                                         │
│ [▶ Avvia] [🗑 Pulisci] [❌ Esci]       │
│                                         │
│ Log:                                    │
│ ✓ Trovati 150 file MP3                 │
│ 📦 Modalità: Cartelle da 600MB         │
│ ✓ Organizzazione completata!           │
└─────────────────────────────────────────┘
```

## 🚀 Installazione e Utilizzo

### Windows - Metodo Rapido

1. **Scarica il progetto**
   ```bash
   git clone https://github.com/tuousername/mp3-organizer.git
   cd mp3-organizer
   ```

2. **Avvia con doppio click**
   - Fai doppio click su `avvia_organizzatore.bat`
   - L'interfaccia si aprirà automaticamente

### Crea Eseguibile Standalone (Windows)

1. Doppio click su `crea_eseguibile.bat`
2. Attendi la creazione
3. Troverai `MP3_Organizer.exe` in `dist/`
4. Copia l'exe ovunque - funziona senza Python!

### Linux / macOS

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia interfaccia grafica
python organizza_mp3_gui.py

# Oppure versione console
python organizza_mp3.py
```

## 📖 Come Usare

1. **Seleziona cartella origine** - Dove sono i tuoi MP3
2. **Seleziona cartella destinazione** - Dove creare le cartelle organizzate
3. **Imposta dimensione massima** - Default 600MB per cartella
4. **Scegli modalità**:
   - ☐ Disattivato: Crea cartelle da 600MB (MP3_Collection_Part1, Part2...)
   - ☑ Attivato: Raggruppa per Album usando tag ID3
5. **Clicca Avvia** - Guarda il log per seguire il progresso

## 📂 Esempio Output

### Modalità: Ignora Tag (Default)
```
Destinazione/
├── MP3_Collection_Part1/
│   ├── 001_song1.mp3
│   ├── 002_song2.mp3
│   └── ... (fino a 600MB)
└── MP3_Collection_Part2/
    ├── 051_song51.mp3
    └── ...
```

### Modalità: Usa Tag Album
```
Destinazione/
├── Best Hits 2024/
│   ├── 001_track1.mp3
│   ├── 002_track2.mp3
│   └── 003_track3.mp3
├── Rock Classics/
│   ├── 001_song1.mp3
│   └── 002_song2.mp3
└── Best Hits 2024_Part2/  (se supera 600MB)
    ├── 004_track4.mp3
    └── ...
```

## 🛠️ Requisiti

- Python 3.7+
- mutagen (per leggere tag ID3)
- tkinter (incluso in Python)

## 📦 Dipendenze

```bash
pip install mutagen
```

## 🤝 Contribuire

Contributi benvenuti! Sentiti libero di:
- 🐛 Segnalare bug
- 💡 Proporre nuove funzionalità
- 🔧 Inviare pull request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per dettagli.

## 🙏 Crediti

Sviluppato con ❤️ per organizzare collezioni musicali

---

**Note**: Questo tool è pensato per organizzare file MP3 di tua proprietà. Rispetta sempre i diritti d'autore.

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
