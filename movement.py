from config import ASCII_TILES  # Import the ASCII_TILES dictionary

class Movement:
    def __init__(self, color):
        self.color = color

    def upper_agent_move(self, visible_world, position):
        """
        Simplified movement logic for the upper agent:
        1. Move left.
        2. If left is blocked, move up.
        3. If both left and up are blocked, move down.
        4. If all directions are blocked, move back (right).
        """
        directions = ["left", "up", "down", "right"]
        for dir in directions:
            next_position = self.get_next_position(position, dir)
            if self.is_valid_move(visible_world, next_position):
                return dir
        return "stay"

    def get_next_position(self, position, direction):
        """
        Get the next position based on the current position and the direction.
        """
        dx, dy = 0, 0
        if direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        elif direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        
        return position[0] + dx, position[1] + dy

    def is_valid_move(self, visible_world, next_position):
        """
        Check if the move is valid (i.e., not blocked by a wall).
        """
        x, y = next_position
        if 0 <= x < len(visible_world) and 0 <= y < len(visible_world[0]):
            if visible_world[x][y] not in [ASCII_TILES["wall"]]:  # Blocked by walls or obstacles
                return True
        return False  # Out of bounds or blocked by wall

    def can_move_up_or_down(self, visible_world, position):
        """
        Check if the agent can move up or down.
        """
        x, y = position
        if y - 1 >= 0 and len(visible_world) > y - 1 and visible_world[x][y - 1] not in [ASCII_TILES["wall"]]:
            return True
        if y + 1 < len(visible_world) and len(visible_world) > y + 1 and visible_world[x][y + 1] not in [ASCII_TILES["wall"]]:
            return True
        return False