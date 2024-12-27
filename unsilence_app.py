import sys
import os
from unsilence import Unsilence
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import subprocess
import platform

command_options = {
    'audible_speed': "1",
    'silent_speed': "6",
    'audible_volume': "1",
    'silent_volume': "0.5",
    'silence_level': "-35",
    'silence_time_threshold': "0.5",
    'short_interval_threshold': "0.3",
    'stretch_time': "0.25",
    'minimum_interval_duration': "0.25",
    'threads': "2",
    'audio_only': False,
    'check_intervals': False,
    'drop_corrupted_intervals': False
}

def validate_float(value, min_val=None, max_val=None):
    try:
        float_val = float(value)
        if min_val is not None and float_val < min_val:
            return False
        if max_val is not None and float_val > max_val:
            return False
        return True
    except ValueError:
        return False

def validate_int(value, min_val=None, max_val=None):
    try:
        int_val = int(value)
        if min_val is not None and int_val < min_val:
            return False
        if max_val is not None and int_val > max_val:
            return False
        return True
    except ValueError:
        return False

def create_advanced_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Advanced Settings")
    settings_window.geometry("500x600")
    
    main_frame = ttk.Frame(settings_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    settings_vars = {}
    for key in command_options:
        if isinstance(command_options[key], bool):
            settings_vars[key] = tk.BooleanVar(value=command_options[key])
        else:
            settings_vars[key] = tk.StringVar(value=command_options[key])
    
    settings_frame = ttk.LabelFrame(scrollable_frame, text="Settings", padding=10)
    settings_frame.pack(fill="x", padx=5, pady=5)
    
    ttk.Label(settings_frame, text="Audible Speed (>0):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['audible_speed']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Silent Speed (>0):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['silent_speed']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Audible Volume (0-1):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['audible_volume']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Silent Volume (0-1):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['silent_volume']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Silence Level (dB):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['silence_level']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Silence Time Threshold (s):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['silence_time_threshold']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Short Interval Threshold (s):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['short_interval_threshold']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Stretch Time (s):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['stretch_time']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Minimum Interval Duration (s):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['minimum_interval_duration']).pack(fill="x", pady=2)
    
    ttk.Label(settings_frame, text="Threads (1-16):").pack(anchor="w")
    ttk.Entry(settings_frame, textvariable=settings_vars['threads']).pack(fill="x", pady=2)
    
    ttk.Checkbutton(settings_frame, text="Audio Only", variable=settings_vars['audio_only']).pack(anchor="w", pady=2)
    ttk.Checkbutton(settings_frame, text="Check Intervals", variable=settings_vars['check_intervals']).pack(anchor="w", pady=2)
    ttk.Checkbutton(settings_frame, text="Drop Corrupted Intervals", variable=settings_vars['drop_corrupted_intervals']).pack(anchor="w", pady=2)
    
    def validate_and_save():
        validation_rules = {
            'audible_speed': lambda x: validate_float(x, 0),
            'silent_speed': lambda x: validate_float(x, 0),
            'audible_volume': lambda x: validate_float(x, 0, 1),
            'silent_volume': lambda x: validate_float(x, 0, 1),
            'silence_level': lambda x: validate_float(x),
            'silence_time_threshold': lambda x: validate_float(x, 0),
            'short_interval_threshold': lambda x: validate_float(x, 0),
            'stretch_time': lambda x: validate_float(x, 0),
            'minimum_interval_duration': lambda x: validate_float(x, 0),
            'threads': lambda x: validate_int(x, 1, 16)
        }
        
        for key, validate_func in validation_rules.items():
            if key in settings_vars and not isinstance(settings_vars[key], tk.BooleanVar):
                if not validate_func(settings_vars[key].get()):
                    messagebox.showerror("Validation Error", f"Invalid value for {key}")
                    return
        
        global command_options
        command_options = {key: var.get() for key, var in settings_vars.items()}
        settings_window.destroy()
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    ttk.Button(settings_window, text="Save", command=validate_and_save).pack(pady=10)

def select_input_file():
    filename = filedialog.askopenfilename(
        title="Select Video/Audio File",
        filetypes=(("Video files", "*.mp4 *.avi *.mkv"), ("Audio files", "*.mp3 *.wav"), ("All files", "*.*"))
    )
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)
        
        file_path, file_extension = os.path.splitext(filename)
        output_path = f"{file_path}_unsilenced{file_extension}"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)
        
        process_button.config(state='normal')
        open_button.pack_forget()

def select_output_file():
    filename = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".mp4",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    if filename:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, filename)

def update_progress(value):
    progress_bar['value'] = value
    progress_label.config(text=f"Processing: {int(value)}%")
    root.update_idletasks()

def open_output_file(output_file):
    if os.path.exists(output_file):
        if platform.system() == 'Windows':
            os.startfile(output_file)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', output_file])
        else:
            subprocess.run(['xdg-open', output_file])

def show_completion():
    completion_frame = tk.Frame(root, bg='#2ecc71')
    completion_frame.place(relx=0.5, rely=0.5, anchor='center')
    
    check_label = tk.Label(completion_frame, text='✓', font=('Arial', 48), bg='#2ecc71', fg='white')
    check_label.pack(pady=10)
    
    complete_label = tk.Label(completion_frame, text='Video Processing Complete!', 
                            font=('Arial', 16, 'bold'), bg='#2ecc71', fg='white')
    complete_label.pack(pady=5)
    
    root.after(2000, completion_frame.destroy)

def get_unsilence_path():
    if getattr(sys, 'frozen', False):
        if platform.system() == 'Darwin':
            return os.path.join(os.path.dirname(sys.executable), '..', 'Resources', 'unsilence')
        elif platform.system() == 'Windows':
            return os.path.join(os.path.dirname(sys.executable), 'unsilence.exe')
    return 'unsilence'  # fallback for development
    
def process_file_thread():
    input_file = input_entry.get()
    output_file = output_entry.get()
    
    unsilence_path = get_unsilence_path()

    if not input_file or not output_file:
        messagebox.showerror("Error", "Please select input and output files!")
        return
    
    try:
        process_button.config(state='disabled')
        progress_bar.pack(pady=10)
        progress_label.pack()
        status_label.pack()
        
        command = [unsilence_path]
        
        if command_options['audio_only']:
            command.extend(['-ao'])
        if command_options['check_intervals']:
            command.extend(['-ci'])
        if command_options['drop_corrupted_intervals']:
            command.extend(['-dci'])
            
        command.extend(['-as', command_options['audible_speed']])
        command.extend(['-ss', command_options['silent_speed']])
        command.extend(['-av', command_options['audible_volume']])
        command.extend(['-sv', command_options['silent_volume']])
        command.extend(['-sl', command_options['silence_level']])
        command.extend(['-stt', command_options['silence_time_threshold']])
        command.extend(['-sit', command_options['short_interval_threshold']])
        command.extend(['-st', command_options['stretch_time']])
        command.extend(['-mid', command_options['minimum_interval_duration']])
        command.extend(['-t', command_options['threads']])
        
        command.extend([input_file, output_file, '-y'])
        
        if platform.system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                startupinfo=startupinfo
            )
        else:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

        current_phase = "Starting..."
        status_label.config(text=current_phase)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output)
                
                if "Calculating Intervals" in output:
                    current_phase = "Calculating silent intervals..."
                    status_label.config(text=current_phase)
                    update_progress(25)
                elif "Type" in output or "Combined" in output:
                    current_phase = "Processing video..."
                    status_label.config(text=current_phase)
                    update_progress(50)
                elif "Rendering Intervals" in output:
                    current_phase = "Rendering video..."
                    status_label.config(text=current_phase)
                    update_progress(75)
                elif "Combining Intervals" in output:
                    current_phase = "Combining intervals..."
                    status_label.config(text=current_phase)
                    update_progress(90)
                
                root.update()
        
        update_progress(100)
        status_label.config(text="Completed!")
        process_button.config(style='Disabled.TButton')
        show_completion()
        open_button.pack(side=tk.LEFT, padx=10)
        open_button.config(state='normal')
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        progress_bar.pack_forget()
        progress_label.pack_forget()
        status_label.pack_forget()
        progress_bar['value'] = 0

def process_file():
    thread = threading.Thread(target=process_file_thread)
    thread.daemon = True
    thread.start()

root = tk.Tk()
root.title("Video Silence Remover")
root.geometry("800x500")

style = ttk.Style()
style.configure('Large.TButton', padding=10, font=('Arial', 11))
style.configure('Process.TButton', padding=(40, 25), font=('Arial', 14, 'bold'))
style.map('Process.TButton',
    background=[('!disabled', '#2ecc71'), ('disabled', '#95a5a6')],
    foreground=[('!disabled', 'white'), ('disabled', '#2c3e50')])

tk.Label(root, text="Input File:", font=('Arial', 11)).pack(pady=5)
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=20)
input_entry = tk.Entry(input_frame, font=('Arial', 11))
input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(input_frame, text="Select", style='Large.TButton', command=select_input_file).pack(side=tk.RIGHT)

tk.Label(root, text="Output File:", font=('Arial', 11)).pack(pady=5)
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.X, padx=20)
output_entry = tk.Entry(output_frame, font=('Arial', 11))
output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(output_frame, text="Select", style='Large.TButton', command=select_output_file).pack(side=tk.RIGHT)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

settings_button = ttk.Button(button_frame, text="Advanced Settings", style='Large.TButton', command=create_advanced_settings_window)
settings_button.pack(side=tk.LEFT, padx=10)

process_button = ttk.Button(button_frame, text="Remove Silent Parts", style='Process.TButton', command=process_file)
process_button.pack(side=tk.LEFT, padx=20, pady=20)
process_button.config(state='disabled')

open_button = ttk.Button(button_frame, text="Open File", style='Large.TButton', command=lambda: open_output_file(output_entry.get()))
open_button.pack_forget()

progress_bar = ttk.Progressbar(root, length=500, mode='determinate')
progress_label = tk.Label(root, text="Processing: 0%", font=('Arial', 11))
status_label = tk.Label(root, text="", font=('Arial', 11))

root.mainloop()
