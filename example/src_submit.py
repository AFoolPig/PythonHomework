from math import sqrt

import cv2
from numpy import uint8, ones

KEY_R = ord('r')
KEY_P = ord('p')
KEY_Z = ord('z')
KEY_Y = ord('y')
KEY_C = ord('c')
KEY_Q = ord('q')

POLY_CLOSE_DIST = 50


def mouse_callback(event, x, y, _, __):
    if event == cv2.EVENT_LBUTTONUP:
        draw_click(x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        draw_move(x, y)


cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.resizeWindow('window', 1280, 720)
cv2.setMouseCallback('window', mouse_callback)

drawing_rect = False
drawing_rect_move = False
rect_points = []

drawing_poly = False
drawing_poly_move = False
poly_points = []
poly_will_close = False

origin_img = ones((2160, 3840, 3), uint8) * 128
img_before_draw = origin_img.copy()
img_drawing = None

op_seq = [(origin_img, None)]
current_op_seq_idx = 0

cv2.imshow('window', origin_img)


def main():
    while True:
        passed_key = cv2.waitKey(1)
        if passed_key == KEY_Q:
            break
        elif passed_key == KEY_R:
            start_draw_rect()
        elif passed_key == KEY_P:
            start_draw_poly()
        elif passed_key == KEY_Y:
            redo()
        elif passed_key == KEY_Z:
            undo()
        elif passed_key == KEY_C:
            clear()

    cv2.destroyAllWindows()


def redo():
    global current_op_seq_idx, img_before_draw
    if drawing_poly:
        reset_draw_poly()
    elif drawing_rect:
        reset_draw_rect()
    if current_op_seq_idx < len(op_seq) - 1:
        current_op_seq_idx += 1
        img_before_draw = op_seq[current_op_seq_idx][0]
        cv2.imshow('window', img_before_draw)
        img_before_draw = img_before_draw.copy()
    else:
        cv2.imshow('window', img_before_draw)


def undo():
    global current_op_seq_idx, img_before_draw
    if drawing_poly:
        reset_draw_poly()
    elif drawing_rect:
        reset_draw_rect()
    if current_op_seq_idx != 0:
        current_op_seq_idx -= 1
        img_before_draw = op_seq[current_op_seq_idx][0]
        cv2.imshow('window', img_before_draw)
        img_before_draw = img_before_draw.copy()
    else:
        cv2.imshow('window', img_before_draw)


def clear():
    global current_op_seq_idx, img_before_draw, op_seq
    if drawing_poly:
        reset_draw_poly()
    elif drawing_rect:
        reset_draw_rect()
    current_op_seq_idx = 0
    op_seq = op_seq[:1]
    img_before_draw = op_seq[0][0]
    cv2.imshow('window', img_before_draw)
    img_before_draw = img_before_draw.copy()


def start_draw_rect():
    global drawing_poly, drawing_rect
    global img_before_draw, img_drawing
    if drawing_rect:
        return
    elif drawing_poly:
        reset_draw_poly()
    img_drawing = img_before_draw.copy()
    cv2.putText(img_drawing, 'R', (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, [255, 0, 0], 6)
    cv2.imshow('window', img_drawing)
    drawing_rect = True


def start_draw_poly():
    global drawing_poly, drawing_rect
    global img_before_draw, img_drawing
    if drawing_poly:
        return
    elif drawing_rect:
        reset_draw_rect()
    img_drawing = img_before_draw.copy()
    cv2.putText(img_drawing, 'P', (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, [255, 0, 0], 6)
    cv2.imshow('window', img_drawing)
    drawing_poly = True


def reset_draw_rect():
    global drawing_rect, drawing_rect_move, rect_points
    drawing_rect = False
    drawing_rect_move = False
    rect_points = []
    pass


def reset_draw_poly():
    global drawing_poly, drawing_poly_move, poly_points, poly_will_close
    drawing_poly = False
    drawing_poly_move = False
    poly_points = []
    poly_will_close = False
    pass


def draw_click(x, y):
    global drawing_rect, drawing_poly
    if drawing_rect:
        draw_click_rect(x, y)
    elif drawing_poly:
        draw_click_poly(x, y)
    pass


def draw_click_rect(x, y):
    global rect_points, drawing_rect, drawing_rect_move
    global op_seq, current_op_seq_idx
    global img_before_draw
    if len(rect_points) == 0:
        rect_points.append((x, y))
        drawing_rect_move = True
    else:
        drawing_rect = False
        drawing_rect_move = False
        rect_points.append((x, y))
        cv2.rectangle(img_before_draw, rect_points[0], rect_points[1], [255, 0, 0], 6)
        cv2.imshow('window', img_before_draw)

        if len(op_seq) != current_op_seq_idx + 1:
            op_seq = op_seq[:current_op_seq_idx + 1]
        op_seq.append((img_before_draw, rect_points))
        current_op_seq_idx += 1
        img_before_draw = img_before_draw.copy()

        rect_points = []


def draw_click_poly(x, y):
    global poly_points, drawing_poly, drawing_poly_move, poly_will_close
    global op_seq, current_op_seq_idx
    global img_before_draw, img_drawing
    if len(poly_points) == 0:
        poly_points.append((x, y))
        drawing_poly_move = True
        return
    if poly_will_close:
        drawing_poly = False
        drawing_poly_move = False
        poly_will_close = False
        for idx in range(len(poly_points)):
            cv2.line(img_before_draw, poly_points[idx - 1], poly_points[idx], [255, 0, 0], 6)
        cv2.imshow('window', img_before_draw)

        if len(op_seq) != current_op_seq_idx + 1:
            op_seq = op_seq[:current_op_seq_idx + 1]
        op_seq.append((img_before_draw, poly_points))
        current_op_seq_idx += 1
        img_before_draw = img_before_draw.copy()

        poly_points = []
    else:
        poly_points.append((x, y))
        cv2.line(img_drawing, poly_points[-2], poly_points[-1], [255, 0, 0], 6)
        cv2.imshow('window', img_drawing)
    pass


def draw_move(x, y):
    global drawing_rect, drawing_poly
    if drawing_rect:
        draw_move_rect(x, y)
    elif drawing_poly:
        draw_move_poly(x, y)
    pass


def draw_move_rect(x, y):
    global drawing_rect_move
    if not drawing_rect_move:
        return
    img = img_drawing.copy()
    cv2.rectangle(img, rect_points[0], (x, y), [255, 0, 0], 6)
    cv2.imshow('window', img)


def draw_move_poly(x, y):
    global drawing_poly_move, poly_will_close
    if not drawing_poly_move:
        return
    img = img_drawing.copy()
    cv2.line(img, poly_points[-1], (x, y), [255, 0, 0], 6)
    x_dist = poly_points[0][0] - x
    y_dist = poly_points[0][1] - y
    if sqrt(x_dist * x_dist + y_dist * y_dist) < POLY_CLOSE_DIST and len(poly_points) > 2:
        cv2.putText(img, 'close polygon', (110, 100), cv2.FONT_HERSHEY_COMPLEX, 2, [255, 0, 0], 6)
        poly_will_close = True
    else:
        poly_will_close = False

    cv2.imshow('window', img)


main()
pass
