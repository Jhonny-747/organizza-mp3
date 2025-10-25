#!/usr/bin/env python3
"""
Script per organizzare file MP3 in sottocartelle basate sul tag compilation/album
con limite di 600MB per cartella e numerazione sequenziale dei file.
"""

import os
import shutil
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import re


class MP3Organizer:
    def __init__(self, source_dir, max_size_mb=600):
        self.source_dir = Path(source_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.compilations = {}
        
    def sanitize_filename(self, name):
        """Rimuove caratteri non validi dai nomi di file/cartelle"""
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        name = name.strip('. ')
        return name[:200]  # Limita lunghezza
    
    def get_compilation_name(self, mp3_file):
        """Estrae il nome della compilation/album dai tag ID3"""
        try:
            audio = MP3(mp3_file, ID3=ID3)
            
            # Prova prima con il tag TALB (album)
            if 'TALB' in audio.tags:
                album = str(audio.tags['TALB'])
                if album and album.strip():
                    return self.sanitize_filename(album)
            
            # Fallback su altri tag
            if 'TIT1' in audio.tags:  # Content group
                return self.sanitize_filename(str(audio.tags['TIT1']))
                
        except Exception as e:
            print(f"Errore lettura tag per {mp3_file.name}: {e}")
        
        return "Sconosciuto"
    
    def get_file_size(self, file_path):
        """Ritorna la dimensione del file in bytes"""
        return file_path.stat().st_size
    
    def organize_files(self):
        """Organizza tutti i file MP3 nella directory"""
        # Trova tutti i file MP3
        mp3_files = list(self.source_dir.glob("*.mp3"))
        
        if not mp3_files:
            print("Nessun file MP3 trovato nella directory.")
            return
        
        print(f"Trovati {len(mp3_files)} file MP3")
        
        # Raggruppa per compilation
        for mp3_file in mp3_files:
            compilation = self.get_compilation_name(mp3_file)
            size = self.get_file_size(mp3_file)
            
            if compilation not in self.compilations:
                self.compilations[compilation] = []
            
            self.compilations[compilation].append({
                'file': mp3_file,
                'size': size
            })
        
        # Organizza ogni compilation
        for compilation, files in self.compilations.items():
            print(f"\nProcessando compilation: {compilation}")
            self.organize_compilation(compilation, files)
        
        print("\n✓ Organizzazione completata!")
    
    def organize_compilation(self, compilation_name, files):
        """Organizza i file di una compilation in sottocartelle da max 600MB"""
        # Ordina i file per nome
        files.sort(key=lambda x: x['file'].name)
        
        folder_index = 1
        current_folder_size = 0
        current_folder_files = []
        file_counter = 1
        
        for file_info in files:
            file_size = file_info['size']
            
            # Se aggiungere questo file supera il limite, crea una nuova cartella
            if current_folder_size + file_size > self.max_size_bytes and current_folder_files:
                self.create_folder_and_move(
                    compilation_name, 
                    folder_index, 
                    current_folder_files,
                    file_counter - len(current_folder_files)
                )
                folder_index += 1
                current_folder_size = 0
                current_folder_files = []
            
            current_folder_files.append(file_info)
            current_folder_size += file_size
        
        # Sposta i file rimanenti
        if current_folder_files:
            self.create_folder_and_move(
                compilation_name,
                folder_index,
                current_folder_files,
                file_counter - len(current_folder_files)
            )
    
    def create_folder_and_move(self, compilation_name, folder_index, files, start_number):
        """Crea la cartella e sposta i file con numerazione sequenziale"""
        # Nome cartella
        if len(self.compilations[compilation_name]) > self.max_size_bytes:
            folder_name = f"{compilation_name}_Part{folder_index}"
        else:
            folder_name = compilation_name
        
        folder_path = self.source_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        
        # Sposta e rinomina i file
        for i, file_info in enumerate(files, start=start_number):
            old_path = file_info['file']
            
            # Nuovo nome con numero sequenziale
            new_name = f"{i:03d}_{old_path.name}"
            new_path = folder_path / new_name
            
            try:
                shutil.move(str(old_path), str(new_path))
                size_mb = file_info['size'] / (1024 * 1024)
                print(f"  Spostato: {old_path.name} → {folder_name}/{new_name} ({size_mb:.1f}MB)")
            except Exception as e:
                print(f"  Errore spostando {old_path.name}: {e}")


def main():
    print("=" * 60)
    print("ORGANIZZATORE MP3")
    print("=" * 60)
    
    # Directory corrente
    current_dir = Path.cwd()
    print(f"\nDirectory di lavoro: {current_dir}")
    
    # Conferma
    risposta = input("\nVuoi organizzare i file MP3 in questa directory? (s/n): ")
    if risposta.lower() != 's':
        print("Operazione annullata.")
        return
    
    # Dimensione massima cartella
    try:
        max_size = input("\nDimensione massima per cartella in MB (default 600): ")
        max_size = int(max_size) if max_size.strip() else 600
    except ValueError:
        max_size = 600
    
    print(f"\nInizio organizzazione con limite di {max_size}MB per cartella...")
    
    organizer = MP3Organizer(current_dir, max_size)
    organizer.organize_files()


if __name__ == "__main__":
    main()
