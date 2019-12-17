import pygame
import sys
import time
import random

image_cache = {}


class Image(pygame.sprite.Sprite):
    def __init__(self, name, size=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if name not in image_cache:
            image_cache[name] = pygame.image.load(name + '.png')
        self.image = image_cache.get(name)
        if size:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def show_position(self, screen, pos=None, size=None):
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)
        if pos is None:
            pos = self.rect
        screen.blit(self.image, pos)


class Burger:
    ingredient_choice = [
        'beef_side', 'bacon_side', 'lettuce_side', 'cheese_side'
    ]

    def __init__(self, count, pos_x, pos_y, ingredient=None):
        if ingredient is None:
            self.ingredient = ['botbun_side']
            random.shuffle(Burger.ingredient_choice)
            self.ingredient += Burger.ingredient_choice[:count - 2]
            self.ingredient.append('topbun_side')
        else:
            self.ingredient = ingredient
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.burger = []
        self.build_burger()

    def equal(self, burger):
        return self.ingredient == burger.ingredient

    def build_burger(self):
        for layer in range(len(self.ingredient)):
            image = Image(self.ingredient[layer], (60, 25))
            image.rect.center = (self.pos_x, self.pos_y - layer * 13)
            self.burger.append(image)

    def update_burger(self, screen, speed=(0, 0)):
        for image in self.burger:
            image.rect = image.rect.move(speed)
            image.show_position(screen)

    def add_ingredient(self, ingredient):
        if len(self.ingredient) < 10:
            self.ingredient.append(ingredient)
        self.burger = []
        self.build_burger()

    def clear(self):
        self.ingredient = []
        self.burger = []
        self.build_burger()


class Customer:
    cust_choice = [
        ('man', (1, 0), 3),
        ('superheroe', (2, 0), 4),
        ('wizard', (3, 0), 5)
    ]

    def __init__(self, custype=None):
        if custype is None:
            custype, self.speed, self.count = random.choice(
                Customer.cust_choice)
        else:
            custype, self.speed, self.count = Customer.cust_choice[custype]

        self.show = True
        self.image = Image(custype, (110, 110))
        self.image.rect.center = (50, 205)
        self.cloud = Image('cloud', (150, 150))
        self.cloud.rect.center = (100, 120)
        self.burger = Burger(self.count, 100, 120)

    def move(self, screen):
        self.image.rect = self.image.rect.move(self.speed)
        self.cloud.rect = self.cloud.rect.move(self.speed)
        if self.image.rect.right > 800:
            self.image.image.fill((0, 0, 0, 0))
            self.show = False
        self.image.show_position(screen)
        self.cloud.show_position(screen)
        self.burger.update_burger(screen, self.speed)


class Player:
    def __init__(self, name, pos_x, cooldown):
        self.name = name
        self.score = 0
        self.max_cooldown = cooldown
        self.cooldown = cooldown
        self.pos_x = pos_x
        self.burger = Burger(3, pos_x, 370, [])

    def show(self, game):
        Image('plate', (150, 150)).show_position(
            game.screen, (self.pos_x - 75, 275))
        game.display_text(self.name + ': ' + str(self.score), (self.pos_x, 20))
        if self.cooldown:
            game.display_text(
                'Cool Down: ' + str(self.cooldown), (self.pos_x, 460))
        else:
            game.display_text('Attack!', (self.pos_x, 460))

        self.burger.update_burger(game.screen)

    def do_serve(self, customer_list):
        pygame.mixer.Sound('sound_serve.wav').play()
        is_served = False
        for cust_id in range(len(customer_list)):
            if customer_list[cust_id].burger.equal(self.burger):
                is_served = True
                self.score += customer_list[cust_id].count * 10
                del customer_list[cust_id]
                break
        if not is_served:
            self.score -= 50
        self.burger.clear()

    def do_trash(self):
        pygame.mixer.Sound('sound_trash.wav').play()
        self.burger.clear()

    def do_fire(self, enemy):
        if not self.cooldown:
            pygame.mixer.Sound('sound_fire.wav').play()
            enemy.burger.clear()
            self.cooldown = self.max_cooldown


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('我是廚神')
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.Clock().tick(60)
        self.prev_customer_tick = -1000
        self.now_tick = 0
        self.game_time = 100
        self.player1 = Player('Player1', 140, 30)
        self.player2 = Player('Player2', 660, 30)

        pygame.mixer.init()
        pygame.mixer.music.load('sound_background.mp3')
        pygame.mixer.music.play(1, 0)
        self.font = pygame.font.SysFont('Consolas', 30)
        self.screen = pygame.display.set_mode((800, 480))
        self.customer_list = []

    def display_background(self):
        Image('background').show_position(self.screen, (-300, -600))
        Image('ring', (50, 50)).show_position(self.screen, (300, 385))
        Image('trashcan', (50, 50)).show_position(self.screen, (380, 385))
        Image('match', (50, 50)).show_position(self.screen, (460, 385))

        chair = Image('chair', (150, 150))
        for i in range(3):
            chair.show_position(self.screen, (100 + 230 * i, 60))
        squareplate = Image('squareplate', (90, 90))
        for i in range(3):
            for j in range(2):
                squareplate.show_position(
                    self.screen, (280 + 80 * i, 250 + 60 * j))

        Image('topbun', (50, 20)).show_position(self.screen, (299, 285))
        Image('botbun', (50, 20)).show_position(self.screen, (380, 288))
        Image('beef', (50, 50)).show_position(self.screen, (460, 275))
        Image('bacon', (90, 90)).show_position(self.screen, (280, 315))
        Image('lettuce', (50, 50)).show_position(self.screen, (380, 330))
        Image('cheese', (80, 80)).show_position(self.screen, (445, 320))

        if self.game_time:
            self.display_text(str(self.game_time), (400, 20))
        else:
            self.display_text('Time\'s up!', (400, 20))

    def display_text(self, text, pos):
        text = self.font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=pos)
        self.screen.blit(text, text_rect)

    def update_customer(self):
        if random.random() < 1.0 / 40 and self.now_tick - self.prev_customer_tick > 120:
            self.prev_customer_tick = self.now_tick
            self.customer_list.append(Customer())

        for cust_id in range(len(self.customer_list)):
            self.customer_list[cust_id].move(self.screen)
        for cust_id in range(len(self.customer_list))[::-1]:
            if not self.customer_list[cust_id].show:
                del self.customer_list[cust_id]

    def catch_keyboard(self):
        keys = pygame.key.get_pressed()
        action = {
            pygame.K_q: lambda: self.player1.burger.add_ingredient('topbun_side'),
            pygame.K_w: lambda: self.player1.burger.add_ingredient('botbun_side'),
            pygame.K_e: lambda: self.player1.burger.add_ingredient('beef_side'),
            pygame.K_a: lambda: self.player1.burger.add_ingredient('bacon_side'),
            pygame.K_s: lambda: self.player1.burger.add_ingredient('lettuce_side'),
            pygame.K_d: lambda: self.player1.burger.add_ingredient('cheese_side'),
            pygame.K_z: lambda: self.player1.do_serve(self.customer_list),
            pygame.K_x: lambda: self.player1.do_trash(),
            pygame.K_c: lambda: self.player1.do_fire(self.player2),


            pygame.K_i: lambda: self.player2.burger.add_ingredient('topbun_side'),
            pygame.K_o: lambda: self.player2.burger.add_ingredient('botbun_side'),
            pygame.K_p: lambda: self.player2.burger.add_ingredient('beef_side'),
            pygame.K_k: lambda: self.player2.burger.add_ingredient('bacon_side'),
            pygame.K_l: lambda: self.player2.burger.add_ingredient('lettuce_side'),
            pygame.K_SEMICOLON: lambda: self.player2.burger.add_ingredient('cheese_side'),
            pygame.K_COMMA: lambda: self.player2.do_serve(self.customer_list),
            pygame.K_PERIOD: lambda: self.player2.do_trash(),
            pygame.K_SLASH: lambda: self.player2.do_fire(self.player1),
        }

        for key, event in action.items():
            if keys[key]:
                event()

    def start_game(self):
        while True:
            random.seed(time.time())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if self.game_time:
                        self.game_time -= 1
                    if self.player1.cooldown:
                        self.player1.cooldown -= 1
                    if self.player2.cooldown:
                        self.player2.cooldown -= 1
                if event.type == pygame.KEYDOWN:
                    self.catch_keyboard()

            self.now_tick += 1
            self.display_background()
            self.update_customer()
            self.player1.show(self)
            self.player2.show(self)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    Game().start_game()
