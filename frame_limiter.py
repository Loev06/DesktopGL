import glfw
import time

from logging_format import logger

class FrameLimiter:
    def __init__(self, limit: int):
        self.limit = limit
        self.last_time = glfw.get_time()
        
        self.elapsed_time = 0.0
        self.frames = 0
    
    def tick(self) -> float:
        current_time = glfw.get_time()
        elapsed_time = current_time - self.last_time
        time_to_wait = 1 / self.limit - elapsed_time
        
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        
        current_time = glfw.get_time()
        dt = current_time - self.last_time

        self.last_time = current_time
        self.elapsed_time += dt
        self.frames += 1

        if self.elapsed_time >= 1.0:
            logger.info(f"FPS: {self.frames}")
            self.elapsed_time = 0.0
            self.frames = 0

        return elapsed_time