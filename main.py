import customtkinter as ctk
import threading
from detect import run_camera_detection, current_sound_function
import detect
from sound import Playsound1, playsound2
from keypress import press
from message import sendmessage
from pymongo import MongoClient
from datetime import datetime
import time
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# --- MongoDB Setup ---
mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.09x2u1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["sadiasc_data"]
collection = db["sadiasc_collection"]

# --- Thread-safe Flag ---
is_detection_running = False

# --- Thread-safe Execution Wrapper ---
def run_in_thread(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper

# --- Functionality (Exportable) ---
@run_in_thread
def set_camera(idx):
    camera_index.set(idx)
    state["camera"] = idx
    try:
        cam_label.configure(text=f"Selected Camera: {idx}")
    except:
        pass

@run_in_thread
def start_detection():
    global is_detection_running
    if is_detection_running:
        return
    is_detection_running = True
    state["detection"] = True

    idx = camera_index.get()
    number = phone_var.get().strip()

    def detection_task():
        try:
            run_camera_detection(camera_index=idx, number=number)
        finally:
            global is_detection_running
            is_detection_running = False
            state["detection"] = False

    threading.Thread(target=detection_task, daemon=True).start()

@run_in_thread
def stop_detection():
    press()
    state["detection"] = False

@run_in_thread
def sound1():
    detect.current_sound_function = Playsound1
    try:
        sound_btn.configure(text="Sound 1 ✅")
        sound_btn2.configure(text="Sound 2")
    except:
        pass
    state["sound"] = 1

@run_in_thread
def sound2():
    detect.current_sound_function = playsound2
    try:
        sound_btn2.configure(text="Sound 2 ✅")
        sound_btn.configure(text="Sound 1")
    except:
        pass
    state["sound"] = 2

@run_in_thread
def on_volume_change(value):
    try:
        volume_label.configure(text=f"Volume: {int(value)}%")
    except:
        pass
    state["volume"] = int(value)

@run_in_thread
def trigger_message():
    sendmessage(phone_var.get())
    state["number"] = phone_var.get()

# --- State Functions ---
def get_camera(): return camera_index.get()
def get_sound(): return 1 if detect.current_sound_function == Playsound1 else 2
def get_volume(): return int(volume_level.get())
def get_detection_status(): return is_detection_running
def get_number(): return phone_var.get()

def get_status(as_text=False):
    state.update({
        "camera": get_camera(),
        "sound": get_sound(),
        "volume": get_volume(),
        "detection": is_detection_running,
        "number": get_number()
    })
    if as_text:
        return (f"camera: {state['camera']}\n"
                f"sound: {state['sound']}\n"
                f"volume: {state['volume']}%\n"
                f"detection: {'activated' if state['detection'] else 'deactivated'}\n"
                f"number: {state['number']}")
    return state

# --- GUI Setup ---
if __name__ == "__main__":
    app = ctk.CTk(fg_color="#12141A")
    app.title("S.A.D.I.A.S.C. Home Interface")
    app.geometry("540x540")

    camera_index = ctk.IntVar(value=1)
    volume_level = ctk.DoubleVar(value=50)
    phone_var = ctk.StringVar(value="+91")

    state = {
        "camera": camera_index.get(),
        "sound": 1,
        "volume": volume_level.get(),
        "detection": is_detection_running,
        "number": phone_var.get()
    }

    def apply_hover_border_effect(button, normal_color, hover_color):
        def on_enter(e): button.configure(border_color=hover_color)
        def on_leave(e): button.configure(border_color=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

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
    button_style2 = button_style.copy()
    button_style2.update({"hover_color": "green", "border_color": "green"})
    button_style3 = button_style.copy()
    button_style3.update({"hover_color": "red", "border_color": "red"})

    title = ctk.CTkLabel(app, text="S.A.D.I.A.S.C.", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=(20, 0))

    subtitle = ctk.CTkLabel(app, text="Smart Anomaly Detection Intelligence and Surveillance Camera", font=ctk.CTkFont(size=12))
    subtitle.pack(pady=(5, 20))

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

    sound_frame = ctk.CTkFrame(app, fg_color="transparent")
    sound_frame.pack(pady=10)

    sound_btn = ctk.CTkButton(sound_frame, text="Sound 1", command=sound1, **button_style)
    sound_btn.pack(side="left", padx=15)
    apply_hover_border_effect(sound_btn, "#454545", "#0d6efd")

    sound_btn2 = ctk.CTkButton(sound_frame, text="Sound 2", command=sound2, **button_style)
    sound_btn2.pack(side="left", padx=15)
    apply_hover_border_effect(sound_btn2, "#454545", "#0d6efd")

    volume_frame = ctk.CTkFrame(app, fg_color="transparent")
    volume_frame.pack(pady=(10, 5))

    volume_label = ctk.CTkLabel(volume_frame, text=f"Volume: {int(volume_level.get())}%", font=ctk.CTkFont(size=13))
    volume_label.pack()

    volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, variable=volume_level, command=on_volume_change, width=250)
    volume_slider.pack(pady=5)

    phone_frame = ctk.CTkFrame(app, fg_color="transparent")
    phone_frame.pack(pady=(10, 5))

    ctk.CTkLabel(phone_frame, text="Receiver Number:", font=ctk.CTkFont(size=13)).pack()
    phone_entry = ctk.CTkEntry(phone_frame, textvariable=phone_var, width=200)
    phone_entry.pack(pady=5)

    ctk.CTkButton(phone_frame, text="Send Test Message", command=trigger_message, **button_style2).pack(pady=5)

    control_frame = ctk.CTkFrame(app, fg_color="transparent")
    control_frame.pack(pady=20)

    ctk.CTkButton(control_frame, text="Start Detection", command=start_detection, **button_style2).pack(pady=5)
    ctk.CTkButton(control_frame, text="Stop Detection", command=stop_detection, **button_style3).pack(pady=5)

    def print_status():
        print(get_status(as_text=True))

    ctk.CTkButton(app, text="Print Status", command=print_status, **button_style).pack(pady=10)

    @run_in_thread
    def status_logger():
        while True:
            current_status = get_status()
            current_status["timestamp"] = datetime.now()

            # ❗ Remove _id if present to avoid duplicate key error
            current_status.pop("_id", None)

            try:
                collection.insert_one(current_status)
            except Exception as e:
                print("[MongoDB Insert Error]", e)

            print("[Status Logger]\n" + get_status(as_text=True) + "\n")
            time.sleep(5)

    status_logger()  # Starts status logging in background
    app.mainloop()

    print("\n--- Final State ---")
    print(get_status(as_text=True))
