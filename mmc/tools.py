from ursina import random, color

def random_val(highest):
    return random.Random().random() * highest

def random_color():
    return color.rgb(random_val(255), random_val(255), random_val(255))
