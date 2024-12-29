import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from datetime import datetime
import os
import sys
import subprocess
from unsilence.Unsilence import Unsilence
import tempfile
import re
import uuid

temp_dir = os.path.join(tempfile.gettempdir(), 'uswg_temp')
os.makedirs(temp_dir, exist_ok=True)
os.environ['TMPDIR'] = temp_dir

class UnsilenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("USWG")
        self.root.geometry("800x800")
        
        self.error_window = None
        
        self.advanced_options = {
            'audible_speed': tk.DoubleVar(value=1.0),
            'silent_speed': tk.DoubleVar(value=6.0),
            'audible_volume': tk.DoubleVar(value=1.0),
            'silent_volume': tk.DoubleVar(value=0.5),
            'silence_level': tk.DoubleVar(value=-35),
            'silence_time_threshold': tk.DoubleVar(value=0.5),
            'short_interval_threshold': tk.DoubleVar(value=0.3),
            'stretch_time': tk.DoubleVar(value=0.25),
            'minimum_interval_duration': tk.DoubleVar(value=0.25),
            'threads': tk.IntVar(value=2),
            'audio_only': tk.BooleanVar(value=False),
            'drop_corrupted_intervals': tk.BooleanVar(value=False),
            'check_intervals': tk.BooleanVar(value=False)
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Large.TButton', padding=10, font=('Helvetica', 14))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Status.TLabel', font=('Helvetica', 14))
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.grid_columnconfigure(1, weight=3)
        
        # Header
        header = ttk.Label(main_frame, text="USWG Auto Video Silence Remover", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Input file section
        ttk.Label(main_frame, text="Input File:", style='Header.TLabel').grid(row=1, column=0, sticky='w', padx=5)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_path, width=50)
        input_entry.grid(row=1, column=1, sticky='ew', padx=5)
        self.input_button = ttk.Button(
            main_frame, 
            text="Select Input", 
            command=self.select_input,
            style='Large.TButton'
        )
        self.input_button.grid(row=1, column=2, sticky='ew', padx=5)

        # Output file section
        ttk.Label(main_frame, text="Output File:", style='Header.TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=20)
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=50)
        output_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=20)
        self.output_button = ttk.Button(
            main_frame, 
            text="Select Output", 
            command=self.select_output,
            style='Large.TButton'
        )
        self.output_button.grid(row=2, column=2, sticky='ew', padx=5, pady=20)

        # Advanced Options
        self.setup_advanced_options()

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky='ew', pady=20)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=700, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to process", style='Status.TLabel')
        self.status_label.pack()

        # Action button
        self.action_button = ttk.Button(
            main_frame, 
            text="Start Processing", 
            command=self.start_processing,
            style='Large.TButton'
        )
        self.action_button.grid(row=5, column=0, columnspan=3, pady=20, sticky='ew')

    def setup_advanced_options(self):
        advanced_frame = ttk.LabelFrame(self.root, text="Advanced Options", padding="10")
        advanced_frame.pack(fill=tk.X, padx=20, pady=10)

        # Create grid layout
        row = 0
        col = 0
        
        # Speed options
        self.create_option_entry(advanced_frame, "Audible Speed:", 'audible_speed', row, col)
        self.create_option_entry(advanced_frame, "Silent Speed:", 'silent_speed', row, col + 2)
        row += 1

        # Volume options
        self.create_option_entry(advanced_frame, "Audible Volume:", 'audible_volume', row, col)
        self.create_option_entry(advanced_frame, "Silent Volume:", 'silent_volume', row, col + 2)
        row += 1

        # Threshold options
        self.create_option_entry(advanced_frame, "Silence Level (dB):", 'silence_level', row, col)
        self.create_option_entry(advanced_frame, "Silence Time Threshold:", 'silence_time_threshold', row, col + 2)
        row += 1

        # Interval options
        self.create_option_entry(advanced_frame, "Short Interval Threshold:", 'short_interval_threshold', row, col)
        self.create_option_entry(advanced_frame, "Stretch Time:", 'stretch_time', row, col + 2)
        row += 1

        # Other numeric options
        self.create_option_entry(advanced_frame, "Min Interval Duration:", 'minimum_interval_duration', row, col)
        self.create_option_entry(advanced_frame, "Threads:", 'threads', row, col + 2)
        row += 1

        # Checkboxes
        ttk.Checkbutton(advanced_frame, text="Audio Only", variable=self.advanced_options['audio_only']).grid(row=row, column=col, sticky='w', padx=5, pady=2)
        ttk.Checkbutton(advanced_frame, text="Drop Corrupted Intervals", variable=self.advanced_options['drop_corrupted_intervals']).grid(row=row, column=col + 2, sticky='w', padx=5, pady=2)
        row += 1
        ttk.Checkbutton(advanced_frame, text="Check Intervals", variable=self.advanced_options['check_intervals']).grid(row=row, column=col, sticky='w', padx=5, pady=2)

    def create_option_entry(self, parent, label_text, option_name, row, col):
        ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky='w', padx=5, pady=2)
        ttk.Entry(parent, textvariable=self.advanced_options[option_name], width=10).grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)

    def show_error_window(self, error_text):
        if self.error_window:
            self.error_window.destroy()
        
        self.error_window = tk.Toplevel(self.root)
        self.error_window.title("Error Details")
        self.error_window.geometry("600x400")
        
        error_text_widget = tk.Text(self.error_window, wrap=tk.WORD, padx=10, pady=10)
        error_text_widget.pack(fill=tk.BOTH, expand=True)
        error_text_widget.insert(tk.END, error_text)
        error_text_widget.config(state='normal')
        
        copy_button = ttk.Button(
            self.error_window,
            text="Copy Error",
            command=lambda: self.root.clipboard_append(error_text)
        )
        copy_button.pack(pady=10)

    def select_input(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Video/Audio File",
            filetypes=[("Video/Audio files", "*.mp4 *.avi *.mkv *.mov *.mp3 *.wav")]
        )
        if file_path:
            self.input_path.set(file_path)
            input_path = Path(file_path)
            output_path = input_path.parent / f"{input_path.stem}_unsilenced{input_path.suffix}"
            self.output_path.set(str(output_path))
            self.status_label['text'] = "Ready for process"
            self.action_button.configure(text="Start Processing", command=self.start_processing)
            self.action_button['state'] = 'normal'

    def select_output(self):
        initial_file = self.output_path.get() if self.output_path.get() else None
        file_path = filedialog.asksaveasfilename(
            title="Save Output File As",
            initialfile=initial_file,
            filetypes=[("Video/Audio files", "*.mp4 *.avi *.mkv *.mov *.mp3 *.wav")]
        )
        if file_path:
            self.output_path.set(file_path)

    def open_output_folder(self):
        output_dir = str(Path(self.output_path.get()).parent)
        try:
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', output_dir])
            else:  # Linux
                linux_commands = ['xdg-open', 'gnome-open', 'kde-open']
                for cmd in linux_commands:
                    try:
                        subprocess.run([cmd, output_dir])
                        return
                    except FileNotFoundError:
                        if cmd == linux_commands[-1]:
                            raise FileNotFoundError("No suitable file manager found")
                        continue
        except Exception as e:
            self.status_label['text'] = f"Could not open folder: {str(e)}"

    def validate_options(self):
        validation_rules = {
            'audible_speed': (0.1, 10.0),
            'silent_speed': (0.1, 50.0),
            'audible_volume': (0.0, 2.0),
            'silent_volume': (0.0, 2.0),
            'silence_level': (-100, 0),
            'silence_time_threshold': (0.1, 10.0),
            'short_interval_threshold': (0.1, 10.0),
            'stretch_time': (0.0, 5.0),
            'minimum_interval_duration': (0.1, 5.0),
            'threads': (1, 16)
        }

        for option_name, (min_val, max_val) in validation_rules.items():
            try:
                value = self.advanced_options[option_name].get()
                if not min_val <= value <= max_val:
                    raise ValueError(f"{option_name.replace('_', ' ').title()} must be between {min_val} and {max_val}")
            except tk.TclError:
                raise ValueError(f"Invalid value for {option_name.replace('_', ' ').title()}")

        return True
            
    def update_progress(self, current_val, total):
        progress = (current_val / total) * 100
        self.progress_bar['value'] = progress
        self.root.update_idletasks()

    def start_processing(self):
        if not self.input_path.get() or not self.output_path.get():
            self.status_label['text'] = "⚠️ Please select both input and output files"
            return

        self.action_button['state'] = 'disabled'
        self.status_label['text'] = "🔄 Processing..."
        
        thread = threading.Thread(target=self.process_video)
        thread.start()

    def process_video(self):
      try:
          self.validate_options()
          
          # Get advanced options
          options = {name: var.get() for name, var in self.advanced_options.items()}
          
          # Create base cache directory
          user_cache_dir = os.path.join(os.path.expanduser('~'), 'Library/Caches/uswg')
          os.makedirs(user_cache_dir, exist_ok=True)
          
          # Create unique temp directory for this process
          process_temp_dir = os.path.join(user_cache_dir, str(uuid.uuid4()))
          os.makedirs(process_temp_dir, exist_ok=True)
          
          # Create output directory
          output_path = Path(self.output_path.get())
          os.makedirs(output_path.parent, exist_ok=True)
          
          start_time = datetime.today()
          
          unsilence = Unsilence(
              Path(self.input_path.get()),
              temp_dir=Path(process_temp_dir)
          )
          
          # Detect silence with parameters
          unsilence.detect_silence(
              silence_level=options['silence_level'],
              silence_time_threshold=options['silence_time_threshold'],
              short_interval_threshold=options['short_interval_threshold'],
              stretch_time=options['stretch_time'],
              minimum_interval_duration=options['minimum_interval_duration'],
              threads=options['threads'],
              on_silence_detect_progress_update=self.update_progress
          )
          
          # Render media with parameters
          unsilence.render_media(
              output_path,
              audible_speed=options['audible_speed'],
              silent_speed=options['silent_speed'],
              audible_volume=options['audible_volume'],
              silent_volume=options['silent_volume'],
              audio_only=options['audio_only'],
              drop_corrupted_intervals=options['drop_corrupted_intervals'],
              check_intervals=options['check_intervals'],
              on_render_progress_update=self.update_progress,
              on_concat_progress_update=self.update_progress
          )
          
          time_passed = datetime.today() - start_time
          self.status_label['text'] = f"✅ Finished in {time_passed.seconds} seconds!"
          
          self.action_button.configure(text="Open Output Folder", command=self.open_output_folder)
          self.action_button['state'] = 'normal'
              
      except Exception as e:
          error_message = f"Error Details:\n{str(e)}"
          self.status_label['text'] = "❌ Error occurred. Click for details"
          self.status_label.bind('<Button-1>', lambda e: self.show_error_window(error_message))
          self.action_button.configure(text="Start Processing", command=self.start_processing)
          self.action_button['state'] = 'normal'
          
      finally:
          self.progress_bar['value'] = 0

def main():
    root = tk.Tk()
    app = UnsilenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
