import pygame
import sys
from pygame.locals import *
from config import *
from sprites import Tank, Bullet, Brick, Steel, Base, Enemy, Wall
from level import Level
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_enemy_spawn = pygame.time.get_ticks()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Create player tank
        self.player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * TILE_SIZE, PLAYER_SPEED)
        self.all_sprites.add(self.player)
        
        # Store enemy spawn points
        self.enemy_spawn_points = []
        
        # Create level
        self.create_level()

    def create_level(self):
        # Load level from LEVEL_MAP
        for y, row in enumerate(LEVEL_MAP):
            for x, cell in enumerate(row):
                if cell == 1:  # Brick wall
                    wall = Wall(x * TILE_SIZE, y * TILE_SIZE)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif cell == 2:  # Steel wall
                    wall = Wall(x * TILE_SIZE, y * TILE_SIZE)
                    wall.image.fill(DARK_GRAY)  # Make steel walls darker
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif cell == 3:  # Enemy spawn point
                    self.enemy_spawn_points.append((x * TILE_SIZE, y * TILE_SIZE))

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > ENEMY_SPAWN_DELAY and len(self.enemies) < ENEMY_COUNT:
            if self.enemy_spawn_points:
                spawn_x, spawn_y = random.choice(self.enemy_spawn_points)
                enemy = Enemy(spawn_x, spawn_y, ENEMY_SPEED)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
                self.last_enemy_spawn = current_time

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Calculate bullet position based on tank direction
                    if self.player.direction == 'up':
                        bullet_x = self.player.rect.centerx
                        bullet_y = self.player.rect.top
                    elif self.player.direction == 'down':
                        bullet_x = self.player.rect.centerx
                        bullet_y = self.player.rect.bottom
                    elif self.player.direction == 'left':
                        bullet_x = self.player.rect.left
                        bullet_y = self.player.rect.centery
                    else:  # right
                        bullet_x = self.player.rect.right
                        bullet_y = self.player.rect.centery
                    
                    bullet = Bullet(bullet_x, bullet_y, self.player.direction)
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

    def update(self):
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')
        if keys[pygame.K_UP]:
            self.player.move('up')
        if keys[pygame.K_DOWN]:
            self.player.move('down')
        
        # Spawn enemies
        self.spawn_enemy()
        
        # Update all sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, (Tank, Enemy)):
                sprite.update(self.walls)
            else:
                sprite.update()
        
        # Update enemy AI and handle enemy shooting
        for enemy in self.enemies:
            if enemy.ai_move(self.player):  # If enemy should shoot
                if enemy.direction == 'up':
                    bullet_x = enemy.rect.centerx
                    bullet_y = enemy.rect.top
                elif enemy.direction == 'down':
                    bullet_x = enemy.rect.centerx
                    bullet_y = enemy.rect.bottom
                elif enemy.direction == 'left':
                    bullet_x = enemy.rect.left
                    bullet_y = enemy.rect.centery
                else:  # right
                    bullet_x = enemy.rect.right
                    bullet_y = enemy.rect.centery
                
                bullet = Bullet(bullet_x, bullet_y, enemy.direction)
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        
        # Check bullet collisions with walls
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.walls, True)
            if hits:
                bullet.kill()
        
        # Check bullet collisions with tanks
        for bullet in self.bullets:
            # Check if bullet hits player
            if pygame.sprite.collide_rect(bullet, self.player):
                bullet.kill()
                # Handle player hit (you can add lives system here)
            
            # Check if bullet hits enemies
            enemy_hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            if enemy_hits:
                bullet.kill()
        
        # Remove bullets that are off screen
        for bullet in self.bullets:
            if (bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT or
                bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH):
                bullet.kill()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

def main():
    game = Game()
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
