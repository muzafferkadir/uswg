import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import threading
from datetime import datetime
import os
import sys
import subprocess
from unsilence.Unsilence import Unsilence
import tempfile

temp_dir = os.path.join(tempfile.gettempdir(), 'uswg_temp')
os.makedirs(temp_dir, exist_ok=True)
os.environ['TMPDIR'] = temp_dir

class UnsilenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("USWG")
        self.root.geometry("800x600")
        
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

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=20)
        
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
        self.action_button.grid(row=4, column=0, columnspan=3, pady=20, sticky='ew')

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
            # Create base cache directory
            user_cache_dir = os.path.join(os.path.expanduser('~'), 'Library/Caches/uswg')
            os.makedirs(user_cache_dir, exist_ok=True)
            
            # Create unique temp directory for this process
            import uuid
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
            
            unsilence.detect_silence(
                on_silence_detect_progress_update=self.update_progress
            )
            
            unsilence.render_media(
                output_path,
                on_render_progress_update=self.update_progress,
                on_concat_progress_update=self.update_progress
            )
            
            time_passed = datetime.today() - start_time
            self.status_label['text'] = f"✅ Finished in {time_passed.seconds} seconds!"
            
            self.action_button.configure(text="Open Output Folder", command=self.open_output_folder)
            self.action_button['state'] = 'normal'
            
        except Exception as e:
            self.status_label['text'] = f"❌ Error: {str(e)}"
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
