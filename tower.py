import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, images, damage=10, range_=100, fire_rate=1.0,
                 projectile_image=None, projectile_speed=300, size=(64, 64)):
        """
        pos: tuple (x, y)
        images: list of Surfaces for tower animation
        damage: damage per projectile
        range_: attack range in pixels
        fire_rate: shots per second
        projectile_image: Surface for projectile
        projectile_speed: speed of projectile
        """
        super().__init__()

        # --- Animation & Images ---
        # Normalize images input
        if isinstance(images, pygame.Surface):
            images = [images]

        # SCALE ALL FRAMES CORRECTLY
        self.images = [pygame.transform.scale(img, size) for img in images]

        self.current_frame = 0
        self.animation_speed = 0.1
        self.time_accumulator = 0.0

        # Set first frame
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=(int(pos[0]), int(pos[1])))

        # Store base image for build animation
        self.original_image = self.image.copy()

        # --- Tower Stats ---
        self.range = range_
        self.damage = damage
        self.fire_rate = fire_rate
        self.cooldown = 0.0
        self.last_shot = 0

        self.projectile_image = projectile_image
        self.projectile_speed = projectile_speed
        self.projectiles = pygame.sprite.Group()

        # --- UI & Selection ---
        self.selected = False
        self.delete_button = None
        self.upgrade_button = None

        # --- Tower States ---
        self.building = True          # True while building animation plays
        self.build_progress = 0.0     # 0.0 → 1.0
        self.upgrading = False
        self.upgrade_progress = 0.0

        # --- Scaling for build/upgrade animation ---
        self.original_image = self.image.copy()
        self.scale_factor = 0.0  # scale for building animation

    # -----------------------------
    # Main update
    # -----------------------------
    def update(self, dt, monsters=None, all_sprites=None):
        self._animate(dt)
        self._handle_building(dt)
        self._handle_upgrade(dt)
        self._attack(monsters, all_sprites)
        self.projectiles.update(dt)

    # -----------------------------
    # Tower Animation
    # -----------------------------
    def _animate(self, dt):
        self.time_accumulator += dt
        if self.time_accumulator >= self.animation_speed:
            frames_to_advance = int(self.time_accumulator / self.animation_speed)
            self.time_accumulator -= frames_to_advance * self.animation_speed
            self.current_frame = (self.current_frame + frames_to_advance) % len(self.images)
            self.original_image = self.images[self.current_frame]
            # Update scaled image if building or upgrading
            self._update_scaled_image()

    # -----------------------------
    # Building Animation
    # -----------------------------
    def _handle_building(self, dt):
        if self.building:
            self.build_progress += dt * 2.0  # speed of build animation
            if self.build_progress >= 1.0:
                self.build_progress = 1.0
                self.building = False
            self._update_scaled_image()

    # -----------------------------
    # Upgrade Animation
    # -----------------------------
    def _handle_upgrade(self, dt):
        if self.upgrading:
            self.upgrade_progress += dt * 2.0
            if self.upgrade_progress >= 1.0:
                self.upgrade_progress = 0.0
                self.upgrading = False
            self._update_scaled_image()

    # -----------------------------
    # Scale image for build/upgrade effect
    # -----------------------------
    def _update_scaled_image(self):
        scale = self.build_progress if self.building else 1.0 + 0.2 * self.upgrade_progress
        size = (max(1, int(self.original_image.get_width() * scale)),
                max(1, int(self.original_image.get_height() * scale)))
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=self.rect.center)

    # -----------------------------
    # Attack Logic
    # -----------------------------
    def _attack(self, monsters, all_sprites):
        if monsters and not self.building:
            self.cooldown -= pygame.time.get_ticks() / 1000.0
            # Find nearest target
            target = self.get_target(monsters)
            if target and pygame.time.get_ticks() - self.last_shot >= 1000 / self.fire_rate:
                self.shoot(target, all_sprites)
                self.last_shot = pygame.time.get_ticks()

    def get_target(self, monsters):
        """Return nearest monster within range"""
        nearest = None
        min_dist_sq = self.range * self.range
        for m in monsters:
            dx = m.rect.centerx - self.rect.centerx
            dy = m.rect.centery - self.rect.centery
            dist_sq = dx*dx + dy*dy
            if dist_sq <= min_dist_sq:
                nearest = m
                min_dist_sq = dist_sq
        return nearest

    def shoot(self, target, all_sprites):
        from projectile import Projectile
        proj = Projectile(
            self.rect.center,
            target,
            self.damage,
            self.projectile_image,
            self.projectile_speed,
            self.projectiles
        )
        if all_sprites:
            all_sprites.add(proj)

    # -----------------------------
    # Upgrade Tower
    # -----------------------------
    def upgrade(self):
        self.damage += 5
        self.range += 20
        self.fire_rate += 0.5
        self.upgrading = True
        self.upgrade_progress = 0.0

    # -----------------------------
    # Selection & UI
    # -----------------------------
    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def draw_selection(self, surface):
        if self.selected:
            cx, cy = self.rect.center
            pygame.draw.circle(surface, (0, 0, 255), (cx, cy), self.range, 2)
            # Upgrade/Delete buttons
            self.delete_button = pygame.Rect(self.rect.right + 10, self.rect.top, 50, 30)
            self.upgrade_button = pygame.Rect(self.rect.right + 10, self.rect.top + 40, 50, 30)
            pygame.draw.rect(surface, (255, 0, 0), self.delete_button)
            pygame.draw.rect(surface, (0, 255, 0), self.upgrade_button)
        else:
            self.delete_button = None
            self.upgrade_button = None
