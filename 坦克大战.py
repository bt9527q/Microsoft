import pygame
from pygame.locals import *
import math
import random

def expand_battle_field():
    for row in small_battle_field:
        new_row = []
        for column in row:
            new_row.extend([column] * 2)
        battle_field.append(new_row)
        battle_field.append(new_row[:])

def area_conflict(area1, area2):
    for point1 in area1:
        if point1 in area2:
            return True
    return False

def draw_battle_field():
    global symbol_position
    global symbol_area
    for row_index in range(y_max):
        for column_index in range(x_max):
            if battle_field[row_index][column_index] == 1:
                # is a brick_wall
                screen.blit(brick_wall_img, (column_index * 30, row_index * 30))
            if battle_field[row_index][column_index] == 2:
                # is a cement_wall
                screen.blit(cement_wall_img, (column_index * 30, row_index * 30))
            if symbol_position != None:
                continue
            if battle_field[row_index][column_index] == 3:
                # is a symbol
                symbol_position = (column_index, row_index)
                symbol_area = (
                        (column_index, row_index),
                        (column_index + 1, row_index),
                        (column_index, row_index + 1),
                        (column_index + 1, row_index + 1))
    if game_over:
        screen.blit(symbol_destoryed_img, (symbol_position[0] * 30, symbol_position[1] * 30))
    else:
        screen.blit(symbol_img, (symbol_position[0] * 30, symbol_position[1] * 30))

def produce_enemy(time):
    global last_product
    global enemys_cur_number
    if last_product != -1 and time - last_product < enemys_product_interval:
        return
    index_e = random.randint(0, 1)
    conflict = False
    for point in tank.area:
        if point in enemy_init_area[index_e]:
            conflict = True
            break

    if not conflict:
        for enemy in enemys:
            for point_e in enemy.area:
                if point_e in enemy_init_area[index_e]:
                    conflict = True
                    break
            if conflict:
                break;

    if not conflict:
        enemys.append(Enemy(enemy_init_position[index_e]))
        last_product = time
        enemys_cur_number += 1
        return

    for point in tank.area:
        if point in enemy_init_area[1 - index_e]:
            return

    for enemy in enemys:
        for point_e in enemy.area:
            if point_e in enemy_init_area[1 - index_e]:
                return

    enemys.append(Enemy(enemy_init_position[1 - index_e]))
    last_product = time
    enemys_cur_number += 1

class ArmoredCar():
    def __init__(self, p_position, p_direction, p_image, p_fire_interval):
        self.position = p_position
        self.area = (
            (self.position[0], self.position[1])，
            (self.position[0] + 1, self.position[1])，
            (self.position[0], self.position[1] + 1),
            (self.position[0] + 1, self.position[1] + 1))
        self.direction = p_direction
        self.image = p_image 
        self.missiles = []

        self.destroyed = False

        self.last_fire = -1
        self.fire_interval = p_fire_interval 

    def draw(self):
        screen.blit(self.image, (self.position[0] * 30, self.position[1] * 30))

    def is_legal(self, new_area):
        for (x, y) in new_area:
            if x < 0 or y < 0 or x >= x_max or y >= y_max:
                return False
            if battle_field[y][x] != 0:
                return False

        for enemy in enemys:
            if enemy == self:
                continue
            if area_conflict(enemy.area, new_area):
                return False
        if isinstance(self, Enemy) and area_conflict(self.area, tank.area):
            return False

        return True

    def update(self):
        self.draw()
        index = 0
        for missile in self.missiles:
            if missile.update() == False:
                self.missiles.pop(index)
            index += 1

    def up(self):
        self.direction = 'U'
        if isinstance(self, Tank):
            self.image = tank_img_U
        else:
            self.image = enemy_img_U 
        new_position = (self.position[0], self.position[1] - 1)
        new_area = (
            (new_position[0], new_position[1]),
            (new_position[0] + 1, new_position[1]),
            (new_position[0], new_position[1] + 1),
            (new_position[0] + 1, new_position[1] + 1)
