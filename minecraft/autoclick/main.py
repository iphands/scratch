import time
from pynput.keyboard import Key, Listener
from threading import Thread, Event, Lock

SPEED = 1.5

from Xlib import X
from Xlib.display import Display
from Xlib.ext import xtest
from Xlib.protocol.event import ButtonPress

clicking = Event()
clicking.clear()

running = Event()
running.set()

timer_lock = Lock()
mouse_lock = Lock()

disp = Display()
window = None
pointer_data = None


def click():
    global mouse_lock
    global timer_lock
    global speed
    global pointer_data
    global window

    while True:
        if not running.is_set():
            print("Clicking thread exiting...")
            break

        timer_lock.acquire()
        time.sleep(SPEED)
        timer_lock.release()

        if not running.is_set():
            print("Clicking thread exiting...")
            break

        if not clicking.is_set():
            continue

        mouse_lock.acquire()

        if not pointer_data or not window:
            print("No pointer_data/window!")
            lock.release()
            continue

        x = pointer_data.root_x + 10
        y = pointer_data.root_y + 10
        print(f"Sending click at {x}, {y} to {window}...")

        press_args = {
            "event_type": X.ButtonPress,
            "detail": X.Button1,
            "root": window,
            "x": 10,
            "y": 10,
        }

        release_args = dict(press_args)
        release_args["event_type"] = X.ButtonRelease

        disp.xtest_fake_input(**press_args)
        disp.xtest_fake_input(**release_args)

        # event = ButtonPress(detail=X.Button1,
        #                     child=0,
        #                     root=disp,
        #                     window=window,
        #                     root_x=10,
        #                     root_y=10,
        #                     event_x=10,
        #                     event_y=10,
        #                     state=0x100,
        #                     same_screen=1,
        #                     time=X.CurrentTime)
        # disp.send_event(event)

        disp.flush()
        mouse_lock.release()


def on_press(key):
    global SPEED
    global mouse_lock
    global timer_lock
    global pointer_data
    global window

    if key == Key.f6:
        # Get click location here and use it FOREVER!!!
        mouse_lock.acquire()
        window = disp.get_input_focus()._data["focus"]
        pointer_data = window.query_pointer()
        mouse_lock.release()
        print(f"Start clicker at: {pointer_data}")
        clicking.set()

    if key == Key.f7:
        print("Stop clicker")
        clicking.clear()

    if key == Key.f9:
        timer_lock.acquire()
        SPEED = SPEED * 0.90
        print(f"- new speed {SPEED}")
        timer_lock.release()

    if key == Key.f10:
        timer_lock.acquire()
        SPEED = SPEED * 1.10
        print(f"+ new speed {SPEED}")
        timer_lock.release()


def on_release(key):
    if key == Key.f8:
        print("F8 pressed EXIT")
        running.clear()
        return False


if __name__ == '__main__':
    print("Starting click thread...")
    thread = Thread(target=click)
    thread.start()

    print("Starting keyboard listener...")
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        print("Keyboard listener done")
        thread.join()
        print("Clicking thread done")
