import pygame
from pygame.locals import *
from Maze import Maze
import settings
# this is the first word of august the 137.1th
def main():
    
    #SETUP
    settings.init()
    pygame.init() 
    screen = pygame.display.set_mode([settings.screenWidth, settings.screenHeight])
    running = True
    space = False
    BackgroundColor = (0, 0, 0) # Red, Green, Blue Values. Higher means Brighter, lower means darker. 0, 0, 0 is black, 255, 255, 255 is white
    font = pygame.font.Font('freesansbold.ttf', 16)
    
    maze = Maze(20, 20, 20)
    
    

    while running:

        # This is where it gets your user input. 
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    space = True
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    space = False
            elif event.type == pygame.QUIT:
                running = False
        
        screen.fill(BackgroundColor)
        maze.Kruskal()
        maze.draw_board(screen)

        debugText = font.render("t1", True, (255, 255, 255), (0, 0, 0))
        debugText1 = font.render("t2: ", True, (255, 255, 255), (0, 0, 0))
        textRect1 = debugText.get_rect()
        textRect2 = (debugText1.get_rect()[0],debugText.get_rect()[1] + 16,debugText.get_rect()[2],debugText.get_rect()[3])
        
        screen.blit(debugText, textRect1)
        screen.blit(debugText1, textRect2)

        # Your code should go above HERE_________________________________________________
        
        pygame.display.update()
    #             w,a,s,d
    print("Ending now")
    
if __name__ == "__main__":
    main()