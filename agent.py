from config import *  # contains, amongst other variables, `ASCII_TILES` (which will probably be useful here)

import random


class Agent:
    
    # called when this agent is instanced (at the beginning of the game)
    def __init__(self, color, index):
        self.color = color  # "blue" or "red"
        self.index = index  # 0, 1, or 2
    
    # called every "agent frame"
    def update(self, visible_world, position, can_shoot, holding_flag):
        # display one agent's vision:
        """if self.index == 0:
            print("\n===========================\n")
            for row in visible_world:
                print(" " + " ".join(row))"""
        
        ## below is a very random and extremely simple implementation for testing purposes
        
        if can_shoot:
            action = "shoot"
        elif random.random() > 0.3:
            action = ""  # do nothing
        else:
            action = "move"
            
        if self.color == "blue":
            preferred_direction = "right"
            if holding_flag:
                preferred_direction = "left"
        elif self.color == "red":
            preferred_direction = "left"
            if holding_flag:
                preferred_direction = "right"
        
       