import pygame
from settings import *

class Tower(pygame.sprite.Sprite):
    
    
    def __init__(self, pos, image, range_, damage, group):
        super().__init__(group)  # add to group automatically
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.range = range_
        self.damage = damage


    def update(self, dt, monsters):
        # Find nearest monster in range
        nearest = None
        min_dist = float('inf')
        for m in monsters:
            distance = self.pos.distance_to(m.pos)
            if distance < self.range and distance < min_dist:
                nearest = m
                min_dist = distance
        self.target = nearest

        if self.target:
            # For now just print attack for testing
            print(f"Attacking {self.target}!")
