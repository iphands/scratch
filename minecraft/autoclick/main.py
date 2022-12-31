import time
from pymouse import PyMouse
from pynput.keyboard import Key, Listener
from threading import Thread, Event, Lock

SPEED = 1.5

clicking = Event()
clicking.clear()
running = Event()
running.set()


def click():
    global lock
    global speed
    m = PyMouse()
    while True:
        if not running.is_set():
            print("Clicking thread exiting...")
            break

        lock.acquire()
        time.sleep(SPEED)
        lock.release()

        if not running.is_set():
            print("Clicking thread exiting...")
            break

        if not clicking.is_set():
            continue

        print("Sending click...")
        pos = m.position()
        m.click(pos[0], pos[1])


def on_press(key):
    global lock
    global SPEED
    if key == Key.f6:
        print("Start clicker")
        clicking.set()

    if key == Key.f7:
        print("Stop clicker")
        clicking.clear()


    if key == Key.f9:
        lock.acquire()
        SPEED = SPEED * 0.90
        print(f"- new speed {SPEED}")
        lock.release()

    if key == Key.f10:
        lock.acquire()
        SPEED = SPEED * 1.10
        print(f"+ new speed {SPEED}")
        lock.release()


def on_release(key):
    if key == Key.f8:
        print("F8 pressed EXIT")
        running.clear()
        return False

lock = Lock()
thread = Thread(target=click)
thread.start()

print("Starting keyboard listener...")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    print("Keyboard listener done")
    thread.join()
    print("Clicking thread done")
