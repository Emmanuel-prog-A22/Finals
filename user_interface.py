from settings import *

class UserInterface(pygame.sprite.Sprite):
    def __init__(self, name, pos, surface, scale, group, game_width=1280, game_height=704):
        super().__init__(group)
        self.name = name
        self.game_width = game_width
        self.game_height = game_height
        # store the base (scaled) image and position so we can toggle hover without compounding
        self.base_image = pygame.transform.scale(surface, scale)
        self.image = self.base_image

        if self.name != "startscreen":
            self.rect = self.image.get_rect(center = pos)
        else:
            self.rect = self.image.get_rect(topleft = pos)
        
        # Use Vector2 for position so we can animate/move smoothly
        self.pos = pygame.math.Vector2(pos)
        # target position (used for animated moves, e.g., ui_bg moving into view)
        self.target_pos = None
        # speed factor used when animating toward target_pos
        self.move_speed = 6.0
        self.base_size = self.base_image.get_size()
        self.hovered = False

        try:
            self.hover_sfx = pygame.mixer.Sound(join('assets', 'audio', 'sfx', 'mouse-hover.wav'))
        except Exception:
            self.hover_sfx = None
        
    def onMouseOver(self, mouse_pos=None):
        # mouse_pos should be in game-surface coordinates. If not provided, use screen coords.
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        if self.name != "cloud" and self.name != "startscreen":
            if self.rect.collidepoint(mouse_pos):
                if not self.hovered:
                    self.hovered = True
                    scale_factor = 1.1
                    new_size = (int(self.base_size[0] * scale_factor), int(self.base_size[1] * scale_factor))
                    self.image = pygame.transform.smoothscale(self.base_image, new_size)
                    # keep the position consistent (center for buttons)
                    self.rect = self.image.get_rect(center=self.pos)
                    if self.hover_sfx:
                        try:
                            self.hover_sfx.play()
                        except Exception:
                            pass
            else:
                if self.hovered:
                    self.hovered = False
                    self.image = self.base_image
                    self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        if self.name == "cloud":
            self.rect.x += randint(75, 200) * dt
            if self.rect.left > 1280:  # If cloud moves off screen, reset to left
                self.rect.right = 0

    def move_to(self):
        # Animate to visible positions for specific UI elements
        if self.name == "ui_bg":
            # Move to center of the screen
            self.target_pos = pygame.math.Vector2(self.game_width // 2, self.game_height // 2)
        elif self.name == "ui_back_btn":
            self.target_pos = pygame.math.Vector2(150, 100)
        elif self.name == "ui_play_btn":
            self.target_pos = pygame.math.Vector2(self.game_width // 2, self.game_height - 100)
        elif self.name == "map_1":
            self.target_pos = pygame.math.Vector2(self.game_width // 2 - 200, 300)
        else:
            self.target_pos = None

    def move_away(self):
        # Animate back to off-screen positions
        if self.name == "ui_bg":
            self.target_pos = pygame.math.Vector2(self.game_width // 2, -self.game_height // 2 -50)
        elif self.name == "ui_back_btn":
            self.target_pos = pygame.math.Vector2(60, -self.game_height + 60)
        elif self.name == "ui_play_btn":
            self.target_pos = pygame.math.Vector2(self.game_width // 2, -self.game_height - 200)
        elif self.name == "map_1":
            self.target_pos = pygame.math.Vector2(self.game_width // 2 - 150, -self.game_height + 150)
        else:
            self.target_pos = None

    def update(self, dt):
        self.onMouseOver()

        if self.target_pos is not None:
            to_target = self.target_pos - self.pos
            if to_target.length() <= 0.5:
                self.pos = self.target_pos
                self.target_pos = None
            else:
                step = to_target * min(1.0, self.move_speed * dt)
                self.pos += step
            if self.name in ("ui_bg", "ui_back_btn", "ui_play_btn"):
                self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))
            elif self.name == "startscreen":
                self.rect = self.image.get_rect(topleft=(round(self.pos.x), round(self.pos.y)))
            else:
                self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        self.move(dt)