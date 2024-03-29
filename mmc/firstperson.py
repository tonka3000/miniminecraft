from ursina import held_keys, time
from ursina.prefabs.first_person_controller import FirstPersonController

class FirstPersonControllerAdvanced(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._fly = True
        self.fly = False

    @property
    def fly(self):
        return self._fly

    @fly.setter
    def fly(self, value:bool):
        self._fly = value
        self.gravity = 0 if self._fly else 1

    def update(self):
        super().update()

        if not self.fly:
            return

        # Fly control
        if held_keys['space']:
            self.position += self.up * time.dt * self.speed
        if held_keys['shift']:
            self.position -= self.up * time.dt * self.speed