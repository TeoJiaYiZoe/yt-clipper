# YouTube Video Clipper

A desktop application for downloading and clipping YouTube videos with precise start and end times.

## Features

- **Precise Clipping**: Specify exact start and end times (HH:MM:SS).
- **Quality Selection**: Choose from 360p up to 4K/2160p, or "Best" available.
- **Custom Output**: Set your own filename and choose a download folder.
- **Modern GUI**: A clean and simple interface that's easy to use.
- **Robust Error Handling**: Includes multiple fallbacks for clipping and FPS issues.
- **Auto Cleanup**: Temporary files are automatically deleted after processing.

---

## Security & Usage Notice

- This tool is intended for **personal use only**.
- Always run it in the provided virtual environment (`venv`) for your safety.
- Do not use this tool to download or distribute copyrighted content without permission.
- The application validates input and manages files safely, but you should always double-check your output folder and filenames to avoid accidental overwrites.

---

## Additional Security Measures & Best Practices

- **Filename Sanitization:** The app automatically removes unsafe characters from output filenames to prevent accidental overwrites or system errors.
- **Overwrite Warning:** If you try to save a file with a name that already exists, the app will ask for confirmation before overwriting.
- **Input Validation:** Only valid YouTube URLs and time formats are accepted. Output folder and filename are checked for safety.
- **Virtual Environment Check:** The app will warn you if you are not running inside the provided virtual environment.
- **Personal Use:** This tool is for your own use. Downloading or sharing copyrighted content without permission may be illegal.
- **Resource Awareness:** For best results, avoid clipping very long videos and make sure you have enough free disk space (at least 2GB recommended).
- **Dependency Management:** All dependencies are managed in the virtual environment. Keep your environment up to date for best security.

---

## Installation

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- Windows Operating System

### Instructions

1.  **Download Project**: Download the files to a folder on your computer.
2.  **Run Setup**: Double-click `run_clipper.bat`. This will:
    - Create a Python virtual environment (`venv` folder).
    - Install all required libraries (`yt-dlp`, `moviepy`, etc.).
    - Launch the application.

The first time you run it, it may take a few minutes to download and install the dependencies. Subsequent launches will be much faster.

## How to Use

1.  **Launch**: Double-click `run_clipper.bat`.
2.  **URL**: Paste a YouTube video URL.
3.  **Times**: Enter the `Start Time` and `End Time` for the clip.
4.  **Filename**: Give your clip a name (e.g., `my-favorite-clip`).
5.  **Folder**: Choose where to save the file (defaults to your `Downloads` folder).
6.  **Quality**: Select your desired video quality.
7.  **Clip It**: Click the **Download & Clip** button.

The application will download the full video to a temporary file, clip it, save the final version, and then delete the temporary file. You will see a success message when it's done.

## Troubleshooting

- **"Download failed"**: Check your internet connection and make sure the URL is a valid, public YouTube video.
- **"Clipping failed" or FPS errors**: The app has built-in fallbacks. If an error still occurs, the video might have an unusual format. Try a different quality setting.
- **"File not found" after download**: This can happen if the video title contains special characters. The issue is usually handled, but if it persists, it's a bug.

---


### This tool is intended for personal use. Please respect YouTube's Terms of Service and the rights of content creators.


