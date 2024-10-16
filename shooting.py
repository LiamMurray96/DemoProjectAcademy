import random
import pygame

pygame.init()

BG_COLOR = pygame.Color('gray12')
PLAYER_IMG = pygame.Surface((30, 50), pygame.SRCALPHA)
pygame.draw.polygon(PLAYER_IMG, pygame.Color('dodgerblue'), [(0, 50), (15, 0), (30, 50)])
ENEMY_IMG = pygame.Surface((50, 30))
ENEMY_IMG.fill(pygame.Color('darkorange1'))
BULLET_IMG = pygame.Surface((9, 15))
BULLET_IMG.fill(pygame.Color('aquamarine2'))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, all_sprites, bullets):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=pos)
        self.all_sprites = all_sprites
        self.add(self.all_sprites)
        self.bullets = bullets
        self.bullet_timer = .1

    def update(self, dt):
        self.rect.center = pygame.mouse.get_pos()

        mouse_pressed = pygame.mouse.get_pressed()
        self.bullet_timer -= dt # Subtract the time since the last tick.
        if self.bullet_timer <= 0:
            self.bullet_timer = 0 # Bullet ready.
            if mouse_pressed[0]: #Left mouse button.
                # Create a new bullet instance and add it to the groups.
                Bullet(pygame.mouse.get_pos(), self.all_sprites, self.bullets)
                self.bullet_timer = .1 # Reset the timer.

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=pos)
        self.health = 30

    def update(self, dt):
        if self.health <= 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, -450)
        self.damage = 10

    def update(self, dt):
        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos # Update the rect pos.
        if self.rect.bottom <= 0:
            self.kill()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player((0, 0), self.all_sprites, self.bullets)

        for i in range(15):
            pos = (random.randrange(30, 750), random.randrange(500))
            Enemy(pos, self.all_sprites, self.enemies)

        self.done = False

    def run(self):
        while not self.done:
            # dt = time since last tick in milliseconds.
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.run_logic(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def run_logic(self, dt):
        self.all_sprites.update(dt)

        # hits is a dict. The enemies are the keys and bullets the values.
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.health -= bullet.damage

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    Game().run()
    pygame.quit()