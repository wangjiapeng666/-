import sys
import random

import pygame

import _cell


def draw_cell(screen, cells):
    screen.blit(_cell.beijing_img, _cell.beijing_img.get_rect())  # 画背景
    for c in cells:
        x, y = c.zuobiao
        if c.lei:
            screen.blit(c.lei, (x + 1, y + 1))
        if c.num:
            screen.blit(c.num, (x + 1, y + 1))
        if c.ban:
            screen.blit(c.ban, (x, y))
        if c.qizi:
            screen.blit(c.qizi, (x + 1, y + 1))


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((320, 320))  # 设置窗口大小
    pygame.display.set_caption('扫雷')
    state = 'running'  # 以此判断游戏状态 over,win

    # 生成格子
    cells = []
    for x in range(0, 320, 32):
        for y in range(0, 320, 32):
            cells.append(_cell.Cell(x, y))

    def init():
        """
        初始化游戏数据
        """

        # 添加雷
        lei = random.sample(cells, 11)

        for cell in lei:
            cell.add_lei()

        # 添加数字
        zuobiao_dict = {}

        for cell in lei:
            m = cell.zhoubian
            for zb in m:
                if zb in zuobiao_dict:
                    zuobiao_dict[zb] += 1
                else:
                    zuobiao_dict[zb] = 1

        for cell in cells:
            zb = (cell.x, cell.y)
            if cell.lei is None and zb in zuobiao_dict:
                cell.add_num(zuobiao_dict[zb])
                # print(zuobiao_dict[zb])

        # 添加板
        for cell in cells:
            cell.add_ban()

    def removeban(cell):
        """移除遮盖板"""
        if cell.qizi is None:
            cell.ban = None
            if cell.isempty:  # 如果是空白
                m = cell.zhoubian  # 获取周边坐标
                for i in m:  # 迭代周边坐标
                    for c in cells:
                        if c.ban and i == c.zuobiao:  # 如果这个坐标有板覆盖则移除板
                            removeban(c)  # 递归调用直到不再有空白

    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # 点击事件
                # print(event.button)
                x, y = pygame.mouse.get_pos()
                if event.button == 1:
                    if state == 'running':
                        for cell in cells:
                            cx, cy = cell.zuobiao
                            if cx <= x < cx + 32 and cy <= y < cy + 32:
                                if cell.ban:
                                    removeban(cell)
                                    if cell.qizi is None and cell.lei:
                                        state = 'game over'
                                    else:
                                        b = [c for c in cells if c.ban]
                                        if len(b) == 11:
                                            state = 'win'
                    else:
                        # 重置游戏数据
                        for c in cells:
                            c.clear()
                        init()
                        state = 'running'
                elif event.button == 3:
                    if state == 'running':
                        for cell in cells:
                            cx, cy = cell.zuobiao
                            if cx <= x < cx + 32 and cy <= y < cy + 32:
                                if cell.ban and cell.qizi is None:
                                    cell.add_qizi()
                                elif cell.qizi:
                                    cell.qizi = None
            if event.type == pygame.QUIT:
                sys.exit()

        draw_cell(screen, cells)
        if state == 'game over':
            screen.blit(_cell.over_img, _cell.over_img.get_rect())
        elif state == 'win':
            screen.blit(_cell.win_img, _cell.win_img.get_rect())
        pygame.display.flip()  # 刷新
        pygame.time.delay(20)


run_game()
