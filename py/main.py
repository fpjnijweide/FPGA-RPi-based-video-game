"""


Sensor Pong


"""
import pygame, sys
import objects, constants

def init():
    """
    init() is called once at the very start of the program and sets up pygame.
    It also set some global variables used inside the pygame loop.
    """
    pygame.init()
    
    #set up screen
    global Screen
    Screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)) 
    #set title of screen
    pygame.display.set_caption("Sensor Pong") 
    
    
    global AllSpritesList
    AllSpritesList = pygame.sprite.Group() #get list of sprites

#    playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
#    playerBall.rect.x = constants.WINDOW_WIDTH  // 2
#    playerBall.rect.y = constants.WINDOW_HEIGHT // 2
    
#    AllSpritesList.add(playerBall) #add this ball to the list of sprites
    global clock
    clock = pygame.time.Clock() #create game clock

    #call Game.__init__()
    game = Game()


def main():
    """
    main() contains the pygame draw loop and is called once every frame.
    Level generation etc should be defined in the objects.Game class
    """
    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # When the game window's [x] is pressed,
                #   exit main() function to end program.
                return

        Screen.fill(constants.colors["BLACK"])


        AllSpritesList.update()

        #draw sprites and refresh Screen
        AllSpritesList.draw(Screen)
        pygame.display.flip()

        #then wait until tick has fully passed
        clock.tick(constants.FPS)
        
        # End of game loop.
        # Note that the game stops updating but is not quit entirely






class Game:
    """

    """
    def __init__(self):
        playerBall = objects.Ball(constants.colors["WHITE"], constants.BALLRADIUS)
        AllSpritesList.add(playerBall)







#execute init() and main() only when program is run directly (not imported)
if __name__ == '__main__':

    init()

    main()

    # Game loop broken, program exits
    pygame.quit()
    print("Thank you for playing")
    print("Program exited.")
    sys.exit()

else:
    print("Imported main.py")




