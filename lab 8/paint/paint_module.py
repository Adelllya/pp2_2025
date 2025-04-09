import pygame
from typing import Tuple
import math

width, height = 640,480


class Figure():
    layers = []
    def __init__(self, color:Tuple[int,int,int], screen : pygame.surface.Surface, draw_size : int):
        '''
        The class Figure - parent class of all of the drawable elements. Has list var layers that stores all of the object's to draw them in order
        Initialized with the following parameters (passed on by the user):
        - color - an RGB tuple
        - screen - pygame's main display Surface
        - draw_size - thickness of elements
        Automatically set parameters:
        - drawn - a bool parameter. whether the current object has been drawn
        - added_to_layers - a bool parameter. whether the current object is in the Figure's class var layers.        '''
        self.color = color
        self.screen = screen
        self.drawn = False
        self.added_to_layers = False
        self.draw_size = draw_size

    def add_to_layers(self):
        '''
        Add the current instance to Figure's layers list
        layers list is then sliced to save only the last 1000 layers (for the sake of optimization)
        '''
        Figure.layers.append(self)
        Figure.layers = Figure.layers[-1000:]

    @classmethod
    def draw_all(cls):
        '''
        Blitting each object in the layers list
        '''
        for o in cls.layers:
            if o.added_to_layers:
                o.blit()



class Circle(Figure):
    '''
    The class Circle - child class of Figure. Used to draw circles.
    Has class var enable that turns on/off the drawing circles mode
    Has adjustable thickness
    '''

    enable = False

    def __init__(self, color : Tuple[int, int, int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing as a child of the Figure class.
        Setting radius to 0, and center to None as we did not draw anything at the point of initialization
        '''
        super().__init__(color, screen, draw_size)
        self.radius = 0
        self.center = None
        self.add_to_layers()
    
    def change_size(self, direction : int):
        '''
        Changing the thickness of circle(affects only next circles). The thickness ranges from 5 to the radius of the circle
        '''

        if direction > 0 and self.radius > 0:
            self.draw_size = min(math.ceil(self.radius), self.draw_size + 2)
        elif direction < 0 and self.radius > 0:
            self.draw_size = max(5, self.draw_size - 2)

    
    def draw(self, mouse_pressed : bool):
        '''
        Function that draws a circle based on the current mouse position
        '''

        #getting the mouse position
        pos = pygame.mouse.get_pos()
        if self.center == None:
            #setting the mouse position as center if we have entered the function for the firss time for this instance
            self.center = pos
        
        #calculating the radius using the distance formula
        self.radius = math.sqrt((pos[0] - self.center[0])**2 + (pos[1] - self.center[1])**2)
        #drawing the circle on the screen
        pygame.draw.circle(self.screen, self.color, self.center, self.radius, self.draw_size)
        if self.radius > 5:     #we consider a circle drawn only if it has a more or less visible radius
            self.drawn = True
        self.added_to_layers = True
    
        

    #blitting the final circle on the screen. accessed in the Figure's class method draw_all()
    def blit(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius, self.draw_size)

class Palette():
    '''
    Palette class. Used to activate color selection by blitting a spectrum image and returning a color tuple on mouse click
    '''
    enable = False
    def __init__(self, screen : pygame.surface.Surface):
        self.screen = screen
        self.spectrum = pygame.image.load("color_select.jpg")
        self.spectrum_rect = self.spectrum.get_rect(center = (180, 196))
    
    def draw_spectrum(self):
        #creating an interactive color selection button
        self.spectrum_button = self.screen.blit(self.spectrum, self.spectrum_rect)
    def select_color(self, pressed : Tuple[bool, bool, bool], mouse_pos : Tuple[int, int], current_color : Tuple[int,int,int]):
        #if LMB is pressed on the position of the spectrum button, we return a color value at this point
        #then we automatically swithc off the palette and color selection
        if pressed[0] and self.spectrum_button.collidepoint(mouse_pos):
            Palette.enable = False
            color = self.spectrum.get_at((mouse_pos[0], mouse_pos[1]-80))
            if color == None:
                return current_color
            else:
                return color
        else:
            return current_color




class NRect(Figure):
    '''
    The class NRect - child class of Figure. Used to draw simple rectangles.
    Named NRect to avoid confusion with pygame's Rect class
    Has class var enable that turns on/off the drawing rectangles mode
    Has adjustable thickness
    '''
    enable = False

    def __init__(self, color : Tuple[int, int, int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing as a child of Figure class 
        Setting the start_point to None as we did not put the first point of the rectangle
        '''
        super().__init__(color, screen, draw_size)
        self.start_point = None
        self.add_to_layers()

    def change_size(self, direction : int):
        '''
        Changes the thickness of border lines(affect only the next rects). The min value is 5, the max value of thickness is the largest side of the rectangle
        '''
        if direction > 0 and self.start_point != None:
            self.draw_size = min(max(self.rect.width, self.rect.height), self.draw_size + 2)
        elif direction < 0 and self.start_point != None:
            self.draw_size = max(5, self.draw_size - 2)


    def draw(self, mouse_pressed : bool):
        '''
        Function that draws a rectangle based on the current mouse position
        '''

        #get the mouse's position
        pos = pygame.mouse.get_pos()

        #if we are setting the size for the first time, the mouse's position as the start point
        if self.start_point == None:
            self.start_point = pos
        
        #get the difference between the starting position and the current mouse position
        #we do this to be able to draw rects in all directions
        x = min(self.start_point[0], pos[0])
        y = min(self.start_point[1], pos[1])
    
        #setting the width and the height of the rect
        width = max(pos[0], self.start_point[0]) - x
        height = max(pos[1], self.start_point[1]) - y

        self.rect = pygame.Rect(x, y, width, height)   #adjustable rect
        pygame.draw.rect(self.screen, self.color, self.rect, self.draw_size)
        if self.rect.width > 5 and self.rect.height > 5:
            self.drawn = True   #we consider an object drawn only if it has a more or less defined size
        self.added_to_layers = True

    #blit function - draws finished rectangle
    def blit(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.draw_size)

class Eraser(Figure):
    '''
    Eraser class - child class of Figure.
    When enalbed, draws circles of background color to eraser the objects on the canvas (if the LMB is pressed).
    When the process of erasing is finished i.g. the LMB is not pressed anymore, we create a new instance.
    Has dynamic size.
    '''
    def __init__(self, bg_color : Tuple[int,int,int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing the eraser as a child of Figure class
        The draw_size is set as the radius of circles that are drawn to erase layers on canvas
        '''
        super().__init__(bg_color, screen, draw_size)
        self.enable = False
        self.radius = draw_size
        self.points = []
        self.add_to_layers()


    def change_size(self, direction : int):
        '''
        Changing the size of the circles
        '''
        if direction > 0:
            self.radius = min(self.radius, self.draw_size + 2)
        elif direction < 0:
            self.radius = max(15, self.draw_size - 2)
 

    def erase(self, mouse_pos : Tuple[int,int]):
        '''
        Drawing the circles on the screen.
        mouse_pos parameter is required to place the circles on the mouse's current position
        '''
        
        pygame.draw.circle(self.screen, self.color, mouse_pos, self.radius)
        self.points.append(mouse_pos)
        self.added_to_layers = True
        self.drawn = True
        


    def blit(self):
        for center in self.points:
            pygame.draw.circle(self.screen, self.color, center, self.radius)

    
def drawLine(screen, index, start, end, width, color_mode):
    #default drawing function

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):            
        progress = 1.0 * i /iterations
        aprogress = 1 - progress

        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color_mode, (x,y), width)


def change_size_all(draw_size : int, circle : Circle, nrect : NRect, eraser : Eraser, direction : int):
    #every figure's size is changed correspondingly with their own function (polymorphism, i guess)
    for el in (circle, nrect, eraser):
        el.change_size(direction)
    #changin the size of the default mode
    if direction == 1:
        draw_size = min(40, draw_size + 2)
    elif direction == -1:
        draw_size =  max(5, draw_size - 2)
    return draw_size


    
    
    
