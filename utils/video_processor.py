from unsilence import Unsilence
import os
import sys

class VideoProcessor:
    def __init__(self):
        self.ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
        os.environ['PATH'] = f"/opt/homebrew/bin:{os.environ.get('PATH', '')}"
        os.environ['FFMPEG_BINARY'] = self.ffmpeg_path
        
        self.command_options = {
            'audible_speed': 1.0,
            'silent_speed': 6.0,
            'audible_volume': 1.0,
            'silent_volume': 0.5,
            'silence_level': -35,
            'silence_time_threshold': 0.5,
            'short_interval_threshold': 0.3,
            'stretch_time': 0.25,
            'minimum_interval_duration': 0.25,
            'threads': 2,
            'audio_only': False,
            'check_intervals': False,
            'drop_corrupted_intervals': False
        }

    def process_video(self, input_file: str, output_file: str, 
                     progress_callback, status_callback) -> bool:
        try:
            status_callback("Initializing...")
            progress_callback(0)
            
            unsilence = Unsilence(input_file)
            
            status_callback("Detecting silence...")
            progress_callback(25)
            
            unsilence.detect_silence(
                silence_threshold=self.command_options['silence_level'],
                min_silence_length=self.command_options['silence_time_threshold']
            )
            
            status_callback("Processing video...")
            progress_callback(50)
            
            unsilence.render_media(
                output_file,
                silent_speed=self.command_options['silent_speed'],
                audio_only=self.command_options['audio_only']
            )
            
            return True
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")

    def update_options(self, new_options: dict):
        self.command_options.update(new_options)
