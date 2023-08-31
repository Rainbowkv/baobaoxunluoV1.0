import time
import traceback
import pygame
from pygame.locals import *
import sys
from any_class import *
from physic_engine import *
from world_info import *
from game_class import *


def main():
    """
    这是一个宝宝专属游戏，在此main2.py文件点击运行即可开始游戏
    游戏过程中请将输入法切换到英文，否则大部分操作不能进行
    """
    # 生成一个游戏窗口
    game_window = GameWindow()
    # 生成一个游戏实例
    game = Game()
    # 时钟
    clock = pygame.time.Clock()
    # 游戏运行标志
    running = True
    while running:
        # 游戏得分
        game.update_sco(game.main_bear)
        for event in pygame.event.get():
            # 窗口X退出游戏
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 支持持续按键的控制
            if event.type == KEYDOWN:
                game.main_bear.sustained_control(event.key)
            # 不支持持续按键的控制
            if event.type == KEYUP:
                game_window.full_screen(event.key)
                game_window.frame_switch(event.key)
                game.main_bear.discrete_control(event.key)
                if event.key == K_p:
                    game = Game()
                # 按q退出游戏
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
        # 更新游戏数据
        game.update(game_window)
        # 内存图像数据翻转到屏幕
        pygame.display.flip()
        clock.tick(game.FPS)
        # 超过游戏时长自动结束
        if game.timer >= game.TIMER:
            # 结束画面绘制，并返回游戏是否重新开始的标志
            running = game.end(game_window)
            if running:
                game = Game()
                # 重置游戏参数


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
