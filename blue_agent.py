import random
from queue import PriorityQueue

from config import *


class Agent:
    def __init__(self, color, index):
        self.color = color  # "blue" or "red"
        self.index = index  # 0, 1, or 2
        self.enemy_color = "r" if color == "blue" else "b"
        self.enemy_flag = "}" if color == "blue" else "{"
        self.role = self.assign_role()
        self.waiting_to_shoot = False  # Dodano za kontrolu čekanja pucanja

    def assign_role(self):
        if self.index in [0, 1]:
            return "attacker"
        else:
            return "defender"

    def find_enemy_direction(self, visible_world):
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        center_x, center_y = len(visible_world) // 2, len(visible_world[0]) // 2
        for direction, (dx, dy) in directions.items():
            for i in range(1, 5):
                x, y = center_x + dx * i, center_y + dy * i
                if 0 <= x < len(visible_world) and 0 <= y < len(visible_world[0]):
                    tile = visible_world[x][y]
                    if tile in [self.enemy_color, self.enemy_color.upper()]:
                        print(f"[DEBUG] Agent {self.color}-{self.index} vidi neprijatelja na {direction}.")
                        return direction
        return None

    def find_unexplored_direction(self, visible_world):
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        center_x, center_y = len(visible_world) // 2, len(visible_world[0]) // 2
        unexplored = []
        for direction, (dx, dy) in directions.items():
            x, y = center_x + dx, center_y + dy
            if 0 <= x < len(visible_world) and 0 <= y < len(visible_world[0]):
                if visible_world[x][y] == " ":
                    unexplored.append(direction)
        return random.choice(unexplored) if unexplored else None

    def a_star_pathfinding(self, visible_world, target_tile):
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        center_x, center_y = len(visible_world) // 2, len(visible_world[0]) // 2
        open_set = PriorityQueue()
        open_set.put((0, (center_x, center_y)))
        came_from = {}
        g_score = {(center_x, center_y): 0}
        f_score = {(center_x, center_y): 0}

        while not open_set.empty():
            _, current = open_set.get()

            if visible_world[current[0]][current[1]] == target_tile:
                path = []
                while current in came_from:
                    prev, move = came_from[current]
                    path.append(move)
                    current = prev
                return path[-1] if path else None

            for direction, (dx, dy) in directions.items():
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < len(visible_world) and 0 <= neighbor[1] < len(visible_world[0]):
                    if visible_world[neighbor[0]][neighbor[1]] != "#":
                        tentative_g_score = g_score[current] + 1
                        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = (current, direction)
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = tentative_g_score
                            open_set.put((f_score[neighbor], neighbor))
        return None

    def update(self, visible_world, position, can_shoot, holding_flag):
        enemy_direction = self.find_enemy_direction(visible_world)
        if enemy_direction and can_shoot:
            print(f"[DEBUG] Agent {self.color}-{self.index} PUCANJE prema {enemy_direction}.")
            return "shoot", enemy_direction

        if self.role == "attacker":
            target_tile = self.enemy_flag if not holding_flag else "*"
            path_direction = self.a_star_pathfinding(visible_world, target_tile)
            if not path_direction:
                # Ako nema puta do cilja, traži neistražena područja
                path_direction = self.find_unexplored_direction(visible_world)
                if not path_direction:
                    # Ako nema neistraženih, nasumično odaberi smjer
                    path_direction = random.choice(["up", "down", "left", "right"])
        else:
            target_tile = "{" if self.color == "red" else "}"
            path_direction = self.a_star_pathfinding(visible_world, target_tile)

        if path_direction:
            print(f"[DEBUG] Agent {self.color}-{self.index} ({self.role}) kreće prema {target_tile} putem {path_direction}.")
            return "move", path_direction

        directions = ["left", "right", "up", "down"]
        return "move", random.choice(directions)

    def terminate(self, reason):
        if reason == "died":
            print(f"[DEBUG] Agent {self.color}-{self.index} ({self.role}) je umro.")
