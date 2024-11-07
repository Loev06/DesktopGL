from screeninfo import get_monitors

import logging
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
    
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--display", help="Selects a monitor", type=str, default="\\\\.\\DISPLAY1")

    args, files = args.parse_known_args()
    args = args.__dict__

    if "display" in args:
        selected_monitor = get_monitor(args["display"])
        if selected_monitor is None:
            err = "Invalid monitor name. Available monitors:"
            for monitor in get_monitors():
                err += f"\n\t{monitor.name}"
            logger.error(err)
            return
    else:
        selected_monitor = get_monitor(None)

if __name__ == "__main__":
    main()