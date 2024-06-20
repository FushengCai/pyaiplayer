import time
import gzip
import collections

import keyboard
import gym
import numpy as np


class EnvironmentWrapper(gym.Wrapper):
    def __init__(self, env, model, reset_round=True, rendering=False):
        super(EnvironmentWrapper, self).__init__(env)
        self.env = env

        # Use a deque to store the last 9 frames
        self.num_frames = 9
        self.frame_stack = collections.deque(maxlen=self.num_frames)

        self.num_step_frames = 6

        self.reward_coeff = 3.0

        self.total_timesteps = 0

        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(100, 128, 3), dtype=np.uint8)

        self.reset_round = reset_round
        self.rendering = rendering

        self.model = model

    def _stack_observation(self):
        return np.stack([self.frame_stack[i * 3 + 2][:, :, i] for i in range(3)], axis=-1)

    def reset(self):
        observation = self.env.reset()

        self.total_timesteps = 0

        # Clear the frame stack and add the first observation [num_frames] times
        self.frame_stack.clear()
        for _ in range(self.num_frames):
            self.frame_stack.append(observation[::2, ::2, :])

        return np.stack([self.frame_stack[i * 3 + 2][:, :, i] for i in range(3)], axis=-1)

    def step(self, action):
        custom_done = False

        obs, _reward, _done, info = self.env.step(action)
        self.frame_stack.append(obs[::2, ::2, :])

        # Render the game if rendering flag is set to True.
        if self.rendering:
            self.env.render()
            time.sleep(0.01)

        for _ in range(self.num_step_frames - 1):
            # Keep the button pressed for (num_step_frames - 1) frames.
            obs, _reward, _done, info = self.env.step(action)
            self.frame_stack.append(obs[::2, ::2, :])
            if self.rendering:
                self.env.render()
                time.sleep(0.01)

        self.total_timesteps += self.num_step_frames

        # Max reward is 6 * full_hp = 1054 (damage * 3 + winning_reward * 3) norm_coefficient = 0.001
        return self._stack_observation(), 0, False, info  # reward normalization

    def close(self):
        self.env.close()

    """
    save current state, which can used in retro.make(state)
    """

    def save_state_to_file(self, name):
        content = self.env.em.get_state()
        with gzip.open(name, 'wb') as f:
            f.write(content)

    def play(self):
        obs = self.env.reset()
        while True:
            action_human = np.zeros(12)  # one player

            # Render the current frame
            # env.render()

            # action mapping      Player1
            # index=0, Strong K,    u
            # index=1, Light K,     i
            # index=2, ??,          o
            # index=3, START,       b
            # index=4, UP,          w
            # index=5, DOWN,        s
            # index=6, LEFT,        a
            # index=7, RIGHT,       d
            # index=8, ??,          n
            # index=9, L P,         l
            # index=10, M P,        k
            # index=11, S P,        j

            if keyboard.is_pressed('t'):
                print('T is pressed')
                self.save_state_to_file(self.env, 'saved_state.state')

            # player 1
            if keyboard.is_pressed('a'):
                print('LEFT is pressed')
                action_human[6] = 1
            if keyboard.is_pressed('d'):
                print('RIGHT is pressed')
                action_human[7] = 1
            if keyboard.is_pressed('w'):
                print('up is pressed')
                action_human[4] = 1
            if keyboard.is_pressed('s'):
                print('DOWN is pressed')
                action_human[5] = 1

            if keyboard.is_pressed('b'):
                print('b is pressed')
                action_human[3] = 1
            if keyboard.is_pressed('n'):
                print('n is pressed')
                action_human[8] = 1

            if keyboard.is_pressed('j'):
                print('j is pressed')
                action_human[11] = 1
            if keyboard.is_pressed('k'):
                print('k is pressed')
                action_human[10] = 1
            if keyboard.is_pressed('l'):
                print('l is pressed')
                action_human[9] = 1

            if keyboard.is_pressed('u'):
                print('u is pressed')
                action_human[0] = 1
            if keyboard.is_pressed('i'):
                print('i is pressed')
                action_human[1] = 1
            if keyboard.is_pressed('o'):
                print('o is pressed')
                action_human[2] = 1

            actionAI, _states = self.model.predict(obs)  # [0. 0. 0. 1. 0. 1. 1. 0. 1. 0. 1. 1.]
            print(actionAI)

            action = np.concatenate((action_human, actionAI))

            # Step through the environment with the chosen action
            observation, reward, done, info = self.env.step(action)
