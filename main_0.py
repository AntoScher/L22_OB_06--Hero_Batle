import pygame
import random
import time
from abc import ABC, abstractmethod

# Интерфейс для персонажей
class IHero(ABC):
    @abstractmethod
    def attack(self, other):
        pass

    @abstractmethod
    def is_alive(self):
        pass

# Класс Героя
class Hero(IHero):
    def __init__(self, name, image_path):
        self.name = name
        self.health = 100
        self.attack_power = 20
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = 5

    def attack(self, other):
        other.health -= self.attack_power

    def is_alive(self):
        return self.health > 0

# Класс Игры
class Game:
    def __init__(self, player_name):
        self.player = Hero(player_name, 'hero.png')
        self.monster = Hero("Monster", 'monster.png')
        self.is_running = True

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Битва героев")

    def choose_weapon(self):
        print("Выберите оружие: \n1. Меч \n2. Топор")
        choice = input("Введите номер оружия: ")
        if choice == '1':
            self.player.attack_power = 20
            self.monster.attack_power = 25
        elif choice == '2':
            self.player.attack_power = 25
            self.monster.attack_power = 20
        else:
            print("Неверный выбор, используем стандартное оружие.")

        print("Начинаем? (y/n)")
        start = input()
        if start.lower() != 'y':
            self.is_running = False

    def start(self):
        self.choose_weapon()
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rect.x -= self.player.speed
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += self.player.speed
            if keys[pygame.K_UP]:
                self.player.rect.y -= self.player.speed
            if keys[pygame.K_DOWN]:
                self.player.rect.y += self.player.speed

            if not self.player.is_alive() or not self.monster.is_alive():
                self.is_running = False
                break

            if random.randint(0, 100) < 5:  # Случайное движение монстра
                self.monster.rect.x += random.choice([-1, 1]) * self.monster.speed
                self.monster.rect.y += random.choice([-1, 1]) * self.monster.speed

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.monster.image, self.monster.rect)

            player_text = font.render(f"{self.player.name}: {self.player.health} HP", True, (255, 255, 255))
            monster_text = font.render(f"{self.monster.name}: {self.monster.health} HP", True, (255, 255, 255))
            self.screen.blit(player_text, (50, 50))
            self.screen.blit(monster_text, (50, 100))

            pygame.display.flip()
            clock.tick(60)

        if self.player.is_alive():
            print(f"{self.player.name} победил!")
        else:
            print(f"{self.monster.name} победил!")

        pygame.quit()

game = Game("Player")
game.start()
