import customtkinter as ctk
from detect import run_camera_detection, current_sound_function
import detect
from sound import Playsound1,playsound2
# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main app window
app = ctk.CTk()
app.title("AI Person Detector")
app.geometry("400x300")

# Global variable for camera index
camera_index = ctk.IntVar(value=0)

# Function to set camera
def set_camera(idx):
    camera_index.set(idx)
    cam_label.configure(text=f"Selected Camera: {idx}")

# Function to run detection
def start_detection():
    idx = camera_index.get()
    run_camera_detection(camera_index=idx)

# --- UI Components ---

def sound1():
    detect.current_sound_function = Playsound1
    sound_btn.configure(text="sound 1 ✅")

def sound2():
    detect.current_sound_function=playsound2
    sound_btn.configure(text="sound 2 ✅")
# Camera label
cam_label = ctk.CTkLabel(app, text="Selected Camera: 0", font=ctk.CTkFont(size=16))
cam_label.place(x=110, y=30)

# Horizontal spacing variables
btn_width = 80
padding = 20

# Camera buttons with padding
cam1_btn = ctk.CTkButton(app, text="Cam 0", command=lambda: set_camera(0), width=btn_width)
cam1_btn.place(x=30, y=90)

cam2_btn = ctk.CTkButton(app, text="Cam 1", command=lambda: set_camera(1), width=btn_width)
cam2_btn.place(x=30 + btn_width + padding, y=90)

cam3_btn = ctk.CTkButton(app, text="Cam 2", command=lambda: set_camera(2), width=btn_width)
cam3_btn.place(x=30 + 2 * (btn_width + padding), y=90)


sound_btn = ctk.CTkButton(app, text="sound 1",  command=sound1,width=btn_width)
sound_btn.place(x=120, y=140)

sound_btn2 = ctk.CTkButton(app, text="sound 2",  command=sound2,width=btn_width)
sound_btn2.place(x=220, y=140)
# Start detection button
start_btn = ctk.CTkButton(app, text="Start Detection", fg_color="green", hover_color="darkgreen", command=start_detection)
start_btn.place(x=120, y=180)

# Run app
app.mainloop()
