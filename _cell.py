import pygame

lei_img = pygame.image.load('images/lei.png')
ban_img = pygame.image.load('images/ban.png')
beijing_img = pygame.image.load('images/beijing.png')
over_img = pygame.image.load('images/gameover.png')
win_img = pygame.image.load('images/win.png')
qizi_img = pygame.image.load('images/qizi.png')

num_images = {
    1: pygame.image.load('images/1.png'),
    2: pygame.image.load('images/2.png'),
    3: pygame.image.load('images/3.png'),
    4: pygame.image.load('images/4.png'),
    5: pygame.image.load('images/5.png')
}


class Cell:
    """
    遮盖板,数字,雷,旗子
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.ban = None
        self.lei = None
        self.num = None
        self.qizi = None

    def add_lei(self):
        self.lei = lei_img

    def add_num(self, n):
        self.num = num_images[n]

    def add_ban(self):
        self.ban = ban_img

    def add_qizi(self):
        self.qizi = qizi_img

    @property
    def isempty(self):
        return self.lei is None and self.num is None

    @property
    def zhoubian(self):
        """返回格子周围坐标"""
        x, y = self.x, self.y
        m = [(x - 32, y - 32), (x, y - 32), (x + 32, y - 32), (x - 32, y),
             (x + 32, y), (x - 32, y + 32), (x, y + 32), (x + 32, y + 32)]
        return m

    @property
    def zuobiao(self):
        return self.x, self.y

    def clear(self):
        """清空格子"""
        self.ban = None
        self.lei = None
        self.num = None
        self.qizi = None
