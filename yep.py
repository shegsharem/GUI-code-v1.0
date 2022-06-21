from pynput import keyboard

def on_press(key):
    try:
        return key.char
    except AttributeError:
        return key

def on_release(key):
    return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()