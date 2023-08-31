import pygame
from pygame.locals import *
import numpy as np


class GameWindow:
    full_flag = False
    frame_flag = False
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 198, 107)
    WARM = (248, 141, 30)

    def __init__(self):
        self.size = 900, 600
        self.screen = pygame.display.set_mode(self.size, flags=RESIZABLE | NOFRAME)
        self.bg = self.WARM

    def draw_background(self):
        """
        更新当前窗口大小，并填充背景颜色
        :return:
        """
        self.size = self.screen.get_size()
        self.screen.fill(self.bg)

    def draw_item(self, item=None, rect=None):
        """
        将item绘制到屏幕上
        :param item:
        :param rect:
        :return:
        """
        if item is not None:
            self.screen.blit(item, rect)

    def full_screen(self, command):
        """
        全屏并启用硬件加速
        :param command:
        :return:
        """
        if command == K_F11:
            if not self.full_flag:
                self.size = pygame.display.list_modes()[0]
                self.screen = pygame.display.set_mode(self.size, flags=RESIZABLE | FULLSCREEN | HWSURFACE)
                self.full_flag = True
            else:
                self.size = 900, 600
                self.screen = pygame.display.set_mode(self.size, flags=RESIZABLE)
                self.full_flag = False

    def frame_switch(self, command):
        """
        切换有无边框
        :param command:
        :return:
        """
        if command == K_F10:
            if not self.full_flag:
                if self.frame_flag:
                    self.screen = pygame.display.set_mode(self.size, flags=RESIZABLE | NOFRAME)
                    self.frame_flag = False
                else:
                    self.screen = pygame.display.set_mode(self.size, flags=RESIZABLE)
                    self.frame_flag = True


class ScoreIndicator:
    def __init__(self):
        self.score = 0


class Role(pygame.sprite.Sprite):
    out_of_zone = False  # 角色出界标志位
    edge_crash = True

    def __init__(self, toward, image, speed, acceleration, max_speed):
        super().__init__()
        # 角色速度，方向，朝向初始化
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.speed = np.array(speed)
        self.abs_speed = np.abs(self.speed)
        self.direction = np.array([1, 1])
        #  原始形象加载
        if toward == 'left':
            self.l_dir = pygame.image.load(image).convert_alpha()
            self.r_dir = pygame.transform.flip(self.l_dir, True, False)
        elif toward == 'right':
            self.r_dir = pygame.image.load(image).convert_alpha()
            self.l_dir = pygame.transform.flip(self.r_dir, True, False)
        else:
            'The toward of role is invalid!'
        #
        self.init_scale_ratio = 0.2
        self.scale_ratio = self.init_scale_ratio
        # 加载当前形象
        if self.speed[0] >= 0:
            self.image = pygame.transform.smoothscale(self.r_dir,
                                                      (int(self.r_dir.get_rect().width * self.scale_ratio),
                                                       int(self.r_dir.get_rect().height * self.scale_ratio)))
            self.direction[0] = 1
        else:
            self.image = pygame.transform.smoothscale(self.l_dir,
                                                      (int(self.l_dir.get_rect().width * self.scale_ratio),
                                                       int(self.l_dir.get_rect().height * self.scale_ratio)))
            self.direction[0] = -1
        if self.speed[1] >= 0:
            self.direction[1] = 1
        else:
            self.direction[1] = -1
        self.rect = self.image.get_rect()  # rect代表图片位置，四元组
        self.width = self.rect.width
        self.height = self.rect.height
        self.init_position = (np.random.randint(self.width / 2, 900 - self.width / 2),
                              np.random.randint(self.width / 2, 600 - self.height / 2))
        self.rect.center = self.init_position

    def move(self, window):
        """
        游戏的惯性系统
        :param window:
        :return:
        """
        width, height = window.screen.get_size()
        # 左右出界互斥，上下出界互斥
        # 边缘不回弹
        if not self.edge_crash:
            if self.rect.right <= 0:
                self.rect.left = width
            elif self.rect.left >= width:
                self.rect.right = 0
            if self.rect.bottom <= 0:
                self.rect.top = height
            elif self.rect.top >= height:
                self.rect.bottom = 0
        # 边缘回弹
        else:
            if self.rect.left <= 0:
                self.direction[0] = 1
                self.image = pygame.transform.smoothscale(self.r_dir,
                                                          (int(self.r_dir.get_rect().width * self.scale_ratio),
                                                           int(self.r_dir.get_rect().height * self.scale_ratio)))
                self.speed[0] = self.abs_speed[0] * self.direction[0]
            elif self.rect.right >= width:
                self.direction[0] = -1
                self.image = pygame.transform.smoothscale(self.l_dir,
                                                          (int(self.l_dir.get_rect().width * self.scale_ratio),
                                                           int(self.l_dir.get_rect().height * self.scale_ratio)))
                self.speed[0] = self.abs_speed[0] * self.direction[0]
            if self.rect.top <= 0:
                self.direction[1] = 1
                self.speed[1] = self.abs_speed[1] * self.direction[1]
            elif self.rect.bottom >= height:
                self.direction[1] = -1
                self.speed[1] = self.abs_speed[1] * self.direction[1]
        self.rect = self.rect.move(self.speed)
        # 角色出界判断
        if self.rect.right <= 0 or self.rect.bottom <= 0 or self.rect.left >= width or self.rect.top >= height:
            self.out_of_zone == True
        else:
            self.out_of_zone == False

    def collide_response(self, speed):
        """
        熊熊自身对碰撞发生的响应
        :param speed:
        :return:
        """
        # 获取方向
        if speed[0] >= 0:
            x_direction = 1
        else:
            x_direction = -1
        if speed[1] >= 0:
            y_direction = -1
        else:
            y_direction = 1
        # 若水平方向改变，则改变朝向
        if self.direction[0] != x_direction:
            self.image = pygame.transform.flip(self.image, True, False)
        # 更新速度，绝对值，方向
        self.speed = speed
        self.abs_speed = np.abs(self.speed)
        self.direction[0] = x_direction
        self.direction[1] = y_direction

        # return self

    def draw(self, window):
        """
        任意熊熊（包括主角）调用GameWindow的方法，将自己绘制到屏幕上
        :param window:
        :return:
        """
        window.draw_item(self.image, self.rect)


class OtherRole(Role):
    def __init__(self, toward, image, speed, acceleration, max_speed, name):
        super().__init__(toward, image, speed, acceleration, max_speed)
        self.name = name


class MainRole(Role):
    MainRole_image = {0: ['left', 'source/1.png'],
                      1: ['left', 'source/2.png'],
                      2: ['right', 'source/3.png']}
    MainRole_info = {0: [[-2.0, 0.0], 0.2, 20.0],
                     1: [[2.0, 1.0], 0.1, 10.0],
                     2: [[3.0, 1.0], 0.1, 1.0]}
    # edge_crash = False
    # 主角碰撞次数
    crash_count = 0  # 碰错的次数
    brake_coef = 4.0  # 刹车时的加速度等于coef * acceleration
    bingo = 0  # 正确碰撞次数

    def __init__(self, toward, image, speed, acceleration, max_speed, name):
        super().__init__(toward, image, speed, acceleration, max_speed)
        self.name = name

    def update_main_image(self):
        """
        更新主角的朝向
        :return:
        """
        x, y = self.rect.centerx, self.rect.centery
        if self.direction[0] == -1:
            self.image = pygame.transform.smoothscale(self.l_dir,
                                                      (int(self.l_dir.get_rect().width * self.scale_ratio),
                                                       int(self.l_dir.get_rect().height * self.scale_ratio)))
        else:
            self.image = pygame.transform.smoothscale(self.r_dir,
                                                      (int(self.r_dir.get_rect().width * self.scale_ratio),
                                                       int(self.r_dir.get_rect().height * self.scale_ratio)))
        self.rect = self.image.get_rect()  # 主角大小要变
        self.rect.center = (x, y)  # 但主角位置不变
        self.width = self.rect.width
        self.height = self.rect.height

    def sustained_control(self, command):
        """
        主角控制(仅改变速度，不改变位置，位置更新仅在move里）
        :param command:
        :return:
        """
        if command == K_LEFT:
            if self.direction[0] == 1:
                self.direction[0] = -1
                self.speed[0] = self.direction[0] * self.abs_speed[0]
                self.image = pygame.transform.smoothscale(self.l_dir,
                                                          (int(self.l_dir.get_rect().width * self.scale_ratio),
                                                           int(self.l_dir.get_rect().height * self.scale_ratio)))
            else:
                self.direction[0] = -1
                if self.abs_speed[0] <= self.max_speed:
                    self.abs_speed[0] += self.acceleration
                self.speed = self.direction * self.abs_speed
        elif command == K_RIGHT:
            if self.direction[0] == -1:
                self.direction[0] = 1
                self.speed[0] = self.direction[0] * self.abs_speed[0]
                self.image = pygame.transform.smoothscale(self.r_dir,
                                                          (int(self.l_dir.get_rect().width * self.scale_ratio),
                                                           int(self.l_dir.get_rect().height * self.scale_ratio)))
            else:
                self.direction[0] = 1
                if self.abs_speed[0] <= self.max_speed:
                    self.abs_speed[0] += self.acceleration
                self.speed = self.direction * self.abs_speed
        elif command == K_UP:
            if self.direction[1] == 1:
                self.direction[1] = -1
                self.speed[1] = self.direction[1] * self.abs_speed[1]
            else:
                self.direction[1] = -1
                if self.abs_speed[1] <= self.max_speed:
                    self.abs_speed[1] += self.acceleration
                self.speed = self.direction * self.abs_speed
        elif command == K_DOWN:
            if self.direction[1] == -1:
                self.direction[1] = 1
                self.speed[1] = self.direction[1] * self.abs_speed[1]
            else:
                self.direction[1] = 1
                if self.abs_speed[1] <= self.max_speed:
                    self.abs_speed[1] += self.acceleration
                self.speed = self.direction * self.abs_speed
        elif command == K_SPACE:
            if self.abs_speed[0] >= 1.0:
                self.abs_speed[0] -= self.acceleration * self.brake_coef
            if self.abs_speed[1] >= 1.0:
                self.abs_speed[1] -= self.acceleration * self.brake_coef
            self.speed = self.abs_speed * self.direction
        elif command == K_EQUALS:
            if self.scale_ratio <= 0.7:
                self.scale_ratio += 0.05
                self.update_main_image()
        elif command == K_MINUS:
            if self.scale_ratio >= 0.1:
                self.scale_ratio -= 0.05
                self.update_main_image()
        elif command == K_0:
            self.scale_ratio = self.init_scale_ratio
            self.update_main_image()

    def discrete_control(self, command):
        """
        处理不宜持续检测的操作
        :param command:
        :return:
        """
        # 主角复位
        if command == K_r:
            self.rect.center = self.init_position
        # 转换角色
        elif command == K_1:
            self.switch(0)
        elif command == K_2:
            self.switch(1)
        elif command == K_3:
            self.switch(2)
        # 边缘碰撞模式切换
        elif command == K_e:
            self.edge_crash = not self.edge_crash
            if self.out_of_zone:  # 按e的同时如果出界，则复位
                self.rect.center = self.init_position

    def switch(self, i):
        """
        切换当前主角
        :param i:
        :return:
        """
        if self.name != i:
            # 速度处理
            speed = self.speed
            center = self.rect.center
            # 当前速度超过了切换角色的最大速度，则强制更改速度
            if self.abs_speed[0] > self.MainRole_info[i][2]:
                speed[0] = self.direction[0] * self.MainRole_info[i][2]
            if self.abs_speed[1] > self.MainRole_info[i][2]:
                speed[1] = self.direction[1] * self.MainRole_info[i][2]
            super().__init__(self.MainRole_image[i][0], self.MainRole_image[i][1],
                             speed, self.MainRole_info[i][1], self.MainRole_info[i][2])
            self.rect.center = center
            self.name = i
