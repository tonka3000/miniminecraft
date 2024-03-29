from ursina import *
from mmc.firstperson import FirstPersonControllerAdvanced
from mmc.tools import random_color

class Game(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scene = None
        self._pause = False
        self.menu = GameMenu(game=self, parent=camera.ui)
        self.start()
        self._current_text_entity = None

    def start(self):
        if self.scene:
            destroy(self.scene)
        self.pause = False
        self.scene = GameScene(game=self, parent=self)

    def show_text(self, text:str, duration_sec=2):
        '''Show the given text for a specific duration'''
        if self._current_text_entity:
            destroy(self._current_text_entity)
            self._current_text_entity = None

        self._current_text_entity = Text(text=text, origin=(0, 0), scale=2)
        text_entity = self._current_text_entity

        def destroy_text():
            destroy(text_entity)

        invoke(destroy_text, delay=duration_sec)

    @property
    def pause(self):
        return self._pause

    @pause.setter
    def pause(self, value:bool):
        self._pause = value
        if self._pause:
            self.menu.enable()
            self.scene.disable()
            self.scene.player.disable()
        else:
            self.menu.disable()
            self.scene.enable()
            self.scene.enabled = True
            self.scene.player.enable()

    def toggle_pause(self):
        self.pause = not self.pause

    def quit(self):
        application.quit()

    def input(self, key):
        if key == "escape":
            self.toggle_pause()

        if key == "f":
            self.scene.player.fly = not self.scene.player.fly
            self.show_text(f"Fly Mode is {'On' if self.scene.player.fly else 'Off'}")

        for b in self.scene.boxes or []:
            if b.hovered:
                if key == "left mouse down":
                    self.scene.add_box(b.position + mouse.normal)
                if key == "right mouse down":
                    self.scene.boxes.remove(b)
                    destroy(b)

class GameMenu(Entity):
    def __init__(self, game:Game, parent=None):
        super().__init__(parent=parent)

        self.game = game

        self.button_start = Button(scale=(.9,.1), position=(0,0.12,0), parent=self, text='Start')
        self.button_restart = Button(scale=(.9,.1), position=(0,0,0), parent=self, text='Restart')
        self.button_exit = Button(scale=(.9,.1), position=(0,-0.12,0), parent=self, text='Exit')

    def input(self, key):
        if self.button_start.hovered:
            if key == "left mouse down":
                self.game.toggle_pause()
        if self.button_exit.hovered:
            if key == "left mouse down":
                self.game.quit()
        if self.button_restart.hovered:
            if key == "left mouse down":
                self.game.start()


class GameScene(Entity):
    def __init__(self, game:Game, parent=None):
        super().__init__(parent=parent)
        self.game = game
        self.sky = Sky(parent=self)
        self.boxes = []
        for x in range(20):
            for y in range(20):
                self.add_box((x,0, y))
        self.player = FirstPersonControllerAdvanced()

    def add_box(self, position):
        self.boxes.append(Button(
            parent=self,
            model="cube",
            origin=0.5,
            color=random_color(),
            position=position,
            texture="grass"
        ))
