import os
import tkinter as tk
from tkinter import filedialog
from yt_dlp import YoutubeDL

def download_and_convert():
    url = url_entry.get().strip()
    if not url:
        status_label.config(text="Error: Please enter a URL", fg="red")
        return

    # Initialize variable to avoid UnboundLocalError
    temp_filename = None

    try:
        # Update status
        status_label.config(text="Downloading and converting audio...", fg="blue")

        # yt-dlp options with workarounds for 403
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio available
            'outtmpl': 'temp/%(title)s.%(ext)s',  # Save to 'temp' folder
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            },  # Updated User-Agent (Chrome, Feb 2025)
            'cookiesfrombrowser': ('firefox',),  # Load cookies from Firefox (optional, adjust browser)
            'cachedir': False,  # Disable caching to avoid stale data
            'quiet': True,  # Suppress normal output
            'verbose': True,  # Enable verbose logging for debugging
        }

        # Ensure temp folder exists
        os.makedirs("temp", exist_ok=True)

        # Download and convert
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        # Ask user where to save the MP3
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")],
            initialfile=f"{info['title']}.mp3",
            title="Save MP3 As"
        )

        if save_path:
            os.replace(temp_filename, save_path)
            status_label.config(text=f"Success! Saved to {save_path}", fg="green")
        else:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            status_label.config(text="Save canceled", fg="orange")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")
        # Clean up temp file if it exists
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)

    finally:
        # Clean up temp folder if empty
        if os.path.exists("temp") and not os.listdir("temp"):
            os.rmdir("temp")

# Set up the GUI
root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("400x200")
root.resizable(False, False)

tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=download_and_convert)
download_button.pack(pady=10)

status_label = tk.Label(root, text="Ready", fg="black")
status_label.pack(pady=20)

root.mainloop()