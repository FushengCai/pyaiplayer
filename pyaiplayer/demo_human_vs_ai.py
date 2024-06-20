import gzip
import os
import time

import numpy
import retro
import numpy as np
import keyboard
from stable_baselines3 import PPO

from EnvironmentWrapper import EnvironmentWrapper

# Load the desired game ROM
game = 'StreetFighterIISpecialChampionEdition-Genesis'
state = 'Champion.Level12.RyuVsBison'
RESET_ROUND = True  # Whether to reset the round when fight is over.
RENDERING = True  # Whether to render the game screen.

player_n = 2  # total players, including human and AI.
human_player_n = 1

# model dir
MODEL_DIR = r"trained_models/"

# model file name
MODEL_NAME = r"model_file"


env = retro.make(
    game=game,
    state=state,
    use_restricted_actions=retro.Actions.FILTERED,
    obs_type=retro.Observations.IMAGE,
    players=player_n
)

model = PPO.load(os.path.join(MODEL_DIR, MODEL_NAME))

env = EnvironmentWrapper(env, model)

# main function
env.play()

# keyboard aswd + jkluio + b (SELECT) + n(START)

# press t to save current state as file saved_state.state

# Force close the window whenever you want.
