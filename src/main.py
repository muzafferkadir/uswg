import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import platform
import subprocess
from utils.video_processor import VideoProcessor

class VideoSilenceRemoverApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Video Silence Remover")
        self.root.geometry("800x500")
        
        self.video_processor = VideoProcessor()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Large.TButton', padding=10, font=('Arial', 11))
        style.configure('Process.TButton', padding=(40, 25), font=('Arial', 14, 'bold'))
        style.map('Process.TButton',
            background=[('!disabled', '#2ecc71'), ('disabled', '#95a5a6')],
            foreground=[('!disabled', 'white'), ('disabled', '#2c3e50')])

    def create_widgets(self):
        tk.Label(self.root, text="Input File:", font=('Arial', 11)).pack(pady=5)
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=20)
        self.input_entry = tk.Entry(input_frame, font=('Arial', 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Select", style='Large.TButton', 
                  command=self.select_input_file).pack(side=tk.RIGHT)

        tk.Label(self.root, text="Output File:", font=('Arial', 11)).pack(pady=5)
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.X, padx=20)
        self.output_entry = tk.Entry(output_frame, font=('Arial', 11))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Select", style='Large.TButton', 
                  command=self.select_output_file).pack(side=tk.RIGHT)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.settings_button = ttk.Button(button_frame, text="Advanced Settings", 
                                        style='Large.TButton', command=self.show_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        self.process_button = ttk.Button(button_frame, text="Remove Silent Parts", 
                                       style='Process.TButton', command=self.process_file)
        self.process_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.process_button.config(state='disabled')

        self.open_button = ttk.Button(button_frame, text="Open File", 
                                    style='Large.TButton', 
                                    command=lambda: self.open_output_file(self.output_entry.get()))
        self.open_button.pack_forget()

        self.progress_bar = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress_label = tk.Label(self.root, text="Processing: 0%", font=('Arial', 11))
        self.status_label = tk.Label(self.root, text="", font=('Arial', 11))

    def select_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Video/Audio File",
            filetypes=(("Video files", "*.mp4 *.avi *.mkv"), 
                      ("Audio files", "*.mp3 *.wav"), 
                      ("All files", "*.*"))
        )
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)
            
            file_path, file_extension = os.path.splitext(filename)
            output_path = f"{file_path}_unsilenced{file_extension}"
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)
            
            self.process_button.config(state='normal')
            self.open_button.pack_forget()

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".mp4",
            filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
        )
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"Processing: {int(value)}%")
        self.root.update_idletasks()

    def update_status(self, status):
        self.status_label.config(text=status)
        self.root.update_idletasks()

    def show_completion(self):
        completion_frame = tk.Frame(self.root, bg='#2ecc71')
        completion_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        check_label = tk.Label(completion_frame, text='✓', 
                             font=('Arial', 48), bg='#2ecc71', fg='white')
        check_label.pack(pady=10)
        
        complete_label = tk.Label(completion_frame, text='Video Processing Complete!', 
                                font=('Arial', 16, 'bold'), bg='#2ecc71', fg='white')
        complete_label.pack(pady=5)
        
        self.root.after(2000, completion_frame.destroy)

    def process_file_thread(self):
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()
        
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select input and output files!")
            return
        
        try:
            self.process_button.config(state='disabled')
            self.progress_bar.pack(pady=10)
            self.progress_label.pack()
            self.status_label.pack()
            
            success = self.video_processor.process_video(
                input_file, 
                output_file, 
                self.update_progress, 
                self.update_status
            )
            
            if success:
                self.update_progress(100)
                self.show_completion()
                self.open_button.pack(side=tk.LEFT, padx=10)
                self.open_button.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_bar.pack_forget()
            self.progress_label.pack_forget()
            self.status_label.pack_forget()
            self.progress_bar['value'] = 0

    def process_file(self):
        thread = threading.Thread(target=self.process_file_thread)
        thread.daemon = True
        thread.start()

    def open_output_file(self, output_file):
        if os.path.exists(output_file):
            if platform.system() == 'Windows':
                os.startfile(output_file)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', output_file])
            else:
                subprocess.run(['xdg-open', output_file])

    def show_settings(self):
        # Settings window implementation here
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VideoSilenceRemoverApp()
    app.run()
