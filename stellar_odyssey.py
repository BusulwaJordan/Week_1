import pygame
import math
import random
from typing import List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import asyncio
import platform
import logging
import os
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    VICTORY = 5
    SETTINGS = 6
    LEVEL_SELECT = 7
    SHIP_CUSTOMIZE = 8
    ACHIEVEMENTS = 9
    HOW_TO_PLAY = 10

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Particle:
    def __init__(self, pos: Vector2, velocity: Vector2, color: tuple, life: float, size: float = 2):
        self.pos = pos
        self.velocity = velocity
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
    
    def update(self, dt: float):
        self.pos += self.velocity * dt
        self.life -= dt
        alpha_factor = max(0, self.life / self.max_life)
        self.color = (*self.color[:3], int(255 * alpha_factor))
    
    def draw(self, screen: pygame.Surface):
        if self.life > 0:
            alpha_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surface, self.color, (self.size, self.size), self.size)
            screen.blit(alpha_surface, (self.pos.x - self.size, self.pos.y - self.size))

class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_explosion(self, pos: Vector2, color: tuple, count: int = 20):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            life = random.uniform(0.5, 1.5)
            size = random.uniform(2, 5)
            self.particles.append(Particle(pos, velocity, color, life, size))
    
    def add_thrust(self, pos: Vector2, direction: Vector2, color: tuple):
        for _ in range(3):
            spread = 0.5
            angle = math.atan2(direction.y, direction.x) + random.uniform(-spread, spread)
            speed = random.uniform(30, 80)
            velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            life = random.uniform(0.2, 0.5)
            size = random.uniform(1, 3)
            self.particles.append(Particle(pos, velocity, color, life, size))
    
    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update(dt)
    
    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            particle.draw(screen)

class Weapon:
    def __init__(self, damage: float, fire_rate: float, bullet_speed: float, color: tuple = WHITE, level: int = 1):
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.color = color
        self.level = level
        self.last_shot = 0
    
    def can_fire(self, current_time: float) -> bool:
        return current_time - self.last_shot >= 1.0 / self.fire_rate
    
    def fire(self, current_time: float):
        self.last_shot = current_time
    
    def upgrade(self):
        self.level = min(self.level + 1, 3)
        self.damage += 10
        self.fire_rate += 2
        self.bullet_speed += 100
        self.color = [WHITE, YELLOW, ORANGE][self.level - 1]

class Bullet:
    def __init__(self, pos: Vector2, velocity: Vector2, damage: float, color: tuple = WHITE, owner: str = "player"):
        self.pos = pos
        self.velocity = velocity
        self.damage = damage
        self.color = color
        self.owner = owner
        self.life = 7.0
    
    def update(self, dt: float):
        self.pos += self.velocity * dt
        self.life -= dt
        logger.debug(f"Bullet update: owner={self.owner}, pos=({self.pos.x:.1f}, {self.pos.y:.1f}), life={self.life:.2f}")
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 3)
    
    def is_alive(self) -> bool:
        margin = 50
        return (self.life > 0 and 
                -margin <= self.pos.x <= SCREEN_WIDTH + margin and 
                -margin <= self.pos.y <= SCREEN_HEIGHT + margin)

class PowerUp:
    def __init__(self, pos: Vector2, power_type: str, color: tuple, value: float):
        self.pos = pos
        self.type = power_type
        self.color = color
        self.value = value
        self.life = 10.0
        self.pulse_time = 0
    
    def update(self, dt: float):
        self.life -= dt
        self.pulse_time += dt * 5
    
    def draw(self, screen: pygame.Surface):
        pulse = abs(math.sin(self.pulse_time)) * 0.3 + 0.7
        size = int(15 * pulse)
        bright_color = tuple(min(255, int(c * pulse)) for c in self.color)
        pygame.draw.circle(screen, bright_color, (int(self.pos.x), int(self.pos.y)), size)
        font = pygame.font.Font(None, 24)
        text = font.render(self.type[0].upper(), True, WHITE)
        text_rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text, text_rect)
    
    def is_alive(self) -> bool:
        return self.life > 0

class Fruit:
    def __init__(self, pos: Vector2, fruit_type: str, color: tuple):
        self.pos = pos
        self.type = fruit_type
        self.color = color
        self.life = 10.0
        self.pulse_time = 0
        self.velocity = Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
    
    def update(self, dt: float):
        self.pos += self.velocity * dt
        self.life -= dt
        self.pulse_time += dt * 5
        margin = 50
        if self.pos.x < -margin:
            self.pos.x += SCREEN_WIDTH + 2 * margin
        elif self.pos.x > SCREEN_WIDTH + margin:
            self.pos.x -= SCREEN_WIDTH + 2 * margin
        if self.pos.y < -margin:
            self.pos.y += SCREEN_HEIGHT + 2 * margin
        elif self.pos.y > SCREEN_HEIGHT + margin:
            self.pos.y -= SCREEN_HEIGHT + 2 * margin
    
    def draw(self, screen: pygame.Surface):
        pulse = abs(math.sin(self.pulse_time)) * 0.3 + 0.7
        size = int(12 * pulse)
        bright_color = tuple(min(255, int(c * pulse)) for c in self.color)
        pygame.draw.circle(screen, bright_color, (int(self.pos.x), int(self.pos.y)), size)
        font = pygame.font.Font(None, 20)
        text = font.render(self.type[0].upper(), True, WHITE)
        text_rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text, text_rect)
    
    def is_alive(self) -> bool:
        return self.life > 0

class Ship:
    def __init__(self, pos: Vector2, color: tuple = WHITE, max_health: float = 100, size: float = 15):
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.angle = 0
        self.color = color
        self.max_health = max_health
        self.health = max_health
        self.size = size
        self.thrust = 300
        self.max_speed = 200
        self.rotation_speed = 4
        self.weapon = Weapon(20, 5, 400)
        self.shield = 0
        self.max_shield = 50
        self.shield_level = 1
        self.thruster_level = 1
        self.abilities = {
            "emp": {"cooldown": 15.0, "last_used": 0.0, "duration": 3.0, "active": False},
            "cloak": {"cooldown": 20.0, "last_used": 0.0, "duration": 5.0, "active": False},
            "overdrive": {"cooldown": 10.0, "last_used": 0.0, "duration": 5.0, "active": False}
        }
    
    def get_forward_vector(self) -> Vector2:
        return Vector2(math.cos(self.angle), math.sin(self.angle))
    
    def update(self, dt: float):
        friction = 0.98
        self.velocity = self.velocity * friction
        if self.abilities["overdrive"]["active"]:
            self.max_speed = 300
            self.thrust = 450
        else:
            self.max_speed = 200 + (self.thruster_level - 1) * 50
            self.thrust = 300 + (self.thruster_level - 1) * 75
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        self.pos += self.velocity * dt
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        elif self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
        elif self.pos.y > SCREEN_HEIGHT:
            self.pos.y = 0
        if self.shield < self.max_shield:
            self.shield += 10 * dt * self.shield_level
            self.shield = min(self.shield, self.max_shield)
        for ability in self.abilities.values():
            if ability["active"] and pygame.time.get_ticks() / 1000.0 - ability["last_used"] > ability["duration"]:
                ability["active"] = False
    
    def thrust_forward(self, dt: float):
        forward = self.get_forward_vector()
        self.velocity += forward * self.thrust * dt
    
    def rotate(self, direction: int, dt: float):
        self.angle += direction * self.rotation_speed * dt
    
    def fire(self, bullets: List[Bullet], current_time: float) -> bool:
        if self.weapon.can_fire(current_time):
            forward = self.get_forward_vector()
            bullet_pos = self.pos + forward * self.size
            bullet_velocity = forward * self.weapon.bullet_speed + self.velocity
            bullet = Bullet(bullet_pos, bullet_velocity, self.weapon.damage, 
                           self.weapon.color, "player")
            bullets.append(bullet)
            self.weapon.fire(current_time)
            logger.debug(f"Fired bullet: owner={bullet.owner}, pos=({bullet_pos.x:.1f}, {bullet_pos.y:.1f}), damage={self.weapon.damage}")
            return True
        return False
    
    def activate_ability(self, ability: str, current_time: float, enemies: List, particles: ParticleSystem) -> bool:
        if current_time - self.abilities[ability]["last_used"] >= self.abilities[ability]["cooldown"]:
            self.abilities[ability]["last_used"] = current_time
            self.abilities[ability]["active"] = True
            if ability == "emp":
                for enemy in enemies:
                    enemy.ai_timer = 0
                    enemy.velocity = Vector2(0, 0)
                    particles.add_explosion(enemy.pos, CYAN, 10)
            elif ability == "cloak":
                particles.add_explosion(self.pos, WHITE, 10)
            elif ability == "overdrive":
                particles.add_explosion(self.pos, ORANGE, 15)
            return True
        return False
    
    def take_damage(self, damage: float) -> bool:
        if self.abilities["cloak"]["active"]:
            return False
        if self.shield > 0:
            shield_absorbed = min(self.shield, damage)
            self.shield -= shield_absorbed
            damage -= shield_absorbed
        self.health -= damage
        logger.debug(f"Player took {damage} damage, health={self.health:.1f}, shield={self.shield:.1f}")
        return self.health <= 0
    
    def draw(self, screen: pygame.Surface):
        if self.abilities["cloak"]["active"]:
            alpha = 50
        else:
            alpha = 255
        forward = self.get_forward_vector()
        right = Vector2(-forward.y, forward.x)
        points = [
            self.pos + forward * self.size,
            self.pos - forward * self.size * 0.5 + right * self.size * 0.5,
            self.pos - forward * self.size * 0.3,
            self.pos - forward * self.size * 0.5 - right * self.size * 0.5
        ]
        point_tuples = [(p.x, p.y) for p in points]
        if len(point_tuples) >= 3:
            alpha_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            try:
                pygame.draw.polygon(alpha_surface, (*self.color[:3], alpha), 
                                   [(p[0] - self.pos.x + self.size * 1.5, p[1] - self.pos.y + self.size * 1.5) 
                                    for p in point_tuples])
                screen.blit(alpha_surface, (self.pos.x - self.size * 1.5, self.pos.y - self.size * 1.5))
            except Exception as e:
                logger.error(f"Failed to draw ship polygon: {e}, points={point_tuples}")
        else:
            logger.warning(f"Invalid ship points: {point_tuples}")
        if self.shield > 0:
            shield_alpha = int(128 * (self.shield / self.max_shield))
            shield_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (*CYAN, shield_alpha), 
                              (self.size * 2, self.size * 2), self.size + 10)
            screen.blit(shield_surface, (self.pos.x - self.size * 2, self.pos.y - self.size * 2))

class Enemy:
    def __init__(self, pos: Vector2, enemy_type: str = "basic"):
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.angle = 0
        self.type = enemy_type
        self.ai_timer = 0
        self.target_angle = 0
        self.is_boss = enemy_type.startswith("boss_")
        if enemy_type == "basic":
            self.color = RED
            self.max_health = 30
            self.size = 12
            self.speed = 80
            self.weapon = Weapon(12, 1.5, 280, RED)
            self.score_value = 100
            self.credit_value = 50
        elif enemy_type == "fast":
            self.color = ORANGE
            self.max_health = 20
            self.size = 10
            self.speed = 140
            self.weapon = Weapon(8, 2.5, 320, ORANGE)
            self.score_value = 150
            self.credit_value = 75
        elif enemy_type == "tank":
            self.color = PURPLE
            self.max_health = 80
            self.size = 18
            self.speed = 50
            self.weapon = Weapon(20, 0.8, 220, PURPLE)
            self.score_value = 300
            self.credit_value = 150
        elif enemy_type == "boss_1":
            self.color = YELLOW
            self.max_health = 500
            self.size = 30
            self.speed = 60
            self.weapon = Weapon(30, 2.0, 300, YELLOW, level=3)
            self.score_value = 1000
            self.credit_value = 500
        elif enemy_type == "boss_2":
            self.color = RED
            self.max_health = 1000
            self.size = 40
            self.speed = 50
            self.weapon = Weapon(40, 3.0, 350, RED, level=3)
            self.score_value = 2000
            self.credit_value = 1000
        self.health = self.max_health
    
    def update(self, dt: float, player_pos: Vector2, bullets: List[Bullet], current_time: float, player_cloaked: bool):
        self.ai_timer += dt
        to_player = player_pos - self.pos
        distance = to_player.magnitude()
        if distance > 0:
            if self.is_boss:
                self.angle += 0.5 * dt
                direction = to_player.normalize()
                if distance > 400:
                    self.velocity = direction * self.speed * 0.8
                elif distance > 200:
                    perpendicular = Vector2(-to_player.y, to_player.x).normalize()
                    self.velocity = (direction * 0.5 + perpendicular * 0.5).normalize() * self.speed
                else:
                    self.velocity = direction * -self.speed * 0.6
                if self.ai_timer > 2.0 and not player_cloaked and self.weapon.can_fire(current_time):
                    for angle_offset in [-0.3, 0, 0.3]:
                        forward = Vector2(math.cos(self.angle + angle_offset), math.sin(self.angle + angle_offset))
                        bullet_pos = self.pos + forward * self.size
                        bullet_velocity = forward * self.weapon.bullet_speed
                        bullets.append(Bullet(bullet_pos, bullet_velocity, self.weapon.damage, 
                                            self.weapon.color, "enemy"))
                    self.weapon.fire(current_time)
            else:
                if distance > 350:
                    direction = to_player.normalize()
                    self.velocity = direction * self.speed * 0.7
                elif distance > 150:
                    direction = to_player.normalize()
                    perpendicular = Vector2(-to_player.y, to_player.x).normalize()
                    move_dir = (direction * 0.6 + perpendicular * 0.4).normalize()
                    self.velocity = move_dir * self.speed * 0.6
                else:
                    direction = to_player.normalize()
                    self.velocity = direction * -self.speed * 0.5
                if self.ai_timer > 0.5 and not player_cloaked:
                    self.angle = math.atan2(to_player.y, to_player.x)
                fire_chance = 0.7 if self.type == "tank" else (0.5 if self.type == "basic" else 0.6)
                if (distance < 400 and distance > 100 and
                    self.weapon.can_fire(current_time) and 
                    random.random() < fire_chance and
                    self.ai_timer > 1.0 and not player_cloaked):
                    accuracy_spread = 0.3 if self.type == "tank" else (0.5 if self.type == "basic" else 0.4)
                    aim_error = random.uniform(-accuracy_spread, accuracy_spread)
                    actual_angle = self.angle + aim_error
                    forward = Vector2(math.cos(actual_angle), math.sin(actual_angle))
                    bullet_pos = self.pos + forward * self.size
                    bullet_velocity = forward * self.weapon.bullet_speed
                    bullets.append(Bullet(bullet_pos, bullet_velocity, self.weapon.damage, 
                                        self.weapon.color, "enemy"))
                    self.weapon.fire(current_time)
        self.pos += self.velocity * dt
        margin = 100
        if self.pos.x < -margin:
            self.pos.x = SCREEN_WIDTH + margin
        elif self.pos.x > SCREEN_WIDTH + margin:
            self.pos.x = -margin
        if self.pos.y < -margin:
            self.pos.y = SCREEN_HEIGHT + margin
        elif self.pos.y > SCREEN_HEIGHT + margin:
            self.pos.y = -margin
    
    def take_damage(self, damage: float) -> bool:
        if damage > 0:
            self.health = max(0, self.health - damage)
            logger.debug(f"Enemy ({self.type}) at ({self.pos.x:.1f}, {self.pos.y:.1f}) took {damage} damage, health now {self.health:.1f}/{self.max_health}")
        else:
            logger.warning(f"Invalid damage value {damage} applied to {self.type} at ({self.pos.x:.1f}, {self.pos.y:.1f})")
        return self.health <= 0
    
    def draw(self, screen: pygame.Surface):
        points = [
            Vector2(self.pos.x, self.pos.y - self.size),
            Vector2(self.pos.x + self.size, self.pos.y),
            Vector2(self.pos.x, self.pos.y + self.size),
            Vector2(self.pos.x - self.size, self.pos.y)
        ]
        if self.is_boss:
            scale = 1.2 + 0.1 * math.sin(pygame.time.get_ticks() / 1000.0 * 2)
            scaled_points = []
            for p in points:
                dx = (p.x - self.pos.x) * scale
                dy = (p.y - self.pos.y) * scale
                scaled_points.append(Vector2(self.pos.x + dx, self.pos.y + dy))
            points = scaled_points
        point_tuples = [(p.x, p.y) for p in points]
        if len(point_tuples) >= 3:
            try:
                pygame.draw.polygon(screen, self.color, point_tuples)
            except Exception as e:
                logger.error(f"Failed to draw enemy polygon (type: {self.type}): {e}, points={point_tuples}")
        else:
            logger.warning(f"Invalid enemy points (type: {self.type}): {point_tuples}")
        bar_width = 30 if not self.is_boss else 60
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, DARK_GRAY, 
                        (self.pos.x - bar_width//2, self.pos.y - self.size - 10, 
                         bar_width, bar_height))
        pygame.draw.rect(screen, GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.25 else RED), 
                        (self.pos.x - bar_width//2, self.pos.y - self.size - 10, 
                         bar_width * health_ratio, bar_height))
        if self.is_boss:
            font = pygame.font.Font(None, 36)
            text = font.render(f"BOSS: {self.type.upper()}", True, WHITE)
            text_rect = text.get_rect(center=(self.pos.x, self.pos.y - self.size - 20))
            screen.blit(text, text_rect)

class Achievement:
    def __init__(self, name: str, description: str, condition: callable, reward: int):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward = reward
        self.unlocked = False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stellar Odyssey - Enhanced")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.score = 0
        self.credits = 0
        self.high_score = 0
        self.max_level_unlocked = 1
        self.level = 1
        self.enemies_killed = 0
        self.wave_timer = 0
        self.wave_active = False
        self.screen_shake = 0
        self.shake_duration = 0
        self.fade_alpha = 0
        self.game_data = {"high_score": 0, "max_level_unlocked": 1, "achievements": {}}
        self.settings = {
            'background': 'nebula_blue',
            'ship_size': 'medium',
            'volume': 50
        }
        self.settings_data = self.settings.copy()
        self.player = Ship(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), CYAN, size=self.get_ship_size())
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []
        self.power_ups: List[PowerUp] = []
        self.fruits: List[Fruit] = []
        self.fruit_targets = {"orange": 0, "apple": 0}
        self.fruits_destroyed = {"orange": 0, "apple": 0}
        self.particles = ParticleSystem()
        self.keys = pygame.key.get_pressed()
        self.last_key_time = 0
        self.key_debounce = 0.2
        self.menu_selected = 0
        self.settings_selected = 0
        self.level_selected = 0
        self.customize_selected = 0
        self.achievements_selected = 0
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.nebula_time = 0
        self.update_background_nebulae()
        self.achievements = [
            Achievement("First Kill", "Destroy your first enemy", lambda g: g.enemies_killed >= 1, 100),
            Achievement("Level 5", "Reach Level 5", lambda g: g.level >= 5, 200),
            Achievement("Boss Slayer", "Defeat a boss", lambda g: any(a.unlocked for a in g.achievements if a.name == "Boss Slayer"), 500),
            Achievement("Collector", "Collect 10 power-ups", lambda g: g.power_ups_collected >= 10, 300),
            Achievement("Fruit Hunter", "Destroy 10 fruits", lambda g: sum(g.fruits_destroyed.values()) >= 10, 200),
            Achievement("Fruit Master", "Complete all fruit targets in a level", lambda g: g.fruit_targets_met(), 400)
        ]
        self.power_ups_collected = 0
        self.load_game_data()
    
    def get_ship_size(self) -> float:
        sizes = {'small': 10, 'medium': 15, 'large': 20}
        return sizes.get(self.settings['ship_size'], 15)
    
    def update_background_nebulae(self):
        self.nebulae = []
        if self.settings['background'] == 'nebula_blue':
            for _ in range(50):
                self.nebulae.append({
                    'pos': Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                    'color': (random.randint(0, 50), random.randint(50, 150), random.randint(150, 255)),
                    'size': random.uniform(20, 50),
                    'speed': random.uniform(-10, 10)
                })
        elif self.settings['background'] == 'nebula_purple':
            for _ in range(50):
                self.nebulae.append({
                    'pos': Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                    'color': (random.randint(100, 200), random.randint(0, 100), random.randint(150, 255)),
                    'size': random.uniform(20, 50),
                    'speed': random.uniform(-10, 10)
                })
        elif self.settings['background'] == 'nebula_red':
            for _ in range(50):
                self.nebulae.append({
                    'pos': Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                    'color': (random.randint(150, 255), random.randint(0, 50), random.randint(0, 50)),
                    'size': random.uniform(20, 50),
                    'speed': random.uniform(-10, 10)
                })
    
    def load_game_data(self) -> None:
        try:
            if platform.system() != "Emscripten" and os.path.exists("high_score.json"):
                with open("high_score.json", "r") as f:
                    self.game_data = json.load(f)
                    self.high_score = self.game_data.get("high_score", 0)
                    self.max_level_unlocked = self.game_data.get("max_level_unlocked", 1)
                    for a in self.achievements:
                        a.unlocked = self.game_data.get("achievements", {}).get(a.name, False)
        except Exception as e:
            logger.error(f"Failed to load game data: {e}")
    
    def save_game_data(self):
        try:
            self.game_data["high_score"] = self.high_score
            self.game_data["max_level_unlocked"] = self.max_level_unlocked
            self.game_data["achievements"] = {a.name: a.unlocked for a in self.achievements}
            if platform.system() != "Emscripten":
                with open("high_score.json", "w") as f:
                    json.dump(self.game_data, f)
        except Exception as e:
            logger.error(f"Failed to save game data: {e}")
    
    def load_settings(self) -> None:
        try:
            if platform.system() != "Emscripten" and os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    self.settings_data = json.load(f)
                    self.settings.update(self.settings_data)
            self.update_background_nebulae()
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
    
    def save_settings(self):
        try:
            self.settings_data = self.settings.copy()
            if platform.system() != "Emscripten":
                with open("settings.json", "w") as f:
                    json.dump(self.settings_data, f)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def reset_game(self, start_level: int = 1):
        self.player = Ship(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), CYAN, size=self.get_ship_size())
        self.enemies.clear()
        self.bullets.clear()
        self.power_ups.clear()
        self.fruits.clear()
        self.fruit_targets = {"orange": 0, "apple": 0}
        self.fruits_destroyed = {"orange": 0, "apple": 0}
        self.particles = ParticleSystem()
        self.score = 0
        self.credits = 0
        self.level = start_level
        self.enemies_killed = 0
        self.power_ups_collected = 0
        self.wave_timer = 0
        self.wave_active = False
        self.screen_shake = 0
        self.fade_alpha = 0
        self.set_fruit_targets()
    
    def set_fruit_targets(self):
        base_targets = {
            1: {"orange": 5, "apple": 3},
            2: {"orange": 7, "apple": 5},
            3: {"orange": 8, "apple": 6},
            4: {"orange": 10, "apple": 8},
            5: {"orange": 12, "apple": 10},
            6: {"orange": 15, "apple": 12},
            7: {"orange": 18, "apple": 14},
            8: {"orange": 20, "apple": 16},
            9: {"orange": 22, "apple": 18},
            10: {"orange": 25, "apple": 20}
        }
        self.fruit_targets = base_targets.get(self.level, {"orange": 10, "apple": 10})
    
    def fruit_targets_met(self) -> bool:
        return (self.fruits_destroyed["orange"] >= self.fruit_targets["orange"] and 
                self.fruits_destroyed["apple"] >= self.fruit_targets["apple"])
    
    def spawn_enemy_wave(self):
        self.fruits.clear()
        self.fruits_destroyed = {"orange": 0, "apple": 0}
        self.set_fruit_targets()
        if self.level in [5, 10]:
            pos = Vector2(SCREEN_WIDTH // 2, -80)
            boss_type = "boss_1" if self.level == 5 else "boss_2"
            self.enemies.append(Enemy(pos, boss_type))
        else:
            base_enemies = 2 + (self.level - 1) // 2
            enemy_count = min(base_enemies, 8)
            for _ in range(enemy_count):
                edge = random.randint(0, 3)
                if edge == 0:
                    pos = Vector2(random.randint(0, SCREEN_WIDTH), -80)
                elif edge == 1:
                    pos = Vector2(SCREEN_WIDTH + 80, random.randint(0, SCREEN_HEIGHT))
                elif edge == 2:
                    pos = Vector2(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 80)
                else:
                    pos = Vector2(-80, random.randint(0, SCREEN_HEIGHT))
                rand = random.random()
                if self.level >= 4 and rand < 0.2:
                    enemy_type = "tank"
                elif self.level >= 3 and rand < 0.4:
                    enemy_type = "fast"
                else:
                    enemy_type = "basic"
                self.enemies.append(Enemy(pos, enemy_type))
        fruit_count = self.fruit_targets["orange"] + self.fruit_targets["apple"]
        for _ in range(fruit_count):
            pos = Vector2(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100))
            fruit_type = "orange" if random.random() < self.fruit_targets["orange"] / (self.fruit_targets["orange"] + self.fruit_targets["apple"]) else "apple"
            color = ORANGE if fruit_type == "orange" else RED
            self.fruits.append(Fruit(pos, fruit_type, color))
        self.wave_active = True
    
    def spawn_power_up(self, pos: Vector2):
        if random.random() < 0.5:
            power_types = [
                ("health", GREEN, 30),
                ("shield", CYAN, 35),
                ("weapon", YELLOW, 0),
                ("speed", BLUE, 0),
                ("credits", ORANGE, 100)
            ]
            power_type, color, value = random.choice(power_types)
            self.power_ups.append(PowerUp(pos, power_type, color, value))
    
    def handle_collisions(self):
        current_time = pygame.time.get_ticks() / 1000.0
        logger.debug(f"Checking collisions: {len(self.bullets)} bullets, {len(self.enemies)} enemies, {len(self.fruits)} fruits")
        for bullet in self.bullets[:]:
            if bullet.owner == "player":
                for enemy in self.enemies[:]:
                    distance = bullet.pos.distance_to(enemy.pos)
                    hit_radius = enemy.size + 12
                    bullet_rect = pygame.Rect(bullet.pos.x - 3, bullet.pos.y - 3, 6, 6)
                    enemy_rect = pygame.Rect(enemy.pos.x - enemy.size, enemy.pos.y - enemy.size, 
                                            enemy.size * 2, enemy.size * 2)
                    if distance < hit_radius or bullet_rect.colliderect(enemy_rect):
                        logger.debug(f"Collision detected: bullet (owner={bullet.owner}, pos=({bullet.pos.x:.1f}, {bullet.pos.y:.1f}), damage={bullet.damage}) "
                                    f"hit {enemy.type} at ({enemy.pos.x:.1f}, {enemy.pos.y:.1f}), distance={distance:.2f}, hit_radius={hit_radius}, "
                                    f"bullet_rect={bullet_rect}, enemy_rect={enemy_rect}")
                        self.particles.add_explosion(enemy.pos, enemy.color, 10)
                        if enemy.take_damage(bullet.damage):
                            logger.debug(f"Enemy {enemy.type} destroyed at ({enemy.pos.x:.1f}, {enemy.pos.y:.1f})")
                            self.particles.add_explosion(enemy.pos, enemy.color, 20)
                            self.score += enemy.score_value
                            self.credits += enemy.credit_value
                            self.enemies_killed += 1
                            if enemy.is_boss:
                                self.achievements[2].unlocked = True
                                self.credits += self.achievements[2].reward
                            self.spawn_power_up(enemy.pos)
                            self.enemies.remove(enemy)
                            self.screen_shake = 0.3
                        else:
                            logger.debug(f"Enemy {enemy.type} survived, health now {enemy.health:.1f}/{enemy.max_health}")
                        self.bullets.remove(bullet)
                        break
                for fruit in self.fruits[:]:
                    distance = bullet.pos.distance_to(fruit.pos)
                    hit_radius = 12
                    bullet_rect = pygame.Rect(bullet.pos.x - 3, bullet.pos.y - 3, 6, 6)
                    fruit_rect = pygame.Rect(fruit.pos.x - 10, fruit.pos.y - 10, 20, 20)
                    if distance < hit_radius or bullet_rect.colliderect(fruit_rect):
                        self.particles.add_explosion(fruit.pos, fruit.color, 10)
                        self.fruits_destroyed[fruit.type] += 1
                        self.score += 50
                        self.credits += 25
                        self.fruits.remove(fruit)
                        self.bullets.remove(bullet)
                        if sum(self.fruits_destroyed.values()) >= 10:
                            self.achievements[4].unlocked = True
                            self.credits += self.achievements[4].reward
                        if self.fruit_targets_met():
                            self.achievements[5].unlocked = True
                            self.credits += self.achievements[5].reward
                        break
            elif bullet.owner == "enemy":
                distance = bullet.pos.distance_to(self.player.pos)
                hit_radius = self.player.size + 12
                bullet_rect = pygame.Rect(bullet.pos.x - 3, bullet.pos.y - 3, 6, 6)
                player_rect = pygame.Rect(self.player.pos.x - self.player.size, self.player.pos.y - self.player.size, 
                                         self.player.size * 2, self.player.size * 2)
                if distance < hit_radius or bullet_rect.colliderect(player_rect):
                    logger.debug(f"Enemy bullet hit player at ({self.player.pos.x:.1f}, {self.player.pos.y:.1f}), distance={distance:.2f}, damage={bullet.damage}")
                    self.particles.add_explosion(self.player.pos, self.player.color, 5)
                    if self.player.take_damage(bullet.damage):
                        self.state = GameState.GAME_OVER
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_game_data()
                    else:
                        self.screen_shake = 0.2
                        self.fade_alpha = 150
                    self.bullets.remove(bullet)
        for power_up in self.power_ups[:]:
            if power_up.pos.distance_to(self.player.pos) < 20:
                if power_up.type == "health":
                    self.player.health = min(self.player.max_health, 
                                           self.player.health + power_up.value)
                elif power_up.type == "shield":
                    self.player.shield = min(self.player.max_shield, 
                                           self.player.shield + power_up.value)
                elif power_up.type == "weapon":
                    self.player.weapon.upgrade()
                elif power_up.type == "speed":
                    self.player.thruster_level = min(self.player.thruster_level + 1, 3)
                elif power_up.type == "credits":
                    self.credits += power_up.value
                self.power_ups_collected += 1
                if self.power_ups_collected >= 10:
                    self.achievements[3].unlocked = True
                    self.credits += self.achievements[3].reward
                self.particles.add_explosion(power_up.pos, power_up.color, 8)
                self.power_ups.remove(power_up)
        for enemy in self.enemies[:]:
            if enemy.pos.distance_to(self.player.pos) < enemy.size + self.player.size:
                collision_damage = 15 if enemy.type == "basic" else (10 if enemy.type == "fast" else (25 if enemy.type == "tank" else 50))
                self.particles.add_explosion(self.player.pos, WHITE, 15)
                if self.player.take_damage(collision_damage):
                    self.state = GameState.GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_game_data()
                else:
                    self.screen_shake = 0.3
                    self.fade_alpha = 200
                self.particles.add_explosion(enemy.pos, enemy.color, 15)
                self.enemies.remove(enemy)
    
    def update_game(self, dt: float):
        current_time = pygame.time.get_ticks() / 1000.0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.thrust_forward(dt)
            backward = self.player.get_forward_vector() * -1
            thrust_pos = self.player.pos + backward * self.player.size
            self.particles.add_thrust(thrust_pos, backward, ORANGE)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.rotate(-1, dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.rotate(1, dt)
        if keys[pygame.K_SPACE]:
            if self.player.fire(self.bullets, current_time):
                forward = self.player.get_forward_vector()
                muzzle_pos = self.player.pos + forward * self.player.size
                self.particles.add_explosion(muzzle_pos, WHITE, 3)
        if keys[pygame.K_1]:
            self.player.activate_ability("emp", current_time, self.enemies, self.particles)
        if keys[pygame.K_2]:
            self.player.activate_ability("cloak", current_time, self.enemies, self.particles)
        if keys[pygame.K_3]:
            self.player.activate_ability("overdrive", current_time, self.enemies, self.particles)
        self.player.update(dt)
        for enemy in self.enemies:
            enemy.update(dt, self.player.pos, self.bullets, current_time, self.player.abilities["cloak"]["active"])
        self.bullets = [b for b in self.bullets if b.is_alive()]
        for bullet in self.bullets:
            bullet.update(dt)
        self.power_ups = [p for p in self.power_ups if p.is_alive()]
        for power_up in self.power_ups:
            power_up.update(dt)
        self.fruits = [f for f in self.fruits if f.is_alive()]
        for fruit in self.fruits:
            fruit.update(dt)
        self.particles.update(dt)
        self.nebula_time += dt
        for nebula in self.nebulae:
            nebula['pos'].x += nebula['speed'] * dt
            nebula['pos'].y += nebula['speed'] * dt
            if nebula['pos'].x < -50:
                nebula['pos'].x += SCREEN_WIDTH + 100
            elif nebula['pos'].x > SCREEN_WIDTH + 50:
                nebula['pos'].x -= SCREEN_WIDTH + 100
            if nebula['pos'].y < -50:
                nebula['pos'].y += SCREEN_HEIGHT + 100
            elif nebula['pos'].y > SCREEN_HEIGHT + 50:
                nebula['pos'].y -= SCREEN_HEIGHT + 100
        if self.screen_shake > 0:
            self.screen_shake -= dt
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 200 * dt)
        if not self.wave_active and len(self.enemies) == 0:
            self.wave_timer += dt
            wave_delay = max(2.0, 4.0 - (self.level * 0.2))
            if self.wave_timer > wave_delay:
                self.spawn_enemy_wave()
                self.wave_timer = 0
        if self.wave_active and len(self.enemies) == 0:
            self.wave_active = False
            if self.level < 10:
                self.level += 1
                if self.level > self.max_level_unlocked:
                    self.max_level_unlocked = self.level
                    self.save_game_data()
                if self.level >= 5:
                    self.achievements[1].unlocked = True
                    self.credits += self.achievements[1].reward
            else:
                self.state = GameState.VICTORY
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_game_data()
        if self.enemies_killed >= 1 and not self.achievements[0].unlocked:
            self.achievements[0].unlocked = True
            self.credits += self.achievements[0].reward
    
    def draw_hud(self):
        health_ratio = self.player.health / self.player.max_health
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(self.screen, DARK_GRAY, (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.25 else RED), 
                        (20, 20, bar_width * health_ratio, bar_height))
        health_text = self.font_small.render(f"Health: {int(self.player.health)}/{int(self.player.max_health)}", 
                                           True, WHITE)
        self.screen.blit(health_text, (20, 45))
        if self.player.max_shield > 0:
            shield_ratio = self.player.shield / self.player.max_shield
            pygame.draw.rect(self.screen, DARK_GRAY, (20, 70, bar_width, bar_height))
            pygame.draw.rect(self.screen, CYAN, (20, 70, bar_width * shield_ratio, bar_height))
            shield_text = self.font_small.render(f"Shield: {int(self.player.shield)}/{int(self.player.max_shield)}", 
                                               True, WHITE)
            self.screen.blit(shield_text, (20, 95))
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        credits_text = self.font_small.render(f"Credits: {self.credits}", True, WHITE)
        level_text = self.font_small.render(f"Level: {self.level}", True, WHITE)
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
        self.screen.blit(credits_text, (SCREEN_WIDTH - 200, 50))
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 80))
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, 110))
        enemy_text = self.font_small.render(f"Enemies: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemy_text, (SCREEN_WIDTH - 200, 140))
        fruit_text = self.font_small.render(f"Oranges: {self.fruits_destroyed['orange']}/{self.fruit_targets['orange']}", True, ORANGE)
        self.screen.blit(fruit_text, (SCREEN_WIDTH - 200, 170))
        apple_text = self.font_small.render(f"Apples: {self.fruits_destroyed['apple']}/{self.fruit_targets['apple']}", True, RED)
        self.screen.blit(apple_text, (SCREEN_WIDTH - 200, 200))
        minimap_size = 100
        minimap = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
        pygame.draw.rect(minimap, (50, 50, 50, 100), (0, 0, minimap_size, minimap_size))
        player_pos = (minimap_size // 2, minimap_size // 2)
        pygame.draw.circle(minimap, CYAN, player_pos, 3)
        for enemy in self.enemies:
            rel_pos = self.player.pos - enemy.pos
            map_pos = (player_pos[0] - rel_pos.x / SCREEN_WIDTH * minimap_size,
                      player_pos[1] - rel_pos.y / SCREEN_HEIGHT * minimap_size)
            if 0 <= map_pos[0] < minimap_size and 0 <= map_pos[1] < minimap_size:
                pygame.draw.circle(minimap, enemy.color, (int(map_pos[0]), int(map_pos[1])), 2)
        for power_up in self.power_ups:
            rel_pos = self.player.pos - power_up.pos
            map_pos = (player_pos[0] - rel_pos.x / SCREEN_WIDTH * minimap_size,
                      player_pos[1] - rel_pos.y / SCREEN_HEIGHT * minimap_size)
            if 0 <= map_pos[0] < minimap_size and 0 <= map_pos[1] < minimap_size:
                pygame.draw.circle(minimap, power_up.color, (int(map_pos[0]), int(map_pos[1])), 2)
        for fruit in self.fruits:
            rel_pos = self.player.pos - fruit.pos
            map_pos = (player_pos[0] - rel_pos.x / SCREEN_WIDTH * minimap_size,
                      player_pos[1] - rel_pos.y / SCREEN_HEIGHT * minimap_size)
            if 0 <= map_pos[0] < minimap_size and 0 <= map_pos[1] < minimap_size:
                pygame.draw.circle(minimap, fruit.color, (int(map_pos[0]), int(map_pos[1])), 2)
        self.screen.blit(minimap, (SCREEN_WIDTH - minimap_size - 20, SCREEN_HEIGHT - minimap_size - 20))
        current_time = pygame.time.get_ticks() / 1000.0
        y_offset = 120
        for i, (name, ability) in enumerate(self.player.abilities.items()):
            cooldown_ratio = min(1.0, (current_time - ability["last_used"]) / ability["cooldown"])
            pygame.draw.rect(self.screen, DARK_GRAY, (20, y_offset, 100, 10))
            pygame.draw.rect(self.screen, CYAN if ability["active"] else GREEN, 
                            (20, y_offset, 100 * cooldown_ratio, 10))
            ability_text = self.font_small.render(f"{name.capitalize()} ({['1', '2', '3'][i]})", True, WHITE)
            self.screen.blit(ability_text, (20, y_offset + 15))
            y_offset += 40
        if not self.wave_active and len(self.enemies) == 0:
            wave_delay = max(2.0, 4.0 - (self.level * 0.2))
            countdown = max(0, wave_delay - self.wave_timer)
            if countdown > 0:
                wave_text = self.font_medium.render(f"Next Wave: {countdown:.1f}", True, YELLOW)
                text_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(wave_text, text_rect)
                info_text = self.font_small.render("Take a break! Collect power-ups or shoot fruits!", True, GREEN)
                info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                self.screen.blit(info_text, info_rect)
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("STELLAR ODYSSEY", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        options = ["Start Game", "Level Select", "Customize Ship", "Settings", "Achievements", "How to Play", "Quit"]
        y_offset = SCREEN_HEIGHT // 2 - 50
        for i, option in enumerate(options):
            color = YELLOW if i == self.menu_selected else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50
        if self.high_score > 0:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(high_score_text, high_score_rect)
    
    def draw_settings(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("SETTINGS", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        options = [
            f"Background: {self.settings['background'].replace('_', ' ').capitalize()}",
            f"Ship Size: {self.settings['ship_size'].capitalize()}",
            f"Volume: {self.settings['volume']}%",
            "Back"
        ]
        y_offset = SCREEN_HEIGHT // 2 - 50
        for i, option in enumerate(options):
            color = YELLOW if i == self.settings_selected else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50
        instructions = self.font_small.render("Use LEFT/RIGHT to change, ENTER to select, ESC to return", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_level_select(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("LEVEL SELECT", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        y_offset = SCREEN_HEIGHT // 2 - 50
        for level in range(1, 11):
            if level <= self.max_level_unlocked:
                color = YELLOW if level - 1 == self.level_selected else WHITE
                text = self.font_medium.render(f"Level {level}", True, color)
            else:
                text = self.font_medium.render(f"Level {level} (Locked)", True, GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
        instructions = self.font_small.render("Use UP/DOWN to select, ENTER to start, ESC to return", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_ship_customize(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("CUSTOMIZE SHIP", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        options = [
            f"Weapon: Level {self.player.weapon.level} ({1000 * self.player.weapon.level} credits to upgrade)",
            f"Shield: Level {self.player.shield_level} ({1000 * self.player.shield_level} credits to upgrade)",
            f"Thruster: Level {self.player.thruster_level} ({1000 * self.player.thruster_level} credits to upgrade)",
            f"Ship Color: {self.player.color == CYAN and 'Cyan' or 'Custom'}",
            "Back"
        ]
        y_offset = SCREEN_HEIGHT // 2 - 50
        for i, option in enumerate(options):
            color = YELLOW if i == self.customize_selected else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50
        credits_text = self.font_small.render(f"Credits: {self.credits}", True, WHITE)
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(credits_text, credits_rect)
        instructions = self.font_small.render("Use LEFT/RIGHT to change, ENTER to upgrade, ESC to return", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_achievements(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("ACHIEVEMENTS", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        y_offset = SCREEN_HEIGHT // 2 - 50
        for i, achievement in enumerate(self.achievements):
            color = YELLOW if i == self.achievements_selected else (GREEN if achievement.unlocked else GRAY)
            text = self.font_small.render(f"{achievement.name}: {achievement.description} ({'Unlocked' if achievement.unlocked else f'{achievement.reward} Credits'})", 
                                        True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
        instructions = self.font_small.render("Use UP/DOWN to view, ESC to return", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_how_to_play(self):
        self.screen.fill(BLACK)
        self.draw_background()
        title = self.font_large.render("HOW TO PLAY", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        self.screen.blit(title, title_rect)
        guide_lines = [
            "Objective: Survive waves of enemies, defeat bosses, and reach Level 10!",
            "Complete fruit targets (oranges and apples) each level!",
            "Controls:",
            "- W or UP: Thrust forward",
            "- A or LEFT: Rotate left",
            "- D or RIGHT: Rotate right",
            "- SPACE: Fire weapon",
            "- 1: EMP (stuns enemies, 15s cooldown)",
            "- 2: Cloak (become invisible, 20s cooldown)",
            "- 3: Overdrive (boost speed, 10s cooldown)",
            "- P: Pause game",
            "- ESC: Return to menu",
            "Gameplay:",
            "- Destroy enemies and fruits to earn score and credits.",
            "- Collect power-ups (H, S, W, P, C) for health, shield, weapon, speed, or credits.",
            "- Use the minimap (bottom-right) to track enemies, power-ups, and fruits.",
            "- Survive until Level 5 and 10 to fight bosses!",
            "Tips:",
            "- Upgrade your weapon, shield, and thrusters in Customize Ship.",
            "- Use EMP to disable enemies, Cloak to avoid damage, and Overdrive for speed.",
            "- Collect credits to unlock upgrades and achieve high scores.",
            "- Shoot fruits (O for orange, A for apple) to meet level targets.",
            "Press ESC to return to the menu."
        ]
        y_offset = SCREEN_HEIGHT // 2 - 150
        for line in guide_lines:
            text = self.font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_background(self):
        for nebula in self.nebulae:
            alpha_surface = pygame.Surface((nebula['size'] * 2, nebula['size'] * 2), pygame.SRCALPHA)
            alpha = int(50 + 30 * math.sin(self.nebula_time + nebula['pos'].x / 100))
            pygame.draw.circle(alpha_surface, (*nebula['color'], alpha), 
                              (nebula['size'], nebula['size']), nebula['size'])
            self.screen.blit(alpha_surface, (nebula['pos'].x - nebula['size'], nebula['pos'].y - nebula['size']))
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        self.draw_background()
        game_over = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over, game_over_rect)
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)
        if self.score >= self.high_score:
            new_high_score = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_score_rect = new_high_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(new_high_score, new_high_score_rect)
        else:
            high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, GRAY)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(high_score_text, high_score_rect)
        level_text = self.font_small.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(level_text, level_rect)
        enemies_text = self.font_small.render(f"Enemies Destroyed: {self.enemies_killed}", True, WHITE)
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(enemies_text, enemies_rect)
        fruits_text = self.font_small.render(f"Fruits Destroyed: {self.fruits_destroyed['orange']}/{self.fruit_targets['orange']} Oranges, {self.fruits_destroyed['apple']}/{self.fruit_targets['apple']} Apples", True, WHITE)
        fruits_rect = fruits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(fruits_text, fruits_rect)
        restart_text = self.font_small.render("Press ENTER to Play Again or ESC to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_victory(self):
        self.screen.fill(BLACK)
        self.draw_background()
        victory = self.font_large.render("VICTORY!", True, GREEN)
        victory_rect = victory.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(victory, victory_rect)
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)
        if self.score >= self.high_score:
            new_high_score = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_score_rect = new_high_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(new_high_score, new_high_score_rect)
        completion_text = self.font_small.render("All Levels Completed!", True, WHITE)
        completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(completion_text, completion_rect)
        fruits_text = self.font_small.render(f"Fruits Destroyed: {self.fruits_destroyed['orange']}/{self.fruit_targets['orange']} Oranges, {self.fruits_destroyed['apple']}/{self.fruit_targets['apple']} Apples", True, WHITE)
        fruits_rect = fruits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(fruits_text, fruits_rect)
        restart_text = self.font_small.render("Press ENTER to Play Again or ESC to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_paused(self):
        self.draw_game()
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 128))
        self.screen.blit(pause_surface, (0, 0))
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        continue_text = self.font_small.render("Press P to Continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game(self):
        self.screen.fill(BLACK)
        shake_offset = Vector2(0, 0)
        if self.screen_shake > 0:
            shake_offset = Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
        self.draw_background()
        self.particles.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        for fruit in self.fruits:
            fruit.draw(self.screen)
        self.draw_hud()
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((255, 0, 0, int(self.fade_alpha)))
            self.screen.blit(fade_surface, (0, 0))
    
    def handle_events(self):
        current_time = pygame.time.get_ticks() / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and current_time - self.last_key_time > self.key_debounce:
                self.last_key_time = current_time
                if self.state == GameState.MENU:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % 7
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.menu_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % 7
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.menu_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_selected == 0:
                            self.reset_game()
                            self.state = GameState.PLAYING
                            self.spawn_enemy_wave()
                        elif self.menu_selected == 1:
                            self.state = GameState.LEVEL_SELECT
                        elif self.menu_selected == 2:
                            self.state = GameState.SHIP_CUSTOMIZE
                        elif self.menu_selected == 3:
                            self.state = GameState.SETTINGS
                        elif self.menu_selected == 4:
                            self.state = GameState.ACHIEVEMENTS
                        elif self.menu_selected == 5:
                            self.state = GameState.HOW_TO_PLAY
                        elif self.menu_selected == 6:
                            self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                elif self.state == GameState.SETTINGS:
                    backgrounds = ['nebula_blue', 'nebula_purple', 'nebula_red']
                    ship_sizes = ['small', 'medium', 'large']
                    if event.key == pygame.K_UP:
                        self.settings_selected = (self.settings_selected - 1) % 4
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.settings_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_DOWN:
                        self.settings_selected = (self.settings_selected + 1) % 4
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.settings_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_LEFT and self.settings_selected < 3:
                        if self.settings_selected == 0:
                            idx = backgrounds.index(self.settings['background'])
                            self.settings['background'] = backgrounds[(idx - 1) % len(backgrounds)]
                        elif self.settings_selected == 1:
                            idx = ship_sizes.index(self.settings['ship_size'])
                            self.settings['ship_size'] = ship_sizes[(idx - 1) % len(ship_sizes)]
                            self.player.size = self.get_ship_size()
                        elif self.settings_selected == 2:
                            self.settings['volume'] = max(0, self.settings['volume'] - 10)
                        self.save_settings()
                        self.update_background_nebulae()
                    elif event.key == pygame.K_RIGHT and self.settings_selected < 3:
                        if self.settings_selected == 0:
                            idx = backgrounds.index(self.settings['background'])
                            self.settings['background'] = backgrounds[(idx + 1) % len(backgrounds)]
                        elif self.settings_selected == 1:
                            idx = ship_sizes.index(self.settings['ship_size'])
                            self.settings['ship_size'] = ship_sizes[(idx + 1) % len(ship_sizes)]
                            self.player.size = self.get_ship_size()
                        elif self.settings_selected == 2:
                            self.settings['volume'] = min(100, self.settings['volume'] + 10)
                        self.save_settings()
                        self.update_background_nebulae()
                    elif event.key == pygame.K_RETURN and self.settings_selected == 3:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.LEVEL_SELECT:
                    if event.key == pygame.K_UP:
                        self.level_selected = (self.level_selected - 1) % 10
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.level_selected * 40), WHITE, 5)
                    elif event.key == pygame.K_DOWN:
                        self.level_selected = (self.level_selected + 1) % 10
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.level_selected * 40), WHITE, 5)
                    elif event.key == pygame.K_RETURN and self.level_selected + 1 <= self.max_level_unlocked:
                        self.reset_game(start_level=self.level_selected + 1)
                        self.state = GameState.PLAYING
                        self.spawn_enemy_wave()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.SHIP_CUSTOMIZE:
                    colors = [CYAN, WHITE, YELLOW, GREEN]
                    if event.key == pygame.K_UP:
                        self.customize_selected = (self.customize_selected - 1) % 5
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.customize_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_DOWN:
                        self.customize_selected = (self.customize_selected + 1) % 5
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.customize_selected * 50), WHITE, 5)
                    elif event.key == pygame.K_LEFT and self.customize_selected == 3:
                        current_idx = colors.index(self.player.color) if self.player.color in colors else 0
                        self.player.color = colors[(current_idx - 1) % len(colors)]
                    elif event.key == pygame.K_RIGHT and self.customize_selected == 3:
                        current_idx = colors.index(self.player.color) if self.player.color in colors else 0
                        self.player.color = colors[(current_idx + 1) % len(colors)]
                    elif event.key == pygame.K_RETURN and self.customize_selected < 4:
                        if self.customize_selected == 0 and self.player.weapon.level < 3 and self.credits >= 1000 * self.player.weapon.level:
                            self.credits -= 1000 * self.player.weapon.level
                            self.player.weapon.upgrade()
                            self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), YELLOW, 10)
                        elif self.customize_selected == 1 and self.player.shield_level < 3 and self.credits >= 1000 * self.player.shield_level:
                            self.credits -= 1000 * self.player.shield_level
                            self.player.shield_level += 1
                            self.player.max_shield += 50
                            self.player.shield = self.player.max_shield
                            self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), CYAN, 10)
                        elif self.customize_selected == 2 and self.player.thruster_level < 3 and self.credits >= 1000 * self.player.thruster_level:
                            self.credits -= 1000 * self.player.thruster_level
                            self.player.thruster_level += 1
                            self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), BLUE, 10)
                    elif event.key == pygame.K_RETURN and self.customize_selected == 4:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                        self.spawn_enemy_wave()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.ACHIEVEMENTS:
                    if event.key == pygame.K_UP:
                        self.achievements_selected = (self.achievements_selected - 1) % len(self.achievements)
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.achievements_selected * 40), WHITE, 5)
                    elif event.key == pygame.K_DOWN:
                        self.achievements_selected = (self.achievements_selected + 1) % len(self.achievements)
                        self.particles.add_explosion(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + self.achievements_selected * 40), WHITE, 5)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.HOW_TO_PLAY:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

async def main():
    game = Game()
    while game.running:
        dt = game.clock.tick(FPS) / 1000.0
        game.handle_events()
        if game.state == GameState.PLAYING:
            game.handle_collisions()
            game.update_game(dt)
        game.screen.fill(BLACK)
        if game.state == GameState.MENU:
            game.draw_menu()
        elif game.state == GameState.PLAYING:
            game.draw_game()
        elif game.state == GameState.PAUSED:
            game.draw_paused()
        elif game.state == GameState.GAME_OVER:
            game.draw_game_over()
        elif game.state == GameState.VICTORY:
            game.draw_victory()
        elif game.state == GameState.SETTINGS:
            game.draw_settings()
        elif game.state == GameState.LEVEL_SELECT:
            game.draw_level_select()
        elif game.state == GameState.SHIP_CUSTOMIZE:
            game.draw_ship_customize()
        elif game.state == GameState.ACHIEVEMENTS:
            game.draw_achievements()
        elif game.state == GameState.HOW_TO_PLAY:
            game.draw_how_to_play()
        pygame.display.flip()
        await asyncio.sleep(1.0 / FPS)
    pygame.quit()

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())