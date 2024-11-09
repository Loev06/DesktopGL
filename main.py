import screeninfo
import argparse

from logging_format import logger
from frame_limiter import FrameLimiter
from glfw_window import GLFWWindow

def get_monitor_with_name(name: str | None) -> screeninfo.Monitor | None:
    monitors = screeninfo.get_monitors()
    if name is None:
        return monitors[0]
    
    for monitor in monitors:
        if monitor.name == name:
            return monitor

    return None

def get_primary_monitor() -> screeninfo.Monitor:
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            return monitor
    return screeninfo.get_monitors()[0]

def main():
    all_args = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    all_args.add_argument("-d", "--display", help="Selects a monitor", type=str, default=None)
    all_args.add_argument("-f", "--framelimit", help="Sets the maximum frame rate", type=int, default=60)
    all_args.add_argument("files", nargs="*")

    args = all_args.parse_args()

    if len(args.files) == 0:
        all_args.print_help()
        return

    if args.display:
        selected_monitor = get_monitor_with_name(args.display)
        if selected_monitor is None:
            err = "Invalid monitor name. Available monitors:"
            for monitor in screeninfo.get_monitors():
                err += f"\n\t{monitor.name}"
            logger.error(err)
            return
    else:
        selected_monitor = get_primary_monitor()
    
    logger.info(f"Selected monitor: {selected_monitor.name}")

    frame_limiter = FrameLimiter(args.framelimit)
    glfw_window = GLFWWindow(selected_monitor, screeninfo.get_monitors()[0])

    for monitor in screeninfo.get_monitors():
        logger.info(f"Monitor: {monitor.name} {monitor.is_primary}, {monitor.width}x{monitor.height}, {monitor.x},{monitor.y}")

    try:
        while glfw_window.is_running():
            frame_limiter.tick()
            glfw_window.render()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt")

if __name__ == "__main__":
    main()