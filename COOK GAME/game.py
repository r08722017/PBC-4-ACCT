import pygame
import sys
import datetime
import random

pygame.mixer.init()
pygame.mixer.music.load('sound_background.mp3')
pygame.mixer.music.play(1, 0)

window_size = (800, 480)
window_color = (255, 255, 255)

pygame.init()
pygame.display.set_caption("我是廚神")
screen = pygame.display.set_mode(window_size)  # 顯示視窗
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)  # 字體
transparent = (0, 0, 0, 0)  # 為了之後讓球消失，第四個零代表完全隱形

clock = pygame.time.Clock()  # 設定時鐘

counter1, text1 = 200, '200'.rjust(3)  # 時間倒數
counter2, text5 = 30, 'Cool Down' + '30'.rjust(3)
counter3, text6 = 30, 'Cool Down' + '30'.rjust(3)

def show_text(text, x, y):  # 專門顯示文字的方法，除了顯示文字還能指定顯示的位置
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))
    
def show_image(image, x, y):  # 顯示圖片
    image = pygame.transform.scale(image.image, image.size)  # 調整圖片大小
    screen.blit(image, (x, y))

class Background(pygame.sprite.Sprite):  # 背景
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load('亮background.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
BackGround = Background('亮background.png', [-300,-600])  # 調整位置

class MyImage:

    def __init__(self, name, size, path):
        self.name = name
        self.size = size
        self.image = pygame.image.load(path)

image_dict = {
    'tbun': MyImage('tbun', (50, 20), '漢堡上bun.png'),
    'bbun': MyImage('tbun', (50, 20), '漢堡下bun.png'),
    'beef': MyImage('tbun', (50, 50), '牛肉.png'),
    'bacon': MyImage('tbun', (90, 90), '培根.png'),
    'lettuce': MyImage('tbun', (50, 50), 'lettuce.png'),
    'cheese': MyImage('tbun', (80, 80), 'cheese.png'),
    'ring': MyImage('tbun', (50, 59), '鈴.png'),
    'garbage': MyImage('tbun', (50, 50), '垃圾桶.png'),
    'match': MyImage('tbun', (50, 50), '火柴.png'),
    'chair': MyImage('tbun', (150, 150), 'chair.png'),
    'nplate': MyImage('tbun', (90, 90), '方形托盤.png'),
    'plate': MyImage('tbun', (150, 150), '盤子.png'),
    'customer': MyImage('customer', (150, 150), 'man.png'),
}

def build_customer(path):
    customer = pygame.image.load(path)  # 載入圖片
    customer = pygame.transform.scale(customer, (150, 150))
    customer_rect = customer.get_rect()  # 獲取矩形區域
    customer_rect.center = (0, 175)  # 人的起始位置

    speed = [1, 0]
    if 'wizard' in path:
        speed = [3, 0]
    if 'superhero' in path:
        speed = [2, 0]
    return (customer, customer_rect, speed)

score1 = 0
score2 = 0
customer_path = ['man.png', 'superhero.png', 'wizard.png']
customer_list = []

customer = pygame.image.load(customer_path[0])  # 載入圖片
customer = pygame.transform.scale(customer, (150, 150))
customer_rect = customer.get_rect()  # 獲取矩形區域
customer_rect.center = (100, 175)  # 人的起始位置

prev_customer_tick = -1000
now_tick = 0

clock.tick(80)  # 每秒執行80次
while True:  # 死迴圈確保視窗一直顯示
    now_tick += 1    
    for event in pygame.event.get():  # 遍歷所有事件
        if event.type == pygame.QUIT:  # 如果單擊關閉視窗，則退出
            sys.exit()
        if event.type == pygame.USEREVENT:  # 讓秒數倒數 
          counter1 -= 1
          text1 = str(counter1).rjust(3) if counter1 > 0 else "Time's up!"  # 秒數歸零時顯示時間到
          counter2 -= 1
          text5 = 'Cool Down' + str(counter2).rjust(3) if counter2 > 0 else "Attack!"  # 秒數歸零時顯示時間到
          counter3 -= 1
          text6 = 'Cool Down' + str(counter3).rjust(3) if counter3 > 0 else "Attack!"  # 秒數歸零時顯示時間到

    screen.fill(window_color)  # 填充顏色
    screen.blit(BackGround.image, BackGround.rect)
    
    if counter1 > 0:
        screen.blit(font.render(text1, True, (0, 0, 0)), (370, 0))  # 顯示倒數時間
    else:
        screen.blit(font.render(text1, True, (0, 0, 0)), (325, 0))  # 顯示倒數時間
    if counter2 > 0:
        screen.blit(font.render(text5, True, (0, 0, 0)), (5, 450))  # 顯示倒數時間
    else:
        screen.blit(font.render(text5, True, (0, 0, 0)), (70, 450))  # 顯示倒數時間
    if counter3 > 0:
        screen.blit(font.render(text6, True, (0, 0, 0)), (580, 450))  # 顯示倒數時間
    else:
        screen.blit(font.render(text6, True, (0, 0, 0)), (620, 450))  # 顯示倒數時間
    
    show_text('Player1: ' + str(score1), 0, 0)  # 顯示Player1位置
    show_text('Player2: ' + str(score2), 600, 0)  # 顯示Player2

    show_image(image_dict['plate'], 50, 275)  # 盤子1
    show_image(image_dict['plate'], 600, 275)  # 盤子2

    for i in range(3):
        show_image(image_dict['chair'], 100 + 230 * i, 60)

    for i in range(3):
        for j in range(2):
            show_image(image_dict['nplate'], 280 + 80 * i, 250 + 60 * j)

    show_image(image_dict['tbun'], 299, 285)
    show_image(image_dict['bbun'], 380, 288)
    show_image(image_dict['beef'], 460, 275)
    show_image(image_dict['bacon'], 280, 315)
    show_image(image_dict['lettuce'], 380, 330)
    show_image(image_dict['cheese'], 445, 320)
    show_image(image_dict['ring'], 300, 385)
    show_image(image_dict['garbage'], 380, 385)
    show_image(image_dict['match'], 460, 385)

    if random.random() < 1.0 / 40 and now_tick - prev_customer_tick > 120:
        prev_customer_tick = now_tick
        customer = build_customer(customer_path[random.randint(0, 2)])
        customer_list.append(customer)

    for i in range(len(customer_list)):
        customer = customer_list[i][0]
        customer_rect = customer_list[i][1]
        speed = customer_list[i][2]
        customer_rect = customer_rect.move(speed)  # 移動人
        if customer_rect.right > 950:  # 視窗寬度800+圖片寬度150 == 950，讓球隱藏
            customer.fill(transparent)
        customer_list[i] = customer, customer_rect, speed

    for customer, customer_rect, speed in customer_list:
        screen.blit(customer, customer_rect)  # 將圖片畫到視窗上
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c] or keys[pygame.K_SLASH]:
        s = pygame.mixer.Sound('sound_fire.wav')
        s.play()
    if keys[pygame.K_x] or keys[pygame.K_PERIOD]:
        s = pygame.mixer.Sound('sound_trash.wav')
        s.play()
    if keys[pygame.K_z] or keys[pygame.K_COMMA]:
        s = pygame.mixer.Sound('sound_serve.wav')
        s.play()

    pygame.display.flip()  # 更新全部顯示

pygame.quit()  # 退出pygame