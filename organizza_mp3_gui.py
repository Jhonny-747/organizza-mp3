#!/usr/bin/env python3
"""
Organizzatore MP3 con interfaccia grafica
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import re
import threading


class MP3OrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizzatore MP3")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Variabili
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.max_size = tk.IntVar(value=600)
        self.use_tags = tk.BooleanVar(value=False)  # Default: ignora i tag
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titolo
        title = ttk.Label(main_frame, text="🎵 Organizzatore MP3", 
                         font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Cartella origine
        ttk.Label(main_frame, text="Cartella Origine:", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.source_dir, 
                 width=50).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Sfoglia...", 
                  command=self.browse_source).grid(row=2, column=2, padx=(5, 0))
        
        # Cartella destinazione
        ttk.Label(main_frame, text="Cartella Destinazione:", 
                 font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.dest_dir, 
                 width=50).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Sfoglia...", 
                  command=self.browse_dest).grid(row=4, column=2, padx=(5, 0))
        
        # Dimensione massima
        size_frame = ttk.Frame(main_frame)
        size_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=10)
        ttk.Label(size_frame, text="Dimensione massima per cartella (MB):", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        ttk.Spinbox(size_frame, from_=100, to=2000, textvariable=self.max_size, 
                   width=10).pack(side=tk.LEFT, padx=10)
        
        # Opzione tag
        tag_frame = ttk.Frame(main_frame)
        tag_frame.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Checkbutton(tag_frame, 
                       text="Raggruppa per Album/Compilation (usa tag ID3)", 
                       variable=self.use_tags).pack(side=tk.LEFT)
        ttk.Label(tag_frame, text="← Se disattivato, crea cartelle da 600MB senza usare i tag", 
                 font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=10)
        
        # Pulsante Avvia
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=15)
        
        self.start_button = tk.Button(button_frame, text="▶ Avvia Organizzazione", 
                                       command=self.start_organization, 
                                       bg="#4CAF50", fg="white", 
                                       font=("Arial", 12, "bold"),
                                       padx=30, pady=10,
                                       cursor="hand2")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑 Pulisci Log", 
                             command=self.clear_log,
                             font=("Arial", 10),
                             padx=15, pady=10,
                             cursor="hand2")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(button_frame, text="❌ Esci", 
                            command=self.root.quit,
                            font=("Arial", 10),
                            padx=15, pady=10,
                            cursor="hand2")
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Area di log
        ttk.Label(main_frame, text="Log:", 
                 font=("Arial", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=(10, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = tk.Text(log_frame, height=12, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
    def browse_source(self):
        folder = filedialog.askdirectory(title="Seleziona cartella origine")
        if folder:
            self.source_dir.set(folder)
            # Se destinazione è vuota, usa la stessa cartella
            if not self.dest_dir.get():
                self.dest_dir.set(folder)
    
    def browse_dest(self):
        folder = filedialog.askdirectory(title="Seleziona cartella destinazione")
        if folder:
            self.dest_dir.set(folder)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def start_organization(self):
        if self.is_processing:
            return
        
        # Validazione
        if not self.source_dir.get():
            messagebox.showerror("Errore", "Seleziona una cartella origine!")
            return
        
        if not self.dest_dir.get():
            messagebox.showerror("Errore", "Seleziona una cartella destinazione!")
            return
        
        if not Path(self.source_dir.get()).exists():
            messagebox.showerror("Errore", "La cartella origine non esiste!")
            return
        
        # Conferma
        response = messagebox.askyesno(
            "Conferma", 
            f"Organizzare i file MP3 da:\n{self.source_dir.get()}\n\nverso:\n{self.dest_dir.get()}?"
        )
        
        if not response:
            return
        
        # Avvia in thread separato
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(target=self.organize_files)
        thread.daemon = True
        thread.start()
    
    def organize_files(self):
        try:
            organizer = MP3Organizer(
                self.source_dir.get(),
                self.dest_dir.get(),
                self.max_size.get(),
                self.use_tags.get(),
                self.log
            )
            organizer.organize_files()
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Completato", 
                "Organizzazione completata con successo!"
            ))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Errore", 
                f"Errore durante l'organizzazione:\n{str(e)}"
            ))
        finally:
            self.root.after(0, self.finish_processing)
    
    def finish_processing(self):
        self.is_processing = False
        self.start_button.config(state=tk.NORMAL)
        self.progress.stop()


class MP3Organizer:
    def __init__(self, source_dir, dest_dir, max_size_mb, use_tags, log_callback):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.use_tags = use_tags
        self.log = log_callback
        self.compilations = {}
        
    def sanitize_filename(self, name):
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        name = name.strip('. ')
        return name[:200]
    
    def get_compilation_name(self, mp3_file):
        try:
            audio = MP3(mp3_file, ID3=ID3)
            
            if 'TALB' in audio.tags:
                album = str(audio.tags['TALB'])
                if album and album.strip():
                    return self.sanitize_filename(album)
            
            if 'TIT1' in audio.tags:
                return self.sanitize_filename(str(audio.tags['TIT1']))
                
        except Exception as e:
            self.log(f"⚠ Errore lettura tag per {mp3_file.name}: {e}")
        
        return "Sconosciuto"
    
    def get_file_size(self, file_path):
        return file_path.stat().st_size
    
    def organize_files(self):
        self.log("=" * 60)
        self.log("Inizio organizzazione MP3")
        self.log("=" * 60)
        
        # Trova tutti i file MP3
        mp3_files = list(self.source_dir.glob("*.mp3"))
        
        if not mp3_files:
            self.log("❌ Nessun file MP3 trovato nella directory.")
            return
        
        self.log(f"✓ Trovati {len(mp3_files)} file MP3")
        
        if self.use_tags:
            self.log("📋 Modalità: Raggruppa per Album/Compilation (tag ID3)\n")
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
            
            # Mostra riepilogo raggruppamento
            self.log(f"📊 Trovate {len(self.compilations)} compilation diverse:")
            for comp_name, comp_files in self.compilations.items():
                total_mb = sum(f['size'] for f in comp_files) / (1024 * 1024)
                self.log(f"  • {comp_name}: {len(comp_files)} file ({total_mb:.1f}MB)")
            
            # Organizza ogni compilation
            for compilation, files in self.compilations.items():
                self.log(f"\n📁 Processando: {compilation}")
                self.organize_compilation(compilation, files)
        else:
            self.log("📦 Modalità: Cartelle da max 600MB (ignora tag)\n")
            # Raggruppa tutti i file insieme
            all_files = []
            for mp3_file in mp3_files:
                size = self.get_file_size(mp3_file)
                all_files.append({
                    'file': mp3_file,
                    'size': size
                })
            
            self.compilations["MP3_Collection"] = all_files
            self.organize_compilation("MP3_Collection", all_files)
        
        self.log("\n" + "=" * 60)
        self.log("✓ Organizzazione completata!")
        self.log("=" * 60)
    
    def organize_compilation(self, compilation_name, files):
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
                    file_counter
                )
                file_counter += len(current_folder_files)
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
                file_counter
            )
    
    def create_folder_and_move(self, compilation_name, folder_index, files, start_number):
        # Calcola dimensione totale compilation
        total_size = sum(f['size'] for f in self.compilations[compilation_name])
        
        if total_size > self.max_size_bytes:
            folder_name = f"{compilation_name}_Part{folder_index}"
        else:
            folder_name = compilation_name
        
        folder_path = self.dest_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        
        for i, file_info in enumerate(files, start=start_number):
            old_path = file_info['file']
            new_name = f"{i:03d}_{old_path.name}"
            new_path = folder_path / new_name
            
            try:
                # Copia o sposta
                if self.source_dir == self.dest_dir:
                    shutil.move(str(old_path), str(new_path))
                    action = "Spostato"
                else:
                    shutil.copy2(str(old_path), str(new_path))
                    action = "Copiato"
                
                size_mb = file_info['size'] / (1024 * 1024)
                self.log(f"  ✓ {action}: {new_name} ({size_mb:.1f}MB)")
            except Exception as e:
                self.log(f"  ❌ Errore con {old_path.name}: {e}")


def main():
    root = tk.Tk()
    app = MP3OrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
