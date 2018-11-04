import pygame

keys = {
    'left' : [pygame.K_LEFT, pygame.K_a],
    'right': [pygame.K_RIGHT, pygame.K_d],
    'up'   : [pygame.K_UP, pygame.K_w],
    'down' : [pygame.K_DOWN, pygame.K_s],
    'activate': [pygame.K_SPACE, pygame.K_RETURN],
    'exit' : [pygame.K_ESCAPE, pygame.K_q],
    'restart': [pygame.K_HOME]
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


def checkDown(action, keys_down):
    """
    Whereas checkPress checks for the currently held keys,
    checkDown checks whether a key has been pressed down
    in the last frame
    (since the last pygame.event.clear()
    :return: boolean
    """
    for binding in keys[action]:
        # print('binding='+str(binding))
        for key_evt in keys_down:
            # print('keydown='+str(key_evt.key))

            if binding == key_evt.key:

                return True
    return False


