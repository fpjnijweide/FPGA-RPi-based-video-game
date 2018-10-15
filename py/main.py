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
    global screen
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)) 
    #set title of screen
    pygame.display.set_caption("Sensor Pong") 
    
    
    global all_sprites_list
    all_sprites_list = pygame.sprite.Group() #get list of sprites

    playerBall = objects.Ball(constants.WHITE, constants.BALLRADIUS)
    playerBall.rect.x = constants.WINDOW_WIDTH  // 2
    playerBall.rect.y = constants.WINDOW_HEIGHT // 2
    
    all_sprites_list.add(playerBall) #add this ball to the list of sprites
    global clock
    clock=pygame.time.Clock() #create game clock

    #pygame initialized



def main():
    """
    main() contains the game loop and is called once every frame.
    """
    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # When the game window's [x] is pressed,
                #   exit main() function to end program.
                return

        screen.fill(constants.BLACK)


        all_sprites_list.update()

        #draw sprites and refresh screen
        all_sprites_list.draw(screen)
        pygame.display.flip()

        #then wait until tick has fully passed
        clock.tick(constants.FPS)
        
        # End of game loop.
        # Note that the game stops updating but is not quit entirely


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

