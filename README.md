# ⚠️ This project is no longer maintained. You can visit [Klyppr](https://github.com/muzafferkadir/klyppr-desktop) instead.

# USWG - Unsilence With GUI
USWG is an automated video silence removal application with a graphical interface. It helps you remove or speed up silent parts in your video and audio files automatically.

> This project is a standalone version of the repo named unsilenced by adding gui. [You can check unsilence repo from here](https://github.com/lagmoellertim/unsilence)


## Demo

### Before 
https://github.com/user-attachments/assets/d88a7acd-ac5c-4d7c-bd44-726c6b1435f0

### After
https://github.com/user-attachments/assets/3e3db21a-bb83-40e4-a29e-e8619413498f



## Features
- Easy-to-use graphical interface
- Support for multiple video/audio formats (mp4, avi, mkv, mov, mp3, wav)
- Real-time progress tracking with progress bar
- Automatic output file naming
- Custom input/output file selection
- Process status notifications
- Open output folder functionality after processing
- Built-in ffmpeg for processing

## Install USWG Mac
![uswg-mac-test](https://github.com/user-attachments/assets/ffd15f50-584e-4533-8908-4aad65db70ad)

## Demo on Windows
![Animation](https://github.com/user-attachments/assets/65df78c5-bc75-4e0b-98c2-547c863bc83b)

## How to Use
1. Launch the application
2. Click "Select Input" to choose your video/audio file
3. Output file path will be automatically set, or click "Select Output" to choose custom location
4. Click "Start Processing" to begin silence removal
5. Monitor progress through the progress bar
6. When complete, click "Open Output Folder" to access your processed file

## Technical Details
- Built with Python and Tkinter
- Multi-threaded processing for responsive UI
- Temporary files managed in user's cache directory
- Progress tracking for silence detection and rendering
- Error handling with user-friendly messages

## Requirements
- Python 3.x
- Tkinter
- Unsilence library
