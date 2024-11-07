import screeninfo
import argparse
import glfw

from logging_format import logger
from frame_limiter import FrameLimiter

def get_monitor(name: str | None) -> screeninfo.Monitor | None:
    monitors = screeninfo.get_monitors()
    if name is None:
        return monitors[0]
    
    for monitor in monitors:
        if monitor.name == name:
            return monitor

    return None

def main():
    all_args = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    all_args.add_argument("-d", "--display", help="Selects a monitor", type=str, default=None)
    all_args.add_argument("-f", "--framelimit", help="Sets the maximum frame rate", type=int, default=60)
    all_args.add_argument("files", nargs="*")

    args = all_args.parse_args()

    if len(args.files) == 0:
        all_args.print_help()
        return

    selected_monitor = get_monitor(args.display)
    if selected_monitor is None:
        err = "Invalid monitor name. Available monitors:"
        for monitor in screeninfo.get_monitors():
            err += f"\n\t{monitor.name}"
        logger.error(err)
        return
    
    logger.info(f"Selected monitor: {selected_monitor.name}")

    frame_limiter = FrameLimiter(args.framelimit)

    if not glfw.init():
        logger.error("Failed to initialize GLFW")
        return
    
    logger.info("GLFW initialized")
    
    try:
        while True:
            frame_limiter.tick()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt")

if __name__ == "__main__":
    main()