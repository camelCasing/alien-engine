try:
    import pygame
    import json
    import os

    sprites = {}
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
    debug = True

    def executeFunction(sprite, where):
        f = open(where, "r")
        code = f.read()
        f.close()

        for line in code.splitlines():
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