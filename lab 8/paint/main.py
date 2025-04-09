import pygame
from paint_module import *

rect_select_img = pygame.image.load("rect_select.png")
circle_select_img = pygame.image.load("circle_select.png")
palette_select_img = pygame.image.load("palette.png")
eraser_select_img = pygame.image.load("eraser.png")

rect_select_rect = rect_select_img.get_rect(center = (40,40))
circle_select_rect = circle_select_img.get_rect(center = (120,40))
palette_select_rect = palette_select_img.get_rect(center = (200,40))
eraser_select_rect = eraser_select_img.get_rect(center = (280,40))

width = 640
height = 480

fps = 120

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    
    #the initial drawing parametersfrom the tutorial
    draw_size = 5
    points = []
    draw_mode = True
    
    #color parameters - default for bg is white, for drawing - black
    color_mode = (0,0,0)
    bg_color = (255,255,255)
    

    #initializing the class instances

    canvas = Figure(bg_color, screen, draw_size)
    
    circle = Circle(color_mode, screen, draw_size)
    nrect = NRect(color_mode, screen, draw_size)
    palette = Palette(screen)
    eraser = Eraser(bg_color, screen, draw_size)
 
    #main loop
    while True:

        pressed_key = pygame.key.get_pressed()
        #get bool values for frequent keys
        alt = pressed_key[pygame.K_LALT] or pressed_key[pygame.K_RALT]
        ctrl = pressed_key[pygame.K_LCTRL] or pressed_key[pygame.K_RCTRL]

        screen.fill(bg_color) 
        canvas.draw_all()

        #mouse parametes
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        
        if Circle.enable:
            #if circle mode is enabled, enter the draw function
            if pressed[0] and not circle_select_button.collidepoint(mouse_pos):
                circle.draw(pressed[0])
            elif not pressed[0] and circle.drawn:
                circle = Circle(color_mode, screen, draw_size)


            #if the current circle is drawn and is added to layers, create a new instance

        elif NRect.enable:
            #the same as for circle
            if pressed[0] and not rect_select_button.collidepoint(mouse_pos):
                nrect.draw(pressed[0])
            elif nrect.drawn and not pressed[0]:
                nrect = NRect(color_mode, screen, draw_size)
            
        elif eraser.enable:
            #if the LMB is pressed activate the erase function
            if pressed[0]:
                eraser.erase(mouse_pos)

            #if the button is lift, and at least something was drawn, we create a new instance of the Eraser class
            elif not pressed[0] and not eraser.drawn:
                eraser = Eraser(bg_color, screen, draw_size)
        elif Palette.enable:
            #if palette is enabled, first we draw the spectrum
            palette.draw_spectrum()
            #then select the color
            color_mode = palette.select_color(pressed, mouse_pos, color_mode)
            #if color is valid, we delete its last component, which is an alpha/transparency value
            if color_mode != None:
                color_mode = color_mode[:3]
        else:
            #if none of the prev modes are selected, the default drawing mode from the tutorial is activated
            draw_mode = True
            i = 0
            while i < len(points) - 1:
                drawLine(screen, i, points[i], points[i + 1], draw_size, color_mode)
                i += 1
           
            
        
        for event in pygame.event.get():
            #quitting logic
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl:
                    return
                if event.key == pygame.K_F4 and alt:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            


                

            #checking if buttons are pressed 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if circle_select_button.collidepoint(event.pos):
                    #switching on/off the selected mode while automatically switching off the others
                    Circle.enable = not Circle.enable
                    NRect.enable = eraser.enable = Palette.enable = draw_mode = False
                    points = []
                elif rect_select_button.collidepoint(event.pos):
                    NRect.enable = not NRect.enable
                    Circle.enable = eraser.enable = Palette.enable = draw_mode = False
                    points = []
                elif eraser_select_button.collidepoint(event.pos):
                    eraser = Eraser(bg_color, screen, draw_size)
                    eraser.enable = not eraser.enable
                    Circle.enable = NRect.enable = Palette.enable =  draw_mode = False
                    points = []
                elif palette_select_button.collidepoint(event.pos):
                    Palette.enable = not Palette.enable
                    Circle.enable = NRect.enable = eraser.enable = draw_mode =  False
                    points = []
              
            #from the original tutorial
            elif event.type == pygame.MOUSEMOTION and draw_mode:
                # if mouse moved, add point to list
                position = event.pos
                points = points + [position]
                points = points[-256:]

            elif event.type == pygame.MOUSEWHEEL:
                #changing the current draw size
                draw_size = change_size_all(draw_size, circle, nrect, eraser, direction=event.dict["y"])
        

        #drawing the panel and select buttons that change the current drawing mode
        pygame.draw.rect(screen, (112,128,144), (0,0,320,80))
        rect_select_button = screen.blit(rect_select_img, rect_select_rect)
        circle_select_button = screen.blit(circle_select_img, circle_select_rect)
        palette_select_button = screen.blit(palette_select_img, palette_select_rect)
        eraser_select_button = screen.blit(eraser_select_img, eraser_select_rect)


        pygame.display.flip()
        
        clock.tick(120)
        

            


main()



