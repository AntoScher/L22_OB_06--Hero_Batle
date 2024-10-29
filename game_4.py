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
    def __init__(self, name, image_path, x, y):
        self.name = name
        self.health = 100
        self.attack_power = 20
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5.0

    def attack(self, other):
        other.health = max(0, other.health - self.attack_power)

    def is_alive(self):
        return self.health > 0

# Класс Игры
class Game:
    def __init__(self, player_name):
        self.screen_width = 800
        self.screen_height = 600
        self.min_distance = self.screen_width // 2
        self.is_running = True
        self.turn = "monster"

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Битва героев")

        self.player_name = player_name

    def random_positions(self):
        while True:
            player_x, player_y = random.randint(50, self.screen_width - 50), random.randint(50, self.screen_height - 50)
            monster_x, monster_y = random.randint(50, self.screen_width - 50), random.randint(50, self.screen_height - 50)
            distance = ((player_x - monster_x) ** 2 + (player_y - monster_y) ** 2) ** 0.5
            if distance >= self.min_distance:
                return (player_x, player_y), (monster_x, monster_y)

    def initialize_heroes(self):
        player_pos, monster_pos = self.random_positions()
        self.player = Hero(self.player_name, 'hero.png', *player_pos)
        self.monster = Hero("Monster", 'monster.png', *monster_pos)

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
        self.initialize_heroes()
        self.choose_weapon()
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        start_time = time.time()

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.player.rect.x = mouse_x
            self.player.rect.y = mouse_y

            current_time = time.time()
            elapsed_time = current_time - start_time

            if not self.player.is_alive() or not self.monster.is_alive():
                self.is_running = False

            if self.turn == "monster" and elapsed_time > 10:
                self.turn = "player"
                start_time = time.time()
                self.initialize_heroes()  # Перезапуск раунда с новыми позициями
            elif self.turn == "player" and elapsed_time > 10:
                self.turn = "monster"
                start_time = time.time()
                self.initialize_heroes()  # Перезапуск раунда с новыми позициями

            if self.turn == "monster":
                direction = pygame.math.Vector2(self.player.rect.x - self.monster.rect.x, self.player.rect.y - self.monster.rect.y)
                if direction.length() > 0:
                    direction = direction.normalize()
                self.monster.rect.x += direction.x * self.monster.speed
                self.monster.rect.y += direction.y * self.monster.speed

                # Монстр атакует героя
                if self.monster.rect.colliderect(self.player.rect):
                    self.monster.attack(self.player)
                    print(f"{self.monster.name} атаковал {self.player.name}. У {self.player.name} осталось {self.player.health} здоровья.")
                    start_time = time.time()  # Перезапуск таймера после атаки

            # Защита от выхода за границы экрана для монстра
            self.monster.rect.x = max(0, min(self.monster.rect.x, self.screen_width - self.monster.rect.width))
            self.monster.rect.y = max(0, min(self.monster.rect.y, self.screen_height - self.monster.rect.height))

            if self.turn == "player" and keys[pygame.K_SPACE] and self.player.rect.colliderect(self.monster.rect):
                self.player.attack(self.monster)
                print(f"{self.player.name} атаковал {self.monster.name}. У {self.monster.name} осталось {self.monster.health} здоровья.")
                if not self.monster.is_alive():
                    self.is_running = False
                start_time = time.time()  # Перезапуск таймера после атаки

            # Обновление экрана и отображение текущего здоровья
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.monster.image, self.monster.rect)

            player_text = font.render(f"{self.player.name}: {self.player.health} HP", True, (255, 255, 255))
            monster_text = font.render(f"{self.monster.name}: {self.monster.health} HP", True, (255, 255, 255))
            self.screen.blit(player_text, (50, 50))
            self.screen.blit(monster_text, (50, 100))

            pygame.display.flip()
            clock.tick(60)

        winner = self.player.name if self.player.is_alive() else self.monster.name
        winner_type = "игрок" if self.player.is_alive() else "компьютер"
        print(f"{winner} ({winner_type}) победил!")

        pygame.quit()

game = Game("Player")
game.start()
