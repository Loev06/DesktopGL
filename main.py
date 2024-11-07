from screeninfo import get_monitors

import argparse
import glfw

from logging_format import logger

def get_monitor(name):
    monitors = get_monitors()
    if name is None:
        return monitors[0]
    
    for monitor in monitors:
        if monitor.name == name:
            return monitor

    return None

def main():
    if not glfw.init():
        logger.error("Failed to initialize GLFW")
        return
    
    all_args = argparse.ArgumentParser()
    all_args.add_argument("-d", "--display", help="Selects a monitor", type=str, default=None)
    all_args.add_argument("files", nargs="*")

    args = all_args.parse_args()

    if len(args.files) == 0:
        all_args.print_help()
        return

    selected_monitor = get_monitor(args.display)
    if selected_monitor is None:
        err = "Invalid monitor name. Available monitors:"
        for monitor in get_monitors():
            err += f"\n\t{monitor.name}"
        logger.error(err)
        return

if __name__ == "__main__":
    main()