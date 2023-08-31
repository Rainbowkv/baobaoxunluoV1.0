import time
import traceback
import pygame
from pygame.locals import *
import sys
from any_class import *
from physic_engine import *
from world_info import *


class Game:
    def __init__(self):
        # 读取最好成绩
        f = open('source/score.txt', 'r', encoding='UTF-8')
        self.best_score = float(f.readline())
        print(self.best_score, type(self.best_score))
        f.close()
        self.final_score = 0
        # 初始化基本参数，背景音乐,音效
        # 初始化pygame
        pygame.init()
        pygame.key.set_repeat(10, 15)
        pygame.mixer.music.load('source/1.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.bingo_sound = pygame.mixer.Sound('source/bingo.mp3')
        self.bingo_sound.set_volume(0.3)
        self.crash_count_sound = pygame.mixer.Sound('source/crash_count.mp3')
        self.crash_count_sound.set_volume(0.3)
        # 初始窗口
        pygame.display.set_caption('宝宝巡逻 (v2.0)------------------------by Milky Way')
        # 记录游戏时长
        self.while_count = 0
        self.timer = 0.0
        # 单次游戏时长
        self.TIMER = 30
        # 剩余时间
        self.residual_time = self.TIMER
        # 游戏开始的时间记为第一次碰撞的时间
        self.s = time.time()
        self.detection_interval = 0.5
        self.score = 0
        # 得分
        self.break_score_font = pygame.font.Font("source/Texturina Medium.ttf", 50)
        self.chinese2_font = pygame.font.Font("source/chinese2.ttf", 25)
        self.score_font = pygame.font.Font("source/Texturina Medium.ttf", 17)
        self.best_score_font = pygame.font.Font("source/Texturina Medium.ttf", 17)
        self.residual_time_font = pygame.font.Font("source/Texturina Medium.ttf", 17)
        self.replay_text = self.chinese2_font.render('按p重新开始', True, BLACK)
        self.hint_text = self.chinese2_font.render('别被撞到咯', True, BLACK)
        self.score_text = self.score_font.render('score : %s' % str(self.score), True, BLACK)
        self.best_score_text = self.best_score_font.render('best_score : %s' % str(self.best_score), True, BLACK)
        self.residual_time_text = self.residual_time_font.render('score : %s' % str(self.residual_time), True, BLACK)
        # 单次游戏时长
        self.TIMER = 60
        # 游戏帧率
        self.FPS = 60  # 代表一秒钟执行多少次while循环
        # 初始主角
        self.init_role = 1
        self.main_bear = MainRole(MainRole_image[self.init_role][0], MainRole_image[self.init_role][1],
                                  MainRole_info[self.init_role][0], MainRole_info[self.init_role][1],
                                  MainRole_info[self.init_role][2], self.init_role)
        # 初始其他熊
        self.bear_num = 2
        self.bears = []
        self.add_bear_delay = 10  # 增加熊的时间间隔10s
        self.add_bear_count = self.FPS * self.add_bear_delay
        self.t1 = 10
        self.t2 = 40
        # 做j次循环，生成bear_num头熊
        for j in range(self.bear_num):
            i = np.random.randint(0, 3)
            speed = [np.random.randint(0, 10), np.random.randint(0, 10)]
            other_bear = OtherRole(MainRole_image[i][0], MainRole_image[i][1], speed, MainRole_info[i][1],
                                   20, i)
            self.bears.append(other_bear)

    def update_sco(self, main_bear):
        """
        更新游戏得分，剩余时间，并绘制；最终得分更新为最新的游戏得分
        :param main_bear: 当前游戏主角，MainRole类型
        :return:
        """
        self.score = self.timer * 100 + main_bear.bingo * 500 - main_bear.crash_count * 300
        self.score_text = self.score_font.render('score : %s' % str(self.score), True, BLACK)
        self.final_score = self.score
        self.residual_time = self.TIMER - self.timer
        self.residual_time_text = self.residual_time_font.render('time : %s S' % str(self.residual_time), True, BLACK)

    def update(self, game_window: GameWindow):
        """
        游戏实时画面的更新
        :param game_window: 绘制游戏的窗口
        :return:
        """
        # 增加熊的数量
        self.add_bear_count -= 1
        if self.add_bear_count == 0:
            if self.timer <= self.t1:
                self.add_bear_count = self.FPS * self.add_bear_delay
            elif self.timer <= self.t2:
                self.add_bear_count = self.FPS * self.add_bear_delay * 0.8
            elif self.timer <= self.TIMER:
                self.add_bear_count = self.FPS * self.add_bear_delay * 0.6
            i = np.random.randint(0, 3)
            speed = [np.random.randint(0, 10), np.random.randint(0, 10)]
            other_bear = OtherRole(MainRole_image[i][0], MainRole_image[i][1], speed, MainRole_info[i][1],
                                   20, i)
            self.bears.append(other_bear)
            self.bear_num += 1
        # 更新游戏进行的时长
        self.while_count += 1
        if self.while_count % self.FPS == 0:
            print(self.timer)
            self.timer += 1
            self.while_count = 0
        # 更新角色位置
        self.main_bear.move(game_window)
        for other_bear in self.bears:
            other_bear.move(game_window)
        # 主角与路人的独特碰撞引擎，应更新主角速度，绝对值，方向，朝向, 碰撞次数
        tmp_crash_info = collide_process2(self.main_bear, self.bears)  # 碰撞信息
        if tmp_crash_info[0] and time.time() - self.s >= self.detection_interval:
            if tmp_crash_info[1] == tmp_crash_info[2]:
                self.main_bear.bingo += 1
                self.bingo_sound.play()
                # 播放音效
            else:
                self.main_bear.crash_count += 1
                self.crash_count_sound.play()
            self.s = time.time()
        # 路人间碰撞引擎，应更新角色速度，绝对值，方向，朝向
        collide_process(self.bear_num, self.bears)
        # 渲染游戏画面
        game_window.draw_background()
        # 得分绘制
        game_window.draw_item(self.replay_text, (int(game_window.size[0] * 0.8), int(game_window.size[1] * 0.06)))
        game_window.draw_item(self.hint_text, (int(game_window.size[0] * 0.8), 0))
        game_window.draw_item(self.best_score_text, (0, 0))
        game_window.draw_item(self.score_text, (0, int(game_window.size[1] * 0.03)))
        game_window.draw_item(self.residual_time_text, (0, int(game_window.size[1] * 0.06)))
        # 人物绘制
        self.main_bear.draw(game_window)
        for other_bear in self.bears:
            other_bear.draw(game_window)

    def end(self, game_window):
        """
        处理游戏结束，绘制游戏结算画面，并返回游戏是否重开的bool值
        :param game_window:绘制游戏的窗口
        :return:
        """
        pygame.mixer.music.set_volume(0.0)  # 停止音乐
        game_window.draw_background()
        end_font = pygame.font.Font("source/chinese2.ttf", 36)
        if self.final_score > self.best_score:
            f = open('source/score.txt', 'w', encoding='UTF_8')
            f.write(str(self.final_score))
            f.flush()
            f.close()
            game_window.draw_item(self.score_text, (0, 0))
            break_score_text = self.break_score_font.render('Score : %s' % str(self.score), True, BLACK)
            game_window.draw_item(break_score_text, (int(game_window.size[0] * 0.3), int(game_window.size[1] * 0.3)))
            end_text = end_font.render('破纪录啦，真厉害我宝宝！c:再玩一次 q:论文写不完啦！', True, game_window.BLACK)
        else:
            end_text = end_font.render('宝宝肥起! c:再玩一次 q:先不玩啦', True, game_window.BLACK)
        game_window.draw_item(end_text, (0, game_window.size[1] // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_q:
                        return False
                    if event.key == K_c:
                        return True
