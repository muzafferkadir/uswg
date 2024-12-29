# USWG - Unsilence With GUI

USWG is an automated video silence removal application with a graphical interface. It helps you remove or speed up silent parts in your video and audio files automatically.

## Features

- Easy-to-use graphical interface
- Support for multiple video/audio formats (mp4, avi, mkv, mov, mp3, wav)
- Real-time progress tracking with progress bar
- Automatic output file naming
- Custom input/output file selection
- Process status notifications
- Open output folder functionality after processing

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

## Supported File Types

- Video: .mp4, .avi, .mkv, .mov
- Audio: .mp3, .wav

## Requirements

- Python 3.x
- Tkinter
- Unsilence library
