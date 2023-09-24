from stable_baselines3.common.env_checker import check_env
from Board import Connect4


env = Connect4()
# It will check your custom environment and output additional warnings if needed
check_env(env)