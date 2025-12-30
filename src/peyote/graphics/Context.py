import pygame
import cairo
from pprint import pprint

class Context:
    def __init__(self, namespace, dims=(256,256)):
        self._surface = pygame.Surface(dims, pygame.SRCALPHA, 32)
        self._namespace = namespace
        self._background = (0,0,0,0)
        self._cairo_state = None
        
    def clear(self,color=(0,0,0)):
        self._surface.fill(color)

    def size(self, w, h):
        global WIDTH, HEIGHT
        self._namespace["WIDTH"] = w
        self._namespace["HEIGHT"] = h
        del self._surface
        self._surface = pygame.Surface((w,h), pygame.SRCALPHA, 32)
        
    def set_pixel(self, x, y, color):
        self._surface.set_at((x,y),color)

    def get_pixel(self, x, y):
        return self._surface.get_at((x,y))

    def background(self, color):
        self._background = color

    def map_rgb(self,color):
        return self._surface.map_rgb(color)

    def unmap_rgb(self, color_int):
        return self._surface.unmap_rgb(color_int)

    def blit(self, surf, coord):
        self._surface.blit(surf, coord)

    def blit_a(self, a, coord):
        pygame.surfarray.blit_array(self._surface, a)

    def start_cairo_context(self):
        self._pixels = pygame.surfarray.pixels2d(self._surface)
        w, h = self._pixels.shape
        self._cairo_surface = cairo.ImageSurface.create_for_data(self._pixels,
                                                         cairo.FORMAT_ARGB32,
                                                         w, h)
        self._cairo = cairo.Context(self._cairo_surface)
        
        self._restore_cairo_state()

    def end_cairo_context(self):
        self._save_cairo_state()
        
        del self._cairo
        del self._cairo_surface
        del self._pixels

    def _save_cairo_state(self):
        attr_pairs = []
        # print "Saving cairo state."
        for attr_name in dir(self._cairo):
            if attr_name.startswith("get_"):
                settr_name = attr_name.replace("get_", "set_")
                if hasattr(self._cairo, settr_name):
                    attr_pairs.append((attr_name, settr_name))
        self._cairo_state = [
            (getattr(self._cairo, g)(), s)
            for g, s in attr_pairs
            ]
        # pprint(self._cairo_state)
        
    def _restore_cairo_state(self):
        if self._cairo_state:
            for val, settr_name in self._cairo_state:
                # print "Setting: %s, %s" % (settr_name, val)
                if isinstance(val, tuple):
                    getattr(self._cairo, settr_name)(*val)
                else:
                    getattr(self._cairo, settr_name)(val)
        self._cairo_state = None

    def __enter__(self):
        self.start_cairo_context()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.end_cairo_context()
        

                                    
        
        
