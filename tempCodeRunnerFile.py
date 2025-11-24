self.game_surface.fill("grey")
            self.all_sprites.set_target_surface(self.game_surface)
            self.all_sprites.draw()
            
            self.castles.draw(self.game_surface)
            for castle in self.castles:
                castle.draw_health(self.game_surface)
            