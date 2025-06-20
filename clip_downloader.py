#!/usr/bin/env python3
"""
YouTube Video Clipper - Downloads and clips videos to exact time ranges
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import shutil
import re

class YouTubeClipper:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Clipper")
        self.root.geometry("650x500")
        self.root.configure(bg='#f0f0f0')
        
        self.check_virtual_env()
        self.show_security_notice()
        
        self.downloads_folder = os.path.expanduser("~/Downloads")
        self.setup_ui()
        
    def check_virtual_env(self):
        # Check if running in a virtual environment
        in_venv = (
            hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
            'VIRTUAL_ENV' in os.environ
        )
        if not in_venv:
            messagebox.showwarning(
                "Virtual Environment Warning",
                "You are NOT running in a Python virtual environment (venv).\n\n"
                "For your safety and best experience, please run this app using the provided venv.\n\n"
                "See the README for instructions."
            )
        
    def show_security_notice(self):
        message = (
            "This tool is intended for PERSONAL USE ONLY.\n\n"
            "Always run it in the provided virtual environment (venv) for your safety.\n\n"
            "Do not use this tool to download or distribute copyrighted content without permission.\n\n"
            "Double-check your output folder and filenames to avoid accidental overwrites."
        )
        messagebox.showwarning("Security & Usage Notice", message)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Clipper", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Clipping Section
        clip_frame = ttk.LabelFrame(main_frame, text="Clipping Settings", padding="10")
        clip_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        clip_frame.columnconfigure(1, weight=1)
        
        # Start time
        ttk.Label(clip_frame, text="Start Time (HH:MM:SS):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.start_time_entry = ttk.Entry(clip_frame, width=15)
        self.start_time_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        self.start_time_entry.insert(0, "00:00:00")
        
        # End time
        ttk.Label(clip_frame, text="End Time (HH:MM:SS):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.end_time_entry = ttk.Entry(clip_frame, width=15)
        self.end_time_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10))
        self.end_time_entry.insert(0, "00:01:00")
        
        # Output filename
        ttk.Label(clip_frame, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.filename_entry = ttk.Entry(clip_frame, width=40)
        self.filename_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.filename_entry.insert(0, "clipped_video")
        
        # Download folder
        folder_frame = ttk.LabelFrame(main_frame, text="Download Settings", padding="10")
        folder_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Download Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.folder_entry = ttk.Entry(folder_frame, width=40)
        self.folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.folder_entry.insert(0, self.downloads_folder)
        
        self.browse_btn = ttk.Button(folder_frame, text="Browse", command=self.browse_folder)
        self.browse_btn.grid(row=0, column=2)
        
        # Quality selection
        ttk.Label(folder_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.quality_var = tk.StringVar(value="720p")
        quality_combo = ttk.Combobox(folder_frame, textvariable=self.quality_var, 
                                   values=["360p", "480p", "720p", "1080p", "1440p", "2160p", "Best"], 
                                   state="readonly", width=10)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Quality info label
        quality_info = ttk.Label(folder_frame, text="Higher quality = larger files & slower processing", 
                                font=('Arial', 8), foreground='gray')
        quality_info.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to clip video")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 20))
        
        self.clip_btn = ttk.Button(button_frame, text="Download & Clip", 
                                  command=self.download_and_clip)
        self.clip_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.downloads_folder)
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            
    def parse_time(self, time_str):
        """Convert HH:MM:SS format to seconds"""
        try:
            parts = time_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            else:
                return int(parts[0])
        except:
            return 0
            
    def validate_inputs(self):
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        filename = self.filename_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return False
            
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid download folder")
            return False
            
        if 'youtube.com' not in url and 'youtu.be' not in url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return False
            
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return False
            
        # Validate times
        start_seconds = self.parse_time(start_time)
        end_seconds = self.parse_time(end_time)
        
        if start_seconds >= end_seconds:
            messagebox.showerror("Error", "Start time must be before end time")
            return False
            
        return True
            
    def sanitize_filename(self, filename):
        # Allow only alphanumeric, dash, underscore, and dot
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Remove any character not in the whitelist
        filename = re.sub(r'[^A-Za-z0-9._-]', '', filename)
        # Prevent path traversal
        filename = filename.lstrip('.').replace('..', '')
        # Prevent empty filename
        if not filename:
            filename = 'clipped_video'
        # Prevent reserved Windows device names
        reserved = {'CON', 'PRN', 'AUX', 'NUL',
                    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
        if filename.upper().split('.')[0] in reserved:
            filename = 'clipped_video'
        return filename
            
    def download_and_clip(self):
        if not self.validate_inputs():
            return
        # Disable UI during processing
        self.clip_btn.config(state='disabled')
        self.progress_var.set("Starting download and clipping...")
        self.progress_bar.start()
        # Get inputs
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        quality = self.quality_var.get()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        filename = self.filename_entry.get().strip()
        # Sanitize filename
        filename = self.sanitize_filename(filename)
        # Check for overwrite
        output_path = os.path.join(folder, f"{filename}.mp4")
        if os.path.exists(output_path):
            confirm = messagebox.askyesno(
                "Overwrite File?",
                f"The file '{output_path}' already exists.\n\nDo you want to overwrite it?"
            )
            if not confirm:
                self.progress_var.set("Operation cancelled by user.")
                self.progress_bar.stop()
                self.clip_btn.config(state='normal')
                return
        # Run in separate thread
        thread = threading.Thread(target=self._download_and_clip_thread, 
                                args=(url, folder, quality, start_time, end_time, filename))
        thread.daemon = True
        thread.start()
        
    def _download_and_clip_thread(self, url, folder, quality, start_time, end_time, filename):
        try:
            # Step 1: Download full video
            self.root.after(0, lambda: self.progress_var.set("Downloading full video..."))
            
            temp_filename = f"temp_{filename}"
            
            # Improved format selection for better quality
            if quality == "Best":
                format_spec = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            elif quality == "2160p":
                format_spec = "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]"
            elif quality == "1440p":
                format_spec = "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]"
            elif quality == "1080p":
                format_spec = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"
            elif quality == "720p":
                format_spec = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"
            elif quality == "480p":
                format_spec = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"
            elif quality == "360p":
                format_spec = "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]"
            else:
                format_spec = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            
            cmd_download = [
                sys.executable, '-m', 'yt_dlp',
                '--format', format_spec,
                '--merge-output-format', 'mp4',
                '--output', os.path.join(folder, f'{temp_filename}.%(ext)s'),
                '--no-playlist',
                '--no-warnings',
                '--prefer-ffmpeg',
                url
            ]
            
            result = subprocess.run(cmd_download, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Download failed: {result.stderr}")
            
            # Find the downloaded file
            temp_files = [f for f in os.listdir(folder) if f.startswith(temp_filename) and f.endswith('.mp4')]
            if not temp_files:
                raise Exception("Downloaded video file not found (no .mp4 file). The download may have produced only audio. Try a different format or check the YouTube video.")
            temp_file = os.path.join(folder, temp_files[0])

            # Check if the temp file is valid before using MoviePy
            if not os.path.exists(temp_file) or os.path.getsize(temp_file) < 1000:
                raise Exception(f"Downloaded file '{temp_file}' is missing or too small to be a valid video.")
            print(f"Temp file: {temp_file}, size: {os.path.getsize(temp_file)} bytes")
            
            # Step 2: Clip the video using moviepy
            self.root.after(0, lambda: self.progress_var.set("Clipping video to specified time range..."))
            
            output_path = os.path.join(folder, f"{filename}.mp4")
            
            # Convert times to seconds
            start_seconds = self.parse_time(start_time)
            end_seconds = self.parse_time(end_time)
            
            # Use moviepy for clipping
            try:
                from moviepy.editor import VideoFileClip
                
                with VideoFileClip(temp_file) as video:
                    # Get video duration
                    video_duration = video.duration
                    video_fps = getattr(video, 'fps', None)
                    if not video_fps or not isinstance(video_fps, (int, float)) or video_fps <= 0:
                        video_fps = 25  # Default fallback FPS
                    print(f"Video duration: {video_duration:.1f} seconds")
                    print(f"Video FPS: {video_fps}")
                    
                    if end_seconds > video_duration:
                        end_seconds = video_duration
                        self.root.after(0, lambda: self.progress_var.set(f"Adjusted end time to video duration: {video_duration:.1f}s"))
                    
                    clipped_video = video.subclip(start_seconds, end_seconds)
                    
                    # Improved video writing settings for better quality and FPS handling
                    write_kwargs = {
                        'codec': 'libx264',
                        'audio_codec': 'aac',
                        'temp_audiofile': 'temp-audio.m4a',
                        'remove_temp': True,
                        'verbose': False,
                        'logger': None,
                        'preset': 'medium',  # Better quality preset
                        'fps': video_fps,  # Use original video FPS or fallback
                        'ffmpeg_params': ['-crf', '18']
                    }
                    
                    # Handle different video formats and FPS issues
                    try:
                        clipped_video.write_videofile(output_path, **write_kwargs)
                    except Exception as fps_error:
                        print(f"FPS error, trying alternative settings: {fps_error}")
                        # Try with default FPS if original FPS fails
                        write_kwargs['fps'] = 25  # Default to 25 FPS
                        clipped_video.write_videofile(output_path, **write_kwargs)
                    
                    clipped_video.close()
                
                # Clean up temporary file
                try:
                    os.remove(temp_file)
                except:
                    pass
                    
                self.root.after(0, lambda: self._process_success(output_path))
                
            except ImportError:
                raise Exception("moviepy is required for clipping. Please install it with: pip install moviepy")
            except Exception as moviepy_error:
                # If moviepy fails, try alternative approach
                print(f"MoviePy error: {moviepy_error}")
                self.root.after(0, lambda: self.progress_var.set("Trying alternative clipping method..."))
                
                # Try using ffmpeg directly for clipping
                try:
                    start_seconds = self.parse_time(start_time)
                    end_seconds = self.parse_time(end_time)
                    duration = end_seconds - start_seconds
                    
                    cmd_ffmpeg = [
                        'ffmpeg', '-i', temp_file,
                        '-ss', str(start_seconds),
                        '-t', str(duration),
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-preset', 'medium',
                        '-crf', '18',
                        output_path,
                        '-y'
                    ]
                    
                    result = subprocess.run(cmd_ffmpeg, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # Clean up temporary file
                        try:
                            os.remove(temp_file)
                        except:
                            pass
                        self.root.after(0, lambda: self._process_success(output_path))
                    else:
                        # If ffmpeg also fails, just copy the file
                        print(f"FFmpeg error: {result.stderr}")
                        try:
                            import shutil
                            shutil.copy2(temp_file, output_path)
                            os.remove(temp_file)
                            self.root.after(0, lambda: self._process_success(output_path))
                        except Exception as copy_error:
                            raise Exception(f"All clipping methods failed: {copy_error}")
                            
                except FileNotFoundError:
                    # If ffmpeg is not available, just copy the file
                    try:
                        import shutil
                        shutil.copy2(temp_file, output_path)
                        os.remove(temp_file)
                        self.root.after(0, lambda: self._process_success(output_path))
                    except Exception as copy_error:
                        raise Exception(f"FFmpeg not found and copy failed: {copy_error}")
                
        except Exception as error:
            error_msg = str(error)
            self.root.after(0, lambda: self._process_error(error_msg))
        finally:
            self.root.after(0, self._process_complete)
            
    def _process_success(self, output_path):
        self.progress_bar.stop()
        self.progress_var.set("Video clipped successfully!")
        messagebox.showinfo("Success", f"Video clipped to your specified time range!\nSaved to: {output_path}")
        
    def _process_error(self, error_msg):
        self.progress_bar.stop()
        self.progress_var.set("Clipping failed")
        messagebox.showerror("Error", f"Failed to clip video:\n{error_msg}")
        
    def _process_complete(self):
        self.clip_btn.config(state='normal')
        
    def clear_all(self):
        self.url_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, "00:00:00")
        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, "00:01:00")
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, "clipped_video")
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.downloads_folder)
        self.progress_var.set("Ready to clip video")
        self.progress_bar.stop()

def main():
    root = tk.Tk()
    app = YouTubeClipper(root)
    root.mainloop()

if __name__ == "__main__":
    main() 