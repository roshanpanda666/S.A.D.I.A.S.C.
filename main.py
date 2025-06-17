import customtkinter as ctk
import threading
from detect import run_camera_detection, current_sound_function
import detect
from sound import Playsound1, playsound2
from keypress import press
from message import sendmessage

# Initialize CustomTkinter
app = ctk.CTk(fg_color="#12141A")
app.title("S.A.D.I.A.S.C. Home Interface")
app.geometry("540x540")

# Variables
camera_index = ctk.IntVar(value=0)
volume_level = ctk.DoubleVar(value=50)
is_detection_running = False  # Thread-safety flag

# --- Hover Border Simulation ---
def apply_hover_border_effect(button, normal_color, hover_color):
    def on_enter(e):
        button.configure(border_color=hover_color)
    def on_leave(e):
        button.configure(border_color=normal_color)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# --- Functionality ---
def set_camera(idx):
    camera_index.set(idx)
    cam_label.configure(text=f"Selected Camera: {idx}")

def start_detection():
    global is_detection_running
    if is_detection_running:
        return  # Avoid multiple parallel threads
    is_detection_running = True

    idx = camera_index.get()
    number = phone_var.get().strip()

    def detection_task():
        
        run_camera_detection(camera_index=idx, number=number)
        # Reset after thread completes
        global is_detection_running
        is_detection_running = False

    threading.Thread(target=detection_task, daemon=True).start()

def stop_detection():
    press()

def sound1():
    detect.current_sound_function = Playsound1
    sound_btn.configure(text="Sound 1 ✅")
    sound_btn2.configure(text="Sound 2")

def sound2():
    detect.current_sound_function = playsound2
    sound_btn2.configure(text="Sound 2 ✅")
    sound_btn.configure(text="Sound 1")

def on_volume_change(value):
    volume_label.configure(text=f"Volume: {int(value)}%")

# --- Styling ---
button_style = {
    "fg_color": "#252835",
    "hover_color": "#252835",
    "text_color": "white",
    "border_color": "#454545",
    "border_width": 1,
    "corner_radius": 8,
    "width": 100,
    "font": ctk.CTkFont(size=13, weight="bold")
}
button_style2 = {
    "fg_color": "transparent",
    "hover_color": "green",
    "text_color": "white",
    "border_color": "green",
    "border_width": 1,
    "corner_radius": 8,
    "width": 100,
    "font": ctk.CTkFont(size=13, weight="bold")
}
button_style3 = {
    "fg_color": "transparent",
    "hover_color": "red",
    "text_color": "white",
    "border_color": "red",
    "border_width": 1,
    "corner_radius": 8,
    "width": 100,
    "font": ctk.CTkFont(size=13, weight="bold")
}

# --- UI Layout ---
title = ctk.CTkLabel(app, text="S.A.D.I.A.S.C.", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(20, 0))

subtitle = ctk.CTkLabel(app, text="Smart Anomaly Detection Intelligence and Surveillance Camera", font=ctk.CTkFont(size=12))
subtitle.pack(pady=(5, 20))

# --- Camera Section ---
cam_frame = ctk.CTkFrame(app, fg_color="transparent")
cam_frame.pack(pady=10)

cam_label = ctk.CTkLabel(cam_frame, text="Selected Camera: 0", font=ctk.CTkFont(size=14))
cam_label.pack(pady=(0, 10))

cam_btns = ctk.CTkFrame(cam_frame, fg_color="transparent")
cam_btns.pack()

for i in range(3):
    btn = ctk.CTkButton(cam_btns, text=f"Cam {i}", command=lambda i=i: set_camera(i), **button_style)
    btn.pack(side="left", padx=10)
    apply_hover_border_effect(btn, "#454545", "#0d6efd")

# --- Sound Buttons ---
sound_frame = ctk.CTkFrame(app, fg_color="transparent")
sound_frame.pack(pady=10)

sound_btn = ctk.CTkButton(sound_frame, text="Sound 1", command=sound1, **button_style)
sound_btn.pack(side="left", padx=15)
apply_hover_border_effect(sound_btn, "#454545", "#0d6efd")

sound_btn2 = ctk.CTkButton(sound_frame, text="Sound 2", command=sound2, **button_style)
sound_btn2.pack(side="left", padx=15)
apply_hover_border_effect(sound_btn2, "#454545", "#0d6efd")

# --- Volume Slider ---
volume_frame = ctk.CTkFrame(app, fg_color="transparent")
volume_frame.pack(pady=(10, 5))

volume_label = ctk.CTkLabel(volume_frame, text=f"Volume: {int(volume_level.get())}%", font=ctk.CTkFont(size=13))
volume_label.pack()

volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, variable=volume_level, command=on_volume_change, width=250)
volume_slider.pack(pady=5)

# --- Phone Number Input ---
phone_var = ctk.StringVar(value="+91")
phone_frame = ctk.CTkFrame(app, fg_color="transparent")
phone_frame.pack(pady=(10, 5))

ctk.CTkLabel(phone_frame, text="Receiver Number:", font=ctk.CTkFont(size=13)).pack()
phone_entry = ctk.CTkEntry(phone_frame, textvariable=phone_var, width=200)
phone_entry.pack(pady=5)

def trigger_message():
    sendmessage(phone_var.get())

ctk.CTkButton(phone_frame, text="Send Test Message", command=trigger_message, **button_style2).pack(pady=5)

# --- Detection Controls ---
control_frame = ctk.CTkFrame(app, fg_color="transparent")
control_frame.pack(pady=20)

ctk.CTkButton(control_frame, text="Start Detection", command=start_detection, **button_style2).pack(pady=5)
ctk.CTkButton(control_frame, text="Stop Detection", command=stop_detection, **button_style3).pack(pady=5)

# Run app
app.mainloop()
