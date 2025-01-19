class Shooting:
    def __init__(self):
        pass

    def shoot(self, direction):
        """
        Return the shooting vector based on the direction.
        """
        if direction == "right":
            return (1, 0)
        elif direction == "left":
            return (-1, 0)
        elif direction == "up":
            return (0, -1)
        elif direction == "down":
            return (0, 1)
