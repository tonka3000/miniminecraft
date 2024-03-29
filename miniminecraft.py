from ursina import Ursina, window, scene
from mmc.game import Game

app = Ursina()

maingame = Game(parent=scene)#parent=camera.ui)
window.borderless = False

app.run()
