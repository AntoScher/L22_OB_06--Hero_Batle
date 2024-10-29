
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
            player_x, player_y = random.randint(50, self.screen_width - 50), random.randint(50, self.screen_height -50)
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

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.player.rect.x = mouse_x
            self.player.rect.y = mouse_y

            if self.turn == "player":
                if keys[pygame.K_SPACE]:  # Игрок атакует при нажатии пробела
                    self.player.attack(self.monster)
                    self.turn = "monster"

            if self.turn == "monster":
                if self.monster.is_alive() and self.player.is_alive():
                    self.monster.attack(self.player)
                    self.turn = "player"

            # Отрисовка
            self.screen.fill((255, 255, 255))  # Очистка экрана
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.monster.image, self.monster.rect)

            # Отображение здоровья
            health_text = font.render(f"{self.player.name} HP: {self.player.health}", True, (0, 0, 0))
            self.screen.blit(health_text, (10, 10))
            health_text = font.render(f"{self.monster.name} HP: {self.monster.health}", True, (0, 0, 0))
            self.screen.blit(health_text, (10, 50))

            pygame.display.flip()  # Обновление экрана
            clock.tick(60)  # Ограничение FPS

        pygame.quit()

# Пример запуска игры
if __name__ == "__main__":  
    player_name = input("Введите имя персонажа: ")
    game = Game(player_name)
    game.start()