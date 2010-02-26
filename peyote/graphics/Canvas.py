import pygame

class Canvas:
    def __init__(self,size=(256,256)):
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)

    def clear(self,color=(0,0,0)):
        self.surface.fill(color)

    def resize(self,size):
        del self.surface
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        
    
