import time
import subprocess
import os.path as path
import os
import sys
import shutil

directory = path.dirname(path.abspath(__file__))
voice_model = [directory + "/" + "en_US-libritts_r-medium.onnx", "-s", "7"]
voice_parameters = ["--sentence-silence", "0.2", "--noise-scale", "0.3", "--length-scale", "1.2"]
pressed_keys = set()


def get_piper_binary():
    """Find piper binary: prefer PATH, then fall back to pip-installed location."""
    piper_in_path = shutil.which("piper")
    if piper_in_path:
        return piper_in_path
    try:
        import piper as piper_module
        return os.path.join(os.path.dirname(piper_module.__file__), "..", "..", "..", "..", "bin", "piper")
    except ImportError:
        pass
    raise FileNotFoundError("piper binary not found in PATH or pip packages")


def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY") is not None


def notify(text):
    subprocess.Popen(["notify-send", text], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def read_aloud_stream(text):
    text = clean_text(text)
    notify("Reading aloud, press CTRL+ALT to stop")
    piper_bin = get_piper_binary()
    echo_process = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    piper_process = subprocess.Popen(
        [piper_bin, "--model"] + voice_model + voice_parameters + ["--output-raw"],
        stdin=echo_process.stdout, stdout=subprocess.PIPE
    )
    aplay_process = subprocess.Popen(
        ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"],
        stdin=piper_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    echo_process.stdout.close()
    piper_process.stdout.close()
    return aplay_process


def read_aloud_file(text):
    notify("Reading aloud")
    piper_bin = get_piper_binary()
    echo_process = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    piper_process = subprocess.Popen(
        [piper_bin, "--model"] + voice_model + voice_parameters + ["--output_file", directory + "/output.wav"],
        stdin=echo_process.stdout, stdout=subprocess.PIPE
    )
    time.sleep(0.1)
    aplay_process = subprocess.Popen(
        ["xdg-open", directory + "/output.wav"],
        stdin=piper_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    echo_process.stdout.close()
    piper_process.stdout.close()
    aplay_process.stdout.close()


def on_press(key):
    from pynput import keyboard as kb
    pressed_keys.add(key)
    if kb.Key.alt in pressed_keys and (kb.Key.ctrl_l in pressed_keys or kb.Key.ctrl_r in pressed_keys):
        return False


def on_release(key):
    pressed_keys.discard(key)


def get_selected_text():
    """Get selected text using the appropriate clipboard tool for X11 or Wayland."""
    try:
        if is_wayland():
            return subprocess.check_output(
                ["wl-paste", "--primary", "--no-newline"],
                stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
        else:
            return subprocess.check_output(
                ["xclip", "-o", "-selection", "primary"]
            ).decode("utf-8").strip()
    except FileNotFoundError:
        tool = "wl-clipboard" if is_wayland() else "xclip"
        subprocess.run(["notify-send", "piper-tts: please install " + tool])
        sys.exit(1)
    except subprocess.CalledProcessError:
        subprocess.run(["notify-send", "piper-tts: no text selected"])
        sys.exit(1)


def clean_text(text):
    return text.replace("*", "").replace("\n", " ")


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as file:
            text_to_read = file.read()
        print("converting the following text:")
        print(text_to_read)
        read_aloud_file(text_to_read)
        print("done")
    else:
        text_to_read = get_selected_text()
        text_to_read = clean_text(text_to_read)
        print(text_to_read)

        read_aloud_stream(text_to_read)

        from pynput import keyboard
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        subprocess.Popen(["pkill", "-f", "piper"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    main()
