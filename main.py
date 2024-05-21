import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytube import YouTube
import threading
import time


def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = int(bytes_downloaded / total_size * 100)

    # Update progress bar
    progress_bar["value"] = percentage
    progress_text.set(f"Downloaded: {percentage}%")

    # Update file size label
    file_size_label.config(text=f"File Size: {total_size // 1048576} MB (approx.)")

    # Calculate and update time remaining label
    if bytes_downloaded > 0:
        download_speed = (bytes_downloaded / (time.time() - start_time))  # Bytes per second
        remaining_bytes = total_size - bytes_downloaded
        remaining_time_seconds = remaining_bytes / download_speed
        remaining_time_minutes = remaining_time_seconds / 60
        time_remaining_label.config(text=f"Time Remaining: {remaining_time_minutes:.1f} minutes (approx.)")
        download_speed_mb = download_speed / 1048576  # Convert to MB/s
        download_speed_label.config(text=f"Download Speed: {download_speed_mb:.2f} MB/s")

    root.update_idletasks()
    print(f"Download progress: {percentage}%")


def start_download():
    global start_time
    start_time = time.time()  # Record start time for calculating download speed

    download_button.config(state=tk.DISABLED)
    progress_bar["value"] = 0  # Reset the progress bar
    threading.Thread(target=download_video).start()


def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube video URL.")
        download_button.config(state=tk.NORMAL)
        return

    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showwarning("Input Error", "Please select a save path.")
        download_button.config(state=tk.NORMAL)
        return

    try:
        yt = YouTube(url, on_progress_callback=update_progress)
        quality = quality_var.get()
        if quality == 'Audio':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.filter(res=quality, progressive=True).first()
            if not stream:
                stream = yt.streams.get_highest_resolution()

        if stream:
            file_size = stream.filesize  # Get file size if available
            print(f"File size: {file_size // 1048576} MB (approx.)")  # Convert to MB

        print("Download started...")
        stream.download(output_path=save_path)
        messagebox.showinfo("Success", f"Downloaded: {yt.title}")
    except Exception as e:
        messagebox.showerror("Download Error", f"Error: {e}")
    finally:
        download_button.config(state=tk.NORMAL)
        progress_bar["value"] = 0
        print("Download finished")


# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("400x500")  # Increased height to accommodate new labels

# Create and place the URL label and entry
url_label = tk.Label(root, text="YouTube Video URL:", font=("Helvetica", 12))
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)
# Create and place the Quality label and dropdown
quality_label = tk.Label(root, text="Video Quality:", font=("Helvetica", 12))
quality_label.pack(pady=10)
quality_var = tk.StringVar()
quality_options = ttk.Combobox(root, width=20, textvariable=quality_var)
quality_options['values'] = ('Audio', '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p')
quality_options.current(3)  # Set default value
quality_options.pack(pady=10)
# Create and place the download button
download_button = tk.Button(root, text="Download", command=start_download, font=("Helvetica", 12))
download_button.pack(pady=10)
# Create and place the progress bar
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=10)
# Create and place the progress text
progress_text = tk.StringVar()
progress_label = tk.Label(root, textvariable=progress_text, font=("Helvetica", 12))
progress_label.pack(pady=10)
# Create and place the file size label
file_size_label = tk.Label(root, text="File Size: ", font=("Helvetica", 12))
file_size_label.pack(pady=10)
# Create and place the time remaining label
time_remaining_label = tk.Label(root, text="Time Remaining: ", font=("Helvetica", 12))
time_remaining_label.pack(pady=10)
# Create and place the download speed label
download_speed_label = tk.Label(root, text="Download Speed: ", font=("Helvetica", 12))
download_speed_label.pack(pady=10)

root.mainloop()
