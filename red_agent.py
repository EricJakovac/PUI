from config import ASCII_TILES  # Import the ASCII_TILES dictionary
from movement import Movement
from shooting import Shooting
import random
import heapq

class Agent:
    
    def __init__(self, color, index):
        self.color = color  # "blue" or "red"
        self.index = index  # 0, 1, or 2
        self.prev_direction = None
        self.prev_position = None
        self.stuck_count = 0
        self.movement = Movement(color)
        self.enemy_location = None
        self.flag_location = None
        self.shooting = Shooting()
        self.starting_position = None
        self.explored_positions = set()
        self.has_flag = False

    def update(self, visible_world, position, can_shoot, holding_flag):
        """
        Decide the agent's action and direction every frame.
        """
        action = "move"
        direction = "left"

        if self.index == 0:  # 1st agent moves normally
            if self.starting_position is None:
                self.starting_position = position

            if self.has_flag:
                # Use A* algorithm to find the shortest path to the goal
                open_list = []
                closed_list = set()
                heapq.heappush(open_list, (0, position))
                came_from = {}
                cost_so_far = {position: 0}

                while open_list:
                    current = heapq.heappop(open_list)[1]
                    if current == self.starting_position:
                        break

                    for neighbor in self.get_neighbors(visible_world, current):
                        new_cost = cost_so_far[current] + 1
                        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                            cost_so_far[neighbor] = new_cost
                            priority = new_cost + self.heuristic(neighbor, self.starting_position)
                            heapq.heappush(open_list, (priority, neighbor))
                            came_from[neighbor] = current

                # Reconstruct the path
                current = self.starting_position
                path = []
                while current != position:
                    path.append(current)
                    current = came_from[current]
                path.append(position)
                path.reverse()

                # Follow the path
                direction = self.get_direction(path[0], path[1])
            else:
                if self.prev_direction == "left" and random.random() < 0.9:  # 90% chance of continuing to move left
                    direction = "left"
                elif self.prev_direction == "left" and random.random() < 0.1:  # 10% chance of moving up or down
                    if random.random() < 0.5:  # 50% chance of moving up
                        direction = "up"
                    else:  # 50% chance of moving down
                        direction = "down"
                else:
                    if random.random() < 0.5:  # 50% chance of moving up
                        direction = "up"
                    else:  # 50% chance of moving down
                        direction = "down"

                # Check if the agent is about to hit a wall
                x = position[0]
                y = position[1]
                if   direction == "right" and x + 1 >= len(visible_world[0]):
                    direction = "left"
                elif direction == "left" and x - 1 < 0:
                    direction = "right"
                elif direction == "up" and y - 1 < 0:
                    direction = "down"
                elif direction == "down" and y + 1 >= len(visible_world):
                    direction = "up"

                # Check if the agent is in a corner
                if (direction == "left" and x - 1 < 0) or (direction == "right" and x + 1 >= len(visible_world[0])):
                    if (direction == "up" and y - 1 < 0) or (direction == "down" and y + 1 >= len(visible_world)):
                        # If the agent is in a corner, move back to the first position
                        direction = "stay"
                        self.prev_direction = None

                # Check if the agent is stuck in a loop
                if self.prev_position == position:
                    self.stuck_count += 1
                    if self.stuck_count > 5:
                        # If the agent is stuck, try a different path
                        direction = random.choice(["right", "left", "up", "down"])
                        self.prev_direction = direction
                        self.stuck_count = 0
                        self.retrace_steps(visible_world, position)
                else:
                    self.stuck_count = 0

                # Check if the agent is surrounded by walls on three sides
                if (direction == "left" and x - 1 < 0) and (direction == "right" and x + 1 >= len(visible_world[0])):
                    if (direction == "up" and y - 1 < 0) or (direction == "down" and y + 1 >= len(visible_world)):
                        # If the agent is surrounded by walls on three sides, try to move up or down
                        if random.random() < 0.5:  # 50% chance of moving up
                            direction = "up"
                        else:  # 50% chance of moving down
                            direction = "down"

                # Check if the agent can move up or down
                if len(visible_world) > 0 and len(visible_world[0]) > 0:
                    if y - 1 >= 0 and y - 1 < len(visible_world) and x < len(visible_world[0]) and visible_world[y - 1][x] not in [ASCII_TILES["wall"]]:
                        if random.random() < 0.5:  # 50% chance of moving up
                            direction = "up"
                    if y + 1 < len(visible_world) and x < len(visible_world[0]) and visible_world[y + 1][x] not in [ASCII_TILES["wall"]]:
                        if random.random() < 0.5:  # 50% chance of moving down
                            direction = "down"

                # Check if the agent has already explored this position
                if position in self.explored_positions:
                    # If the agent has already explored this position, try a different path
                    direction = random.choice(["right", "left", "up", "down"])
                    self.prev_direction = direction

                # Add the current position to the explored positions
                self.explored_positions.add(position)
                

        elif self.index == 1 or self.index == 2:  # 2nd and 3rd agents stay at the flag and protect it
            action = "shoot"
            direction = random.choice(["right", "left", "up", "down"])

            # Check if there is an enemy agent in the visible world
            for y in range(len(visible_world)):
                for x in range(len(visible_world[0])):
                    if visible_world[y][x] == 'b':
                        # If there is an enemy agent, shoot at it
                        direction = self.get_direction(position, (x, y))
                        break

        self.prev_position = position
        self.prev_direction = direction
        
        return action, direction

    def retrace_steps(self, visible_world, position):
        """
        Retrace the agent's steps to the starting position.
        """
        action = "move"
        direction = "stay"
        
        x, y = position
        while (x, y) != self.starting_position:
            if x > self.starting_position[0]:
                x -= 1
            elif x < self.starting_position[0]:
                x += 1
            elif y > self.starting_position[1]:
                y -= 1
            elif y < self.starting_position[1]:
                y += 1
            position = (x, y)
            self.prev_position = position

        return action, direction

    def get_neighbors(self, visible_world, position):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < len(visible_world[0]) and 0 <= y < len(visible_world):
                neighbors.append((x, y))
        return neighbors

    def heuristic(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def get_direction(self, position1, position2):
        dx = position2[0] - position1[0]
        dy = position2[1] - position1[1]
        if dx > 0:
            return "right"
        elif dx < 0:
            return "left"
        elif dy > 0:
            return "down"
        elif dy < 0:
            return "up"

    def terminate(self, reason):
        if reason == "died":
            self.has_flag = False  # Reset flag status if the agent dies
            print(self.color, self.index, "died")
        else:
            print(self.color, self.index, "terminated due to:", reason)