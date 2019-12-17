import pygame
import sys
import datetime

pygame.init()  # 初始化pygame
size = width, height = 800, 480  # 設定視窗大小
screen = pygame.display.set_mode(size)  # 顯示視窗
color = (255, 255, 255)  # 設定顏色
transparent = (0, 0, 0, 0)  # 為了之後讓球消失，第四個零代表完全隱形
customer = pygame.image.load('C:\\Users\\howie\\Desktop\\man1.png')  # 載入圖片
customer = pygame.transform.scale(customer, (150, 150))
customer_rect = customer.get_rect()  # 獲取矩形區域
customer_rect.center = (0,175)  # 人的起始位置
speed = [1, 0]  # 設定移動的X軸、Y軸
clock = pygame.time.Clock()  # 設定時鐘
pygame.display.set_caption("我是廚神")  # 遊戲視窗標題

counter1, text1 = 60, '60'.rjust(3)  # 時間倒數
counter2, text5 = 30, 'Cool Down' + '30'.rjust(3)
counter3, text6 = 30, 'Cool Down' + '30'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)  # 字體

def Player1_text(text, x, y):  # 專門顯示文字的方法，除了顯示文字還能指定顯示的位置
    x = x
    y = y
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))
    #pygame.display.update()

def Player2_text(text, x, y):  
    x = x
    y = y
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))
    #pygame.display.update()

score1 = 0  # 初始分數
score2 = 0

def show_plate(image, x, y):  # 顯示左盤子
    x = x
    y = y
    image = pygame.transform.scale(image, (150, 150))  # 調整圖片大小
    screen.blit(image, (x, y))
    #pygame.display.update()
    
def show_image(image, x, y):  # 顯示圖片
    x = x
    y = y
    image = pygame.transform.scale(image, (50, 50))  # 調整圖片大小
    screen.blit(image, (x, y))
    #pygame.display.update()

def show_tbun(image, x, y):  # 顯示上餅皮
    x = x
    y = y
    image = pygame.transform.scale(image, (50, 20))  # 調整圖片大小
    screen.blit(image, (x, y))
    #pygame.display.update()

def show_bbun(image, x, y):  # 顯示下餅皮
    x = x
    y = y
    image = pygame.transform.scale(image, (50, 10))  # 調整圖片大小
    screen.blit(image, (x, y))

def show_cheese(image, x, y):  # 顯示起司
    x = x
    y = y
    image = pygame.transform.scale(image, (80, 80))  # 調整圖片大小
    screen.blit(image, (x, y))

def show_bacon(image, x, y):  # 顯示培根
    x = x
    y = y
    image = pygame.transform.scale(image, (90, 90))  # 調整圖片大小
    screen.blit(image, (x, y))

def show_chair(image, x, y):  # 顯示桌椅
    x = x
    y = y
    image = pygame.transform.scale(image, (150, 150))  # 調整圖片大小
    screen.blit(image, (x, y))
def show_nplate(image, x, y):  # 顯示托盤
    x = x
    y = y
    image = pygame.transform.scale(image, (90, 90))  # 調整圖片大小
    screen.blit(image, (x, y))

class Background(pygame.sprite.Sprite):  # 背景
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load('C:\\Users\\howie\\Desktop\\亮background.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
		
BackGround = Background('C:\\Users\\howie\\Desktop\\亮background.png', [-300,-600])  # 調整位置

tbun = pygame.image.load('C:\\Users\\howie\\Desktop\\漢堡上bun.png')
bbun = pygame.image.load('C:\\Users\\howie\\Desktop\\漢堡下bun.png')
beef = pygame.image.load('C:\\Users\\howie\\Desktop\\牛肉.png')
pork = pygame.image.load('C:\\Users\\howie\\Desktop\\培根.png')
lettuce = pygame.image.load('C:\\Users\\howie\\Desktop\\lettuce.png')
cheese = pygame.image.load('C:\\Users\\howie\\Desktop\\cheese slice 1.png')
ring = pygame.image.load('C:\\Users\\howie\\Desktop\\鈴.png')
garbage = pygame.image.load('C:\\Users\\howie\\Desktop\\垃圾桶.png')
match = pygame.image.load('C:\\Users\\howie\\Desktop\\火柴.png')
chair = pygame.image.load('C:\\Users\\howie\\Desktop\\chair.png')
nplate = pygame.image.load('C:\\Users\\howie\\Desktop\\方形托盤.png') 



		
while True:  # 死迴圈確保視窗一直顯示
    clock.tick(80)  # 每秒執行80次
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
    customer_rect = customer_rect.move(speed)  # 移動人

    if customer_rect.right > 950:  # 視窗寬度800+圖片寬度150 == 950，讓球隱藏
        customer.fill(transparent)
   

    screen.fill(color)  # 填充顏色
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
    text2 = ('Player1:' + ' ' + str(score1))  # 顯示玩家&分數
    text3 = ('Player2:' + ' ' + str(score2))
    Player1_text(text2, 0, 0)  # 顯示Player1位置
    Player2_text(text3, 600, 0)  # 顯示Player2
    
    plate = pygame.image.load('C:\\Users\\howie\\Desktop\\盤子.png')
    show_plate(plate, 50, 275)  # 盤子1
    show_plate(plate, 600, 275)  # 盤子2
    
	
    #顯示九宮格物件，以圖片長寬(50)為單位排列
    show_chair(chair, 330, 60)
    show_chair(chair, 560, 60)
    show_chair(chair, 100, 60)
    screen.blit(customer, customer_rect)  # 將圖片畫到視窗上
    show_nplate(nplate, 280, 250)
    show_nplate(nplate, 360, 250)
    show_nplate(nplate, 440, 250)
    show_nplate(nplate, 280, 310)
    show_nplate(nplate, 360, 310)
    show_nplate(nplate, 440, 310)
    show_tbun(tbun, 300, 285)
    show_bbun(bbun, 380, 295)
    show_image(beef, 460, 275)
    show_bacon(pork, 280, 315)
    show_image(lettuce, 380, 330)
    show_cheese(cheese, 445, 320)
    show_image(ring, 300, 385)
    show_image(garbage, 380, 385)
    show_image(match, 460, 385)
    

    pygame.display.flip()  # 更新全部顯示

pygame.quit()  # 退出pygame









