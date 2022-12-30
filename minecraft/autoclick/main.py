import time
from pymouse import PyMouse
from pynput.keyboard import Key, Listener
from threading import Thread, Event

clicking = Event()
clicking.clear()
running = Event()
running.set()


def click():
    m = PyMouse()
    while True:
        if not running.is_set():
            print("Clicking thread exiting...")
            break

        time.sleep(2.5)

        if not running.is_set():
            print("Clicking thread exiting...")
            break

        if not clicking.is_set():
            continue
        print("Sending click...")
        pos = m.position()
        m.click(pos[0], pos[1])


def on_press(key):
    if key == Key.f6:
        print("Start clicker")
        clicking.set()
    if key == Key.f7:
        print("Stop clicker")
        clicking.clear()


def on_release(key):
    if key == Key.f8:
        print("F8 pressed EXIT")
        running.clear()
        return False


thread = Thread(target=click)
thread.start()

print("Starting keyboard listener...")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    print("Keyboard listener done")
    thread.join()
    print("Clicking thread done")
