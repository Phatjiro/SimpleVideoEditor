import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess


class SimpleVideoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Video Editor")

        # path to get and save video
        self.video1_path = tk.StringVar()
        self.video2_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # path to change and save video volume change
        self.video_volume_path = tk.StringVar()
        self.volume_index = tk.DoubleVar()
        self.volume_index.set(1.0)
        self.volume_output_path = tk.StringVar()
        self.audio_output_path = tk.StringVar()

        # create UI
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tab_merge = ttk.Frame(notebook)
        tab_up_volume = ttk.Frame(notebook)
        notebook.add(tab_merge, text="Merge Video")
        notebook.add(tab_up_volume, text="Up Volume")

        # tab merge video
        tk.Label(tab_merge, text="Video 1:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(tab_merge, textvariable=self.video1_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(tab_merge, text="Browse", command=self.browse_video1).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(tab_merge, text="Video 2:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(tab_merge, textvariable=self.video2_path, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(tab_merge, text="Browse", command=self.browse_video2).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(tab_merge, text="Output Video:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(tab_merge, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(tab_merge, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=10, pady=10)

        tk.Button(tab_merge, text="Merge Videos", command=self.merge_videos).grid(row=3, column=0, columnspan=3, pady=20)

        # tab up volume
        tk.Label(tab_up_volume, text="Video:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(tab_up_volume, textvariable=self.video_volume_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(tab_up_volume, text="Browse", command=self.browse_video_volume).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(tab_up_volume, text="Output Video:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(tab_up_volume, textvariable=self.volume_output_path, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(tab_up_volume, text="Browse", command=self.browse_volume_output).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(tab_up_volume, text="Index Volume:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(tab_up_volume, textvariable=self.volume_index, width=50).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(tab_up_volume, text="Change Volume", command=self.change_volume).grid(row=3, column=0, columnspan=3, pady=20)

        tk.Label(tab_up_volume, text="Output Audio:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(tab_up_volume, textvariable=self.audio_output_path, width=50).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(tab_up_volume, text="Browse", command=self.browse_audio_output).grid(row=4, column=2, padx=10, pady=10)

        tk.Button(tab_up_volume, text="Export Audio", command=self.export_audio).grid(row=5, column=0, columnspan=3, pady=20)

    def browse_video1(self):
        file_path = filedialog.askopenfilename(title="Select Video 1", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video1_path.set(file_path)

    def browse_video2(self):
        file_path = filedialog.askopenfilename(title="Select Video 2", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video2_path.set(file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(title="Save Merged Video", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.output_path.set(file_path)

    def merge_videos(self):
        video1 = self.video1_path.get()
        video2 = self.video2_path.get()
        output = self.output_path.get()

        if not video1 or not video2 or not output:
            messagebox.showerror("Error", "Please select both videos and output file.")
            return

        try:
            with open("input.txt", "w") as f:
                f.write(f"file '{video1}'\n")
                f.write(f"file '{video2}'\n")

            command = f"ffmpeg -f concat -safe 0 -i input.txt -c copy \"{output}\""

            subprocess.run(command, shell=True, check=True)

            messagebox.showinfo("Success", "Videos merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def browse_video_volume(self):
        file_path = filedialog.askopenfilename(title="Select Video Change Volume", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video_volume_path.set(file_path)

    def browse_volume_output(self):
        file_path = filedialog.asksaveasfilename(title="Save Change Volume Video", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.volume_output_path.set(file_path)

    def change_volume(self):
        video_volume = self.video_volume_path.get()
        volume_index = self.volume_index.get()
        volume_output = self.volume_output_path.get()

        if not video_volume:
            messagebox.showerror("Error", "Please select video to change volume.")
            return

        try:
            command = f"ffmpeg -i \"{video_volume}\" -filter:a \"volume={volume_index}\" -c:v copy -c:a aac \"{volume_output}\""
            print(command)
            subprocess.run(command, shell=True, check=True)

            messagebox.showinfo("Success", "Videos change successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def browse_audio_output(self):
        file_path = filedialog.asksaveasfilename(title="Save Audio", defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.audio_output_path.set(file_path)

    def export_audio(self):
        video_volume = self.video_volume_path.get()
        audio_output = self.audio_output_path.get()

        if not audio_output:
            messagebox.showerror("Error", "Please select audio to export.")
            return

        try:
            command = f"ffmpeg -i \"{video_volume}\" -q:a 0 -map a \"{audio_output}\""
            print(command)
            subprocess.run(command, shell=True, check=True)

            messagebox.showinfo("Success", "Audio export successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleVideoEditor(root)
    root.mainloop()

