from Board import Connect4
from time import sleep
# from stable_baselines3 import A2C


env = Connect4()
env.reset()

for step in range(200):
    env.render()
    # take random action
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    print(reward)
    sleep(5)

    if terminated or truncated:
        break

