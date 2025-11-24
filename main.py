from settings import *
from sprites import *
from monsters import Monster
from castle import CastleBox
from user_interface import UserInterface

import pygame

class TowerDefense:
    def __init__(self):
        pygame.init()

        self.GAME_WIDTH  = 1280
        self.GAME_HEIGHT = 704
        self.game_surface = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

        self.screen = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Fortress Frontline")

        self.all_sprites = AllSprite(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.ui_sprites = AllSprite(self.GAME_WIDTH, self.GAME_HEIGHT)

        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.show_start = False
        self.show_map = False

        self.button_sfx = pygame.mixer.Sound(join('assets', 'audio', 'sfx', 'button-click.wav'))
        self.start_bgmusic = pygame.mixer.Sound(join('assets', 'audio', 'bgm', 'start_bgm.wav'))
        self.start_bgmusic.set_volume(0.5)
        self.start_bgmusic.play(loops=-1)

        # load images
        self.startscreen_images = {
            "start": pygame.image.load(join('assets', 'images', 'startscreen', 'Startscreen.png')).convert_alpha(),
            "logo": pygame.image.load(join('assets', 'images', 'startscreen', 'logo.png')).convert_alpha(),
            "play": pygame.image.load(join('assets', 'images', 'startscreen', 'play.png')).convert_alpha(),
            "setting": pygame.image.load(join('assets', 'images', 'startscreen', 'settings.png')).convert_alpha(),
            "exit": pygame.image.load(join('assets', 'images', 'startscreen', 'exit.png')).convert_alpha(),
        }
        self.map_selection_images = {
            "map": pygame.image.load(join('assets', 'images', 'mapscreen', 'map.png')).convert_alpha(),
            "back": pygame.image.load(join('assets', 'images', 'mapscreen', 'back.png')).convert_alpha(),
            "upgrade": pygame.image.load(join('assets', 'images', 'mapscreen', 'upgrade.png')).convert_alpha()
        }
        self.upgrades_images = {}

        #self.start_screen()
        self.setup()

    def start_screen(self):
        self.show_start = True
        if not hasattr(self, "start_screen_bg"):
            self.start_screen_bg = UserInterface("startscreen", (0, 0), self.startscreen_images["start"], (self.GAME_WIDTH, self.GAME_HEIGHT), self.ui_sprites)

        if not hasattr(self, "cloud"):
            for cloud in range(5):
                self.cloud = UserInterface(
                    "cloud",
                    (randint(0 - 100, self.GAME_WIDTH), randint(0, self.GAME_HEIGHT // 2 - 200)),
                    pygame.image.load(join('assets', 'images', 'startscreen', 'clouds', f'cloud{randint(1, 4)}.png')).convert_alpha(),
                    (300, 80),
                    self.ui_sprites
                )

        self.logo = UserInterface("logo", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2 - 250), self.startscreen_images["logo"], (417, 146), self.ui_sprites)
        self.play_button = UserInterface("play", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2 - 100), self.startscreen_images["play"], (150, 65), self.ui_sprites)
        self.settings_button = UserInterface("settings", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2), self.startscreen_images["setting"], (254, 68), self.ui_sprites)
        self.exit_button = UserInterface("exit", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2 + 100), self.startscreen_images["exit"], (139, 58), self.ui_sprites)

    def map_selection(self):
        self.show_map = True

        self.ui_sprites.add(self.logo)
        
        self.map_button = UserInterface("map", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2 - 100), self.map_selection_images["map"], (150, 65), self.ui_sprites)
        self.upgrades_button = UserInterface("upgrades", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2), self.map_selection_images["upgrade"], (265, 68), self.ui_sprites)
        self.back_button = UserInterface("back", (self.GAME_WIDTH // 2 + 360, self.GAME_HEIGHT // 2 + 100), self.map_selection_images["back"], (139, 58), self.ui_sprites)

    def setup(self):
        map = load_pygame(join('assets', 'data', 'tmx', 'finals.tmx'))

        # Ground tiles
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprites((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # Castles
        self.castles = pygame.sprite.Group()
        castle_layer = map.get_layer_by_name("castle")
        for obj in castle_layer:
            if hasattr(obj, "image") and obj.image is not None:
                castle = CastleBox((obj.x, obj.y), obj.width, obj.height, self.all_sprites, image=obj.image)
                self.all_sprites.add(castle)  # Add to all_sprites for correct draw order
                self.castles.add(castle)      # Keep for HP & collision

                if obj.properties.get("hp_castle", False):
                    castle.has_hp = True

        # Houses, Decorations, Fences
        for layer_name in ["House", "decoration", "fences"]:
            for obj in map.get_layer_by_name(layer_name):
                Objects((obj.x, obj.y), obj.image, (obj.width, obj.height), obj.rotation, self.all_sprites)

        # Waypoints
        self.waypoints = [(waypoint.x, waypoint.y) for waypoint in map.get_layer_by_name("Waypoints1")]
        self.waypoints = [(waypoint.x, waypoint.y) for waypoint in map.get_layer_by_name("Waypoints2")]
        
        # Monsters for testing
        self.monsters = pygame.sprite.Group()
        monster_img = pygame.image.load(join('assets', 'images', '0.png'))
        for _ in range(5):
            monster = Monster(self.waypoints, monster_img, randint(1, 5), self.all_sprites)
            self.monsters.add(monster)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            window_w, window_h = self.screen.get_size()
            scale_x = window_w / self.GAME_WIDTH if self.GAME_WIDTH != 0 else 1
            scale_y = window_h / self.GAME_HEIGHT if self.GAME_HEIGHT != 0 else 1
            scaled_w = window_w
            scaled_h = window_h
            
            offset_x = 0
            offset_y = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Fullscreen toggle
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            w, h = self.screen.get_size()
                            self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

                # WINDOW RESIZE
                if event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                # Mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (self.show_start or self.show_map):
                    mx, my = event.pos
                    gx = (mx - offset_x) / scale_x
                    gy = (my - offset_y) / scale_y
                    for ui in list(self.ui_sprites):
                        if ui.rect.collidepoint((gx, gy)):
                            if ui.name != "cloud" and ui.name != "startscreen":
                                try:
                                    self.button_sfx.play()
                                except Exception:
                                    pass
                            if ui.name == "play":
                                self.show_start = False
                                self.ui_sprites.remove(self.play_button, self.settings_button, self.exit_button, self.logo)
                                self.map_selection()
                            if ui.name == "settings":
                                print("Settings button clicked")
                            if ui.name == "exit":
                                self.running = False
                            if ui.name == "map":
                                print("Map button clicked")
                            if ui.name == "upgrades":
                                print("Upgrades button clicked")
                            if ui.name == "back":
                                self.show_map = False
                                self.ui_sprites.remove(self.map_button, self.upgrades_button, self.back_button, self.logo)
                                self.start_screen()

            # Update
            self.all_sprites.update(dt)
            self.ui_sprites.update(dt)
            self.castles.update(dt)

            # Collision
            hits = pygame.sprite.groupcollide(self.castles, self.monsters, False, False)
            for castle, monsters in hits.items():
                for monster in monsters:
                    damage = getattr(monster, "damage", 10)
                    castle.take_damage(damage)
                    monster.kill()  

            # Draw
            self.game_surface.fill("grey")
            self.all_sprites.set_target_surface(self.game_surface)
            self.all_sprites.draw()

            # Draw only HP bars on top
            for castle in self.castles:
                castle.draw_health(self.game_surface)
            
            # Draw UI
            if self.show_start or self.show_map:
                self.ui_sprites.set_target_surface(self.game_surface)
                self.ui_sprites.draw()

            # Scale to window
            scaled_surface = pygame.transform.smoothscale(self.game_surface, (scaled_w, scaled_h))
            self.screen.fill("black")
            self.screen.blit(scaled_surface, (offset_x, offset_y))
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = TowerDefense()
    game.run()
