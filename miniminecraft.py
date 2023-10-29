from typing import List
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
Sky()

boxes:List[Button] = []

def random_val(highest):
    return random.Random().random() * highest

def random_color():
    return color.rgb(random_val(255), random_val(255), random_val(255))

def add_box(position):
    boxes.append(Button(
        parent=scene,
        model="cube",
        origin=0.5,
        color=random_color(),#color.blue,
        position=position,
        texture="grass"
    ))


for x in range(20):
    for y in range(20):
        add_box((x,0, y))

def input(key):
    for b in boxes:
        if b.hovered:
            if key == "left mouse down":
                add_box(b.position + mouse.normal)
            if key == "right mouse down":
                boxes.remove(b)
                destroy(b)

app.run()
