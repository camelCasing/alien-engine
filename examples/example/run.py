import pygame
import json
import os

sprites = {"gamer": {"source": "steve", "x": 100, "y": 100}}
loadedSprites = []

manifestFile = open("manifest.json", "r")
manifest = json.loads(manifestFile.read())
manifestFile.close()
window = pygame.display.set_mode((manifest["window_width"], manifest["window_height"]))
pygame.display.set_caption(manifest["display_name"])
window.fill((manifest["background_colour"][0], manifest["background_colour"][1], manifest["background_colour"][2]))
pygame.display.flip()

running = True
clicked = False

def executeFunction(sprite, where):
    f = open(where, "r")
    code = f.read()
    f.close()

    for line in code.splitlines():
        if line.startswith("move"):
            if sprites.get(line.split(" ")[1]):
                print(line.split(" ")[1])
                if line.split(" ")[2] == "abs":
                    sprites[line.split(" ")[1]]["x"] == int(line.split(" ")[3])
                    sprites[line.split(" ")[1]]["y"] == int(line.split(" ")[4])
                elif line.split(" ")[2] == "rel":
                    sprites[line.split(" ")[1]]["x"] += int(line.split(" ")[3])
                    sprites[line.split(" ")[1]]["y"] += int(line.split(" ")[4])
        elif line.startswith("print"):
            print(line.lstrip("print "))

def scaleObject(object_, width, height):
    pygame.transform.scale(object_, (int(width), int(height)))

def drawSprite(identifier, x ,y):
    global clicked
    spriteRelativePath = "entity/"+identifier+"/"

    image = pygame.image.load(spriteRelativePath+"sprite.png")
    window.blit(image, (x, y))

    imageRect = image.get_rect()
    imageRect.topleft = (x, y)

    if imageRect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            if not clicked:
                clicked = True
                executeFunction(image, spriteRelativePath+"on_click")
        else:
            clicked = False

    loadedSprites.append(image)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sprite in sprites:
        drawSprite(sprites[sprite]["source"], sprites[sprite]["x"], sprites[sprite]["y"])
        
    pygame.display.update()
    window.fill((manifest["background_colour"][0], manifest["background_colour"][1], manifest["background_colour"][2]))

pygame.quit()

input("Press enter to close")
