import pygame

keys = {
    'left' : [pygame.K_LEFT, pygame.K_a],
    'right': [pygame.K_RIGHT, pygame.K_d],
    'up'   : [pygame.K_UP, pygame.K_w],
    'down' : [pygame.K_DOWN, pygame.K_s],
    'activate' : [pygame.K_SPACE, pygame.K_RETURN],
    'exit' : [pygame.K_ESCAPE],
    'restart' : [pygame.K_HOME]
}

def checkPress(action, keysPressed):
    """
    checkPress takes in the pygame.key.get_pressed() array and an action string
        to determine whether the action should be executed
    """
    for binding in keys[action]:

        if keysPressed[binding]:

            return True

    return False
