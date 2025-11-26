import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target, damage, image=None, speed=300, groups=None):
        super().__init__(groups)
        self.pos = pygame.Vector2(pos)
        self.target = target
        self.damage = damage
        self.speed = speed

        # Image
        if image is None:
            self.image = pygame.Surface((10,10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255,0,0), (5,5), 5)
        else:
            self.image = image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        if not self.target or not self.target.alive():
            self.kill()
            return

        # Compute direction toward target
        direction = pygame.Vector2(self.target.rect.center) - self.pos
        distance = direction.length()
        if distance <= self.speed * dt:
            # Hit target
            if hasattr(self.target, "take_damage"):
                self.target.take_damage(self.damage)
            self.kill()
        else:
            direction.normalize_ip()
            self.pos += direction * self.speed * dt
            self.rect.center = self.pos
