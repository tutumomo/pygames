import pygame
from pygame.locals import *
from config import *
import random

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        # Load tank images for different directions
        self.images = {
            'up': pygame.Surface((TILE_SIZE, TILE_SIZE)),
            'down': pygame.Surface((TILE_SIZE, TILE_SIZE)),
            'left': pygame.Surface((TILE_SIZE, TILE_SIZE)),
            'right': pygame.Surface((TILE_SIZE, TILE_SIZE))
        }
        
        # Draw tank for each direction
        for direction, surface in self.images.items():
            surface.fill(BLACK)  # Background
            if direction in ['up', 'down']:
                # Draw tank body
                pygame.draw.rect(surface, GREEN, (4, 2, 24, 28))
                # Draw tank tracks
                pygame.draw.rect(surface, DARK_GREEN, (2, 0, 4, 32))
                pygame.draw.rect(surface, DARK_GREEN, (26, 0, 4, 32))
                # Draw tank cannon
                if direction == 'up':
                    pygame.draw.rect(surface, GREEN, (14, 0, 4, 12))
                else:  # down
                    pygame.draw.rect(surface, GREEN, (14, 20, 4, 12))
            else:  # left or right
                # Draw tank body
                pygame.draw.rect(surface, GREEN, (2, 4, 28, 24))
                # Draw tank tracks
                pygame.draw.rect(surface, DARK_GREEN, (0, 2, 32, 4))
                pygame.draw.rect(surface, DARK_GREEN, (0, 26, 32, 4))
                # Draw tank cannon
                if direction == 'left':
                    pygame.draw.rect(surface, GREEN, (0, 14, 12, 4))
                else:  # right
                    pygame.draw.rect(surface, GREEN, (20, 14, 12, 4))
            
            # Set color key for transparency
            surface.set_colorkey(BLACK)
        
        self.direction = 'up'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.original_x = x
        self.original_y = y
        self.old_x = x
        self.old_y = y
        self.can_shoot = True
        self.shoot_delay = 500  # Milliseconds
        self.last_shot = 0

    def move(self, direction):
        self.direction = direction
        self.image = self.images[self.direction]
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
        elif direction == 'up':
            self.rect.y -= self.speed
        elif direction == 'down':
            self.rect.y += self.speed
            
        # Keep tank within screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def shoot(self, bullets_group):
        current_time = pygame.time.get_ticks()
        if self.can_shoot and current_time - self.last_shot > self.shoot_delay:
            # Calculate bullet starting position based on tank direction
            if self.direction == 'up':
                bullet_x = self.rect.centerx - 2
                bullet_y = self.rect.top
            elif self.direction == 'down':
                bullet_x = self.rect.centerx - 2
                bullet_y = self.rect.bottom
            elif self.direction == 'left':
                bullet_x = self.rect.left
                bullet_y = self.rect.centery - 2
            else:  # right
                bullet_x = self.rect.right
                bullet_y = self.rect.centery - 2
            
            bullet = Bullet(bullet_x, bullet_y, self.direction)
            bullets_group.add(bullet)
            self.last_shot = current_time

    def update(self, walls=None):
        # Check collision with walls if walls group is provided
        if walls:
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                # Revert to previous position if there's a collision
                self.rect.x = self.old_x
                self.rect.y = self.old_y

    def reset_position(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.direction = 'up'

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy(Tank):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        # Change enemy tank color to red
        for direction, surface in self.images.items():
            surface.fill(BLACK)
            if direction in ['up', 'down']:
                pygame.draw.rect(surface, RED, (4, 2, 24, 28))
                pygame.draw.rect(surface, DARK_RED, (2, 0, 4, 32))
                pygame.draw.rect(surface, DARK_RED, (26, 0, 4, 32))
                if direction == 'up':
                    pygame.draw.rect(surface, RED, (14, 0, 4, 12))
                else:
                    pygame.draw.rect(surface, RED, (14, 20, 4, 12))
            else:
                pygame.draw.rect(surface, RED, (2, 4, 28, 24))
                pygame.draw.rect(surface, DARK_RED, (0, 2, 32, 4))
                pygame.draw.rect(surface, DARK_RED, (0, 26, 32, 4))
                if direction == 'left':
                    pygame.draw.rect(surface, RED, (0, 14, 12, 4))
                else:
                    pygame.draw.rect(surface, RED, (20, 14, 12, 4))
            surface.set_colorkey(BLACK)
        
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.image = self.images[self.direction]
        self.move_time = 0
        self.move_delay = 1000  # Time to wait before changing direction
        self.last_shot = 0
        self.shoot_delay = random.randint(1000, 3000)  # Random delay between shots

    def ai_move(self, player):
        current_time = pygame.time.get_ticks()
        
        # Change direction periodically
        if current_time - self.move_time > self.move_delay:
            # Sometimes move towards player
            if random.random() < 0.7:  # 70% chance to move towards player
                # Determine direction to player
                if abs(self.rect.x - player.rect.x) > abs(self.rect.y - player.rect.y):
                    if self.rect.x < player.rect.x:
                        self.direction = 'right'
                    else:
                        self.direction = 'left'
                else:
                    if self.rect.y < player.rect.y:
                        self.direction = 'down'
                    else:
                        self.direction = 'up'
            else:
                # Random direction
                self.direction = random.choice(['up', 'down', 'left', 'right'])
            
            self.move_time = current_time
            self.move_delay = random.randint(500, 2000)  # Random delay before next direction change
        
        # Move in current direction
        self.move(self.direction)
        
        # Shoot periodically
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            self.shoot_delay = random.randint(1000, 3000)
            return True  # Signal to create bullet
        return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, YELLOW, (4, 4), 3)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.speed = BULLET_SPEED

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        # Remove bullet if it goes off screen
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)
        # Draw brick pattern
        for i in range(0, TILE_SIZE, 8):
            for j in range(0, TILE_SIZE, 4):
                if (i + j) % 8 == 0:
                    pygame.draw.rect(self.image, DARK_GRAY, (i, j, 8, 4))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Brick(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((165, 42, 42))  # Brown color for brick


class Steel(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((128, 128, 128))  # Gray color for steel


class Base(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
        self.image.fill(BLUE)  # Temporary color for base
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
