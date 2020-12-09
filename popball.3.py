# -*- coding: utf-8 -*-
'''
1、添加计分功能
2、添加声音效果(todo)
'''

from turtle import *
from random import randint, choice
from time import sleep
from winsound import PlaySound, SND_ASYNC

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
score_now = 0
score_high = 0

#########################################################

# 小球
ball = Turtle(shape='circle')  # 新建海龟，形状为圆形
ball.speed(0)
ball.penup()
ball.color("yellow", "yellow")
ball_fd = randint(5, 9)  # 小球移动速度
ball_hd = randint(45, 135) * choice([1, -1])  # 小球移动角度，避免水平夹角过小

# 挡板
board = Turtle(shape='square')  # 新建海龟，形状为长方形
board.shapesize(0.5, 5)  # 形状为100x10像素
board.speed(0)
board.penup()
board.color("white", "white")
board.sety(-h/2 + 30)  # 距下沿30像素


def BoardLeft():
    if board.xcor() > -w/2 + 50:
        board.setx(board.xcor() - 10)


def BoardRight():
    if board.xcor() < w/2 - 50:
        board.setx(board.xcor() + 10)


# 计分
pen1 = Turtle()
pen1.ht()
pen1.up()
pen1.color("white")
pen1.goto(-w/2 + 30, h/2 - 30)
pen1.write('当前得分：%d' % score_now, align='left', font={"Arial", 20, 'bold'})

pen2 = Turtle()
pen2.ht()
pen2.up()
pen2.color("white")
pen2.goto(w/2 - 30, h/2 - 30)
pen2.write('最高得分：%d' % score_high, align='right', font={"Arial", 20, 'bold'})


# 游戏状态：0 开始，1 游戏，2 失败
state_index = 0


def GameState():
    global state_index, ball_fd, ball_hd, score_now
    if state_index in [0, 2]:
        # 重新开始游戏
        screen.bgpic(back_pic)
        screen.update()
        score_now = 0
        ball_fd = randint(3, 6)  # 小球移动速度
        ball_hd = randint(45, 135) * choice([1, -1])  # 小球移动角度，避免水平夹角过小
        ball.goto(0, 0)
        ball.seth(ball_hd)
        pen1.clear()
        pen1.write('当前得分：%d' % score_now, align='left',
                   font={"Arial", 20, 'bold'})
        pen2.clear()
        pen2.write('最高得分：%d' % score_high, align='right',
                   font={"Arial", 20, 'bold'})
        state_index = 1

screen.onkeypress(BoardLeft, "Left")
screen.onkeypress(BoardRight, "Right")
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
            elif ball.heading()>270:
                ang = 180 -(360 - ball.heading())*2
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
            PlaySound('res/fail.wav', SND_ASYNC)

        board_x1 = board.xcor() - 50
        board_x2 = board.xcor() + 50
        board_y1 = board.ycor() + 5
        board_y2 = board.ycor() - 5

        if x > board_x1 and x < board_x2 and y < board_y1 and y > board_y2:
            # 挡板反弹
            if ball.heading() < 270:
                ang = 180 - (270 - ball.heading())*2
                ball.rt(ang)
            else:
                ang = 180 - (ball.heading() - 270)*2
                ball.lt(ang)
            ball.fd(ball_fd)
            PlaySound('res/pop.wav', SND_ASYNC)
            
            # 计分
            score_now += 10
            score_high = score_now if score_now > score_high else score_high
            pen1.clear()
            pen1.write('当前得分：%d' % score_now, align='left',
                       font={"Arial", 20, 'bold'})
            pen2.clear()
            pen2.write('最高得分：%d' % score_high, align='right',
                       font={"Arial", 20, 'bold'})

    elif state_index == 2:
        # 游戏失败
        screen.bgpic(fail_pic)
        screen.update()
    sleep(0.015)

mainloop()
