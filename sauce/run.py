import keyboard
import pygame
import random
import json
import os

sprites = {}
loadedSprites = []
variables = {}

manifestFile = open("manifest.json", "r")
manifest = json.loads(manifestFile.read())
manifestFile.close()
window = pygame.display.set_mode((manifest["window_width"], manifest["window_height"]))
pygame.display.set_caption(manifest["display_name"])
window.fill((manifest["background_colour"][0], manifest["background_colour"][1], manifest["background_colour"][2]))
pygame.display.flip()

running = True
clicked = False
debug = False

def executeFunction(sprite, where):
    f = open(where, "r")
    code = f.read()
    f.close()

    for line in code.splitlines():
        for i in line.split(" "):
            if i.startswith("#"):
                if i.startswith("#ran"):
                    minimum = i.split("(")[1].rstrip(")").split(".")[0]
                    maximum = i.split("(")[1].rstrip(")").split(".")[1]
                    result = random.randint(int(minimum), int(maximum))
                    line = line.replace(i, str(result))
                elif variables.get(i.lstrip("#")):
                    line = line.replace(i, variables[i.lstrip("#")])

        if line.startswith("move"):
            if sprites.get(line.split(" ")[1]):
                print(line.split(" ")[1])
                if line.split(" ")[2] == "abs":
                    sprites[line.split(" ")[1]]["x"] = int(line.split(" ")[3])
                    sprites[line.split(" ")[1]]["y"] = int(line.split(" ")[4])
                elif line.split(" ")[2] == "rel":
                    sprites[line.split(" ")[1]]["x"] += int(line.split(" ")[3])
                    sprites[line.split(" ")[1]]["y"] += int(line.split(" ")[4])
        elif line.startswith("print"):
            print(line.lstrip("print "))
        elif line.startswith("spawn"):
            spriteName = line.split(" ")[1]
            spriteId = line.split(" ")[2]
            spriteX = int(line.split(" ")[3])
            spriteY = int(line.split(" ")[4])

            createdSprite = {"source": spriteName, "x": spriteX, "y": spriteY}

            sprites[spriteId] = createdSprite
        elif line.startswith("set"):
            variables[line.split(" ")[1]] = line.split(" ")[2]

def onKeyPress(keyString):
    for sprite in os.listdir("entity"):
        if os.path.exists(f"entity/{sprite}/on_press_{keyString}"):
            executeFunction(None, f"entity/{sprite}/on_press_{keyString}")

def onKeyRelease(keyString):
    for sprite in os.listdir("entity"):
        if os.path.exists(f"entity/{sprite}/on_release_{keyString}"):
            executeFunction(None, f"entity/{sprite}/on_release_{keyString}")

def scaleObject(object_, width, height):
    pygame.transform.scale(object_, (int(width), int(height)))

def drawSprite(identifier, x ,y):
    global clicked
    spriteRelativePath = "entity/"+identifier+"/"

    image = pygame.image.load(spriteRelativePath+"sprite.png")
    window.blit(image, (x, y))

    if os.path.exists(spriteRelativePath+"on_load"):
        executeFunction(image, spriteRelativePath+"on_load")

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

for entity in os.listdir("entity"):
    if os.path.exists(f"entity/{entity}/on_start"):
        executeFunction(None, f"entity/{entity}/on_start")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            onKeyPress(event.unicode)
        elif event.type == pygame.KEYUP:
            onKeyRelease(event.unicode)

    for sprite in loadedSprites:
        loadedSprites.remove(sprite)

    for sprite in sprites:
        drawSprite(sprites[sprite]["source"], sprites[sprite]["x"], sprites[sprite]["y"])

    pygame.display.update()
    window.fill((manifest["background_colour"][0], manifest["background_colour"][1], manifest["background_colour"][2]))

    if debug == True:
        print("Loaded Sprites: "+str(loadedSprites))

pygame.quit()

input("Press enter to close")
