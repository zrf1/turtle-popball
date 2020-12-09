# -*- coding: utf-8 -*-
'''
1、实现游戏流程：开始，游戏，失败
2、创建小球
3、模拟小球反弹
'''
from turtle import *
from random import randint, choice
from time import sleep

# 初始化
w, h = 480, 600
screen = Screen()
screen.setup(w, h)
screen.title("弹球小游戏")
screen.bgcolor("black")
# 图片资源
start_pic = 'res/start.gif'
fail_pic = 'res/fail.gif'
back_pic = 'res/back.gif'

#########################################################

# 小球
ball = Turtle(shape='circle')  # 新建海龟，形状为圆形
ball.speed(0)
ball.penup()
ball.color("yellow", "yellow")
ball_fd = randint(3, 6)  # 小球移动速度
ball_hd = randint(45, 135) * choice([1, -1])  # 小球移动角度，避免水平夹角过小

# 游戏状态：0 开始，1 游戏，2 失败
state_index = 0


def GameState():
    global state_index, ball_fd, ball_hd
    if state_index in [0, 2]:
        # 重新开始游戏
        screen.bgpic(back_pic)
        screen.update()
        ball_fd = randint(3, 6)  # 小球移动速度
        ball_hd = randint(45, 135) * choice([1, -1])  # 小球移动角度，避免水平夹角过小
        ball.goto(0, 0)
        ball.seth(ball_hd)
        state_index = 1


screen.onkeypress(GameState, "space")
screen.listen()

#########################################################

while True:
    if state_index == 0:
        # 游戏开始
        screen.bgpic(start_pic)
        screen.update()

    elif state_index == 1:
        # 正常游戏，移动小球
        ball.fd(ball_fd)
        if ball_hd != ball.heading():
            print(ball_fd, ball.heading())
        ball_hd = ball.heading()

        x = ball.xcor()
        y = ball.ycor()
        # 右边界反弹
        if x > w/2:
            if ball.heading() < 90:
                ang = 180 - ball.heading()*2
                ball.lt(ang)
            elif ball.heading() > 270:
                ang = 180 - (360 - ball.heading())*2
                ball.rt(ang)
        # 左边界反弹
        if x < -w/2:
            if ball.heading() < 180:
                ang = 180 - (180 - ball.heading())*2
                ball.rt(ang)
            elif ball.heading() > 180:
                ang = 180 - (ball.heading() - 180)*2
                ball.lt(ang)
        # 上边界反弹
        if y > h/2:
            if ball.heading() < 90:
                ang = ball.heading() * 2
                ball.rt(ang)
            elif ball.heading() > 90:
                ang = 180 - (ball.heading() - 90)*2
                ball.lt(ang)
        # 下边界超出，失败
        if y < -h/2:
            state_index = 2

    elif state_index == 2:
        # 游戏失败
        screen.bgpic(fail_pic)
        screen.update()
    sleep(0.01)

mainloop()
