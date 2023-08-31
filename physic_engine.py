import numpy as np


def collide_detection(one, the_other):
    """
    检测两个Role类型的熊是否发生碰撞
    :param one:
    :param the_other:
    :return:
    """
    real_dis = np.sqrt(
        np.power(one.rect.centerx - the_other.rect.centerx, 2) + np.power(one.rect.centery - the_other.rect.centery, 2))
    if real_dis <= one.rect.height // 2 + the_other.rect.height // 2:
        return True
    else:
        return False


# 碰撞模型
def generate_v_after_collide(v1, v2):
    """
    返回相撞后两头熊的速度
    :param v1:
    :param v2:
    :return:
    """

    # tmp = v1.copy()
    # v1 = v2.copy()
    # v2 = tmp.copy()

    return -v1, -v2


# 更新撞车熊熊的速度
def collide_process(bear_num, inner_bears):
    """
    处理配角间的碰撞
    :param bear_num: 当前配角的数量
    :param inner_bears: 存放当前配角的列表
    :return:
    """
    for i in range(bear_num):
        j = i + 1
        while j < bear_num:
            if collide_detection(inner_bears[i], inner_bears[j]):
                vi, vj = generate_v_after_collide(inner_bears[i].speed, inner_bears[j].speed)
                inner_bears[i].collide_response(vi)  # inner_bears[i] =
                inner_bears[j].collide_response(vj)  # inner_bears[j] =
            j += 1


def collide_process2(main_bear, bears) -> [bool, int, int]:
    """
    处理主角与其它配角的碰撞函数
    :param main_bear: 当前主角
    :param bears: 配角
    :return: return[0]代表主角当前是否发生碰撞，若碰撞则是return[1]和return[2]种类编号的熊发生碰撞
    """
    for bear in bears:
        if collide_detection(main_bear, bear):
            vi, vj = generate_v_after_collide(main_bear.speed, bear.speed)
            main_bear.collide_response(vi)
            bear.collide_response(vj)
            return True, main_bear.name, bear.name
    return False, -1, -1  # 没有碰撞则返回两个角色的序号-1
