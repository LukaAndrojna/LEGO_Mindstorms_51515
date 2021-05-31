from time import ticks_ms
from random import random

from mindstorms.control import wait_for_seconds
from mindstorms import MSHub, MotorPair, DistanceSensor


class Bot:
    def __init__(self, dist: float=5.0, speed: int=50, duration: int=20):
        self._hub = MSHub()
        self._motor_pair = MotorPair('A', 'B')
        self._distance_sensor = DistanceSensor('D')
        self._dist = dist
        self._speed = speed
        self._motor_pair.set_default_speed(speed)
        self._start_time = ticks_ms()
        self._duration = duration * 1e3
    
    def done_matrix(self):
        self._hub.light_matrix.write('Done')
        wait_for_seconds(2)
        self._hub.light_matrix.off()

    def collision_detection(self) -> bool:
        dist = self._distance_sensor.get_distance_cm(True)
        if dist is not None:
            if dist < self._dist:
                return True
        return False

    def collision_aversion(self) -> None:
        rotation = 1 
        if random() < 0.67:
            rotation = 0.5

        speed = self._speed
        if random() > 0.5:
            self._speed

        self._motor_pair.move_tank(1, 'rotations', left_speed=-speed, right_speed=speed)
        self._motor_pair.start()

    def run(self):
        self._motor_pair.start()
        while True:
            if self.collision_detection():
                self.collision_aversion()

            if ticks_ms() - self._start_time > self._duration:
                break
        self._motor_pair.stop()
        self.done_matrix()


def main():
    bot = Bot(duration=5)
    bot.run()

main()