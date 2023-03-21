try:
    import pygame.mixer
    import pygame
    import random
    import json
    import sys
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

    #bgName = manifest["background"]
    #bg = pygame.image.load(f"entity/{bgName}/sprite.png")
    #bg = pygame.transform.scale(bg, (manifest["window_width"], manifest["window_height"]))
    #window.blit(bg, (manifest["window_width"] / 2, manifest["window_height"] / 2))

    def executeFunction(spriteId, where):
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
                    elif i.startswith("#this"):
                        line = line.replace(i, spriteId)
                    elif i.startswith("#posX"):
                        print("getting x")
                        entityId = i.spit("(")[1].rstrip(")")
                        print("getting x 2")
                        result = sprites[entityId]["x"]
                        print("getting x 3")
                        line = line.replace(i, result)
                        print("getting x 4")
                    elif i.startswith("#posY"):
                        print("getting y")
                        entityId = i.spit("(")[1].rstrip(")")
                        print("getting y 2")
                        result = sprites[entityId]["y"]
                        print("getting y 3")
                        line = line.replace(i, result)
                        print("getting y 4")
                    elif variables.get(i.lstrip("#")):
                        line = line.replace(i, variables[i.lstrip("#")])

            if line.startswith("move"):
                if sprites.get(line.split(" ")[1]):
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

                if os.path.exists(f"entity/{spriteName}/on_load"):
                    executeFunction(None, f"entity/{spriteName}/on_load")
            elif line.startswith("set"):
                variables[line.split(" ")[1]] = line.split(" ")[2]
            elif line.startswith("sound"):
                if line.split(" ")[1] == "play":
                    soundId = line.split(" ")[2]

    def onKeyPress(keyString):
        for sprite in sprites:
            spriteName = sprites[sprite]["source"]
            if os.path.exists(f"entity/{spriteName}/on_press_{keyString}"):
                executeFunction(sprite, f"entity/{spriteName}/on_press_{keyString}")

    def onKeyRelease(keyString):
        for sprite in sprites:
            spriteName = sprites[sprite]["source"]
            if os.path.exists(f"entity/{spriteName}/on_release_{keyString}"):
                executeFunction(sprite, f"entity/{spriteName}/on_release_{keyString}")

    def onMouseDown():
        for sprite in sprites:
            spriteName = sprites[sprite]["source"]
            if os.path.exists(f"entity/{spriteName}/on_mouse_down"):
                executeFunction(sprite, f"entity/{spriteName}/on_mouse_down")

    def onMouseUp():
        for sprite in sprites:
            spriteName = sprites[sprite]["source"]
            if os.path.exists(f"entity/{spriteName}/on_mouse_up"):
                executeFunction(sprite, f"entity/{spriteName}/on_mouse_up")

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                onMouseDown()
            elif event.type == pygame.MOUSEBUTTONUP:
                onMouseUp()

        for sprite in sprites:
            spriteName = sprites[sprite]["source"]
            if os.path.exists(f"entity/{spriteName}/on_render"):
                executeFunction(sprite, f"entity/{spriteName}/on_render")

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

except Exception as err:
    print(err)

input()
