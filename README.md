# pyaiplayer
A tool to let human play game against AI model.

Today there are quite many python RL(reinforcement learning) models that can play arcade game, e.g. stree fighter. Models are trained in an internal environment, such as gym-retro environment, and it is not inter-actable (you cannot interact with the environment via your mouse or keyboard), which means human cannot play with/against the model you trained. It will be interesting and exciting that human can play with/against the model you trained, that's why I invented this library and share it with you guys.

You can refer to test_human_vs_ai.py which is an example for main function.

There are not too many code in this library, it is more like a reference, if you are trying to do similar thing, i.e. create a human vs AI inter-actable gym-retro environment.
You may find some answer when you encounter technical problems and difficulties.

API (very simple, just two lines):
env = EnvironmentWrapper(env, model)
#env is grm-retro environment, normally created by retro.make method.
#model is the model you trained.

# then, play
env.play()
# keyboard ASDW + jkluio + b (SELECT) + n(START)
# press t to save current state as file saved_state.state
# Force close the window whenever you want.