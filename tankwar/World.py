import pygame
from pygame.locals import *
from pygame.math import Vector2
import random

SCREEN_SIZE = (1920, 1080)
 
class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))
 
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
 
    def remove_entity(self, entity):
        del self.entities[entity.id]
 
    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
 
    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
 
    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.itervalues():
            entity.render(surface)
 
    def get_close_entity(self, name, location, range=100.):
        location = Vector2(*location)
        for entity in self.entities.itervalues():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity
        return None
 
class GameEntity(object):
 
    def __init__(self, world, name, image):
 
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        self.id = 0
 
    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))   
 

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    ant_image = pygame.image.load("ant.png").convert_alpha()
    leaf_image = pygame.image.load("leaf.png").convert_alpha()
    spider_image = pygame.image.load("spider.png").convert_alpha()
 
    for ant_no in xrange(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, w), randint(0, h))
        ant.brain.set_state("exploring")
        world.add_entity(ant)
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        time_passed = clock.tick(30)
 
        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, w), randint(0, h))
            world.add_entity(leaf)
 
        if randint(1, 100) == 1:
            spider = Spider(world, spider_image)
            spider.location = Vector2(-50, randint(0, h))
            spider.destination = Vector2(w+50, randint(0, h))
            world.add_entity(spider)
 
        world.process(time_passed)
        world.render(screen)
 
        pygame.display.update()
 
if __name__ == "__main__":
    run()