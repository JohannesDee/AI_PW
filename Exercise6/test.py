import gym
import numpy as np
import random

env = gym.make('CarRacing-v1')
env.seed(42)
print(env.step(env.action_space.sample()))

state_size = env.observation_space
state_size = 96*96
action_size = env.action_space
action_size = 4

qtable = np.zeros((state_size, action_size))

# hyperparameters
learning_rate = 0.9
discount_rate = 0.8
epsilon = 1.0
decay_rate= 0.005

# training variables
num_episodes = 1000
max_steps = 99 # per episode
 # training
for episode in range(num_episodes):

        # reset the environment
        state = env.reset()
        done = False

        for s in range(max_steps):

            # exploration-exploitation tradeoff
            if random.uniform(0,1) < epsilon:
                # explore
               # action = env.action_space.sample()
                action = np.zeros(4)
                action[random.randrange(0,3)] = 1
            else:
                # exploit
                action = np.argmax(qtable[state,:])
                print("IN ELSE")
            #print(action)

            # take action and observe reward
            new_state, reward, done, info = env.step(action)
            # Q-learning algorithm
            ind = np.argmax(action)
            qtable[state,ind] = qtable[state,ind] + learning_rate * (reward + discount_rate * np.max(qtable[new_state,ind])-qtable[state,ind])

            # Update to our new state
            state = new_state

            # if done, finish episode
            if done == True:
                break

        # Decrease epsilon
        epsilon = np.exp(-decay_rate*episode)
print(qtable.shape)
print(f"Training completed over {num_episodes} episodes")
input("Press Enter to watch trained agent...")

# watch trained agent
state = env.reset()
print("state is: " , state)
done = False
rewards = 0

for s in range(max_steps):

    print(f"TRAINED AGENT")
    print("Step {}".format(s+1))

    action = np.argmax(qtable[state,:])
    print(action, qtable[state,:].shape)
    """
    if action[0] == 1:
        action = [1, action[2:3]]
    elif action[1] == 1:
        action = [-1, action[2:3]]
    else:
        action = [0, action[2:3]]

    print(action)
    """
    new_state, reward, done, info = env.step(action)
    rewards += reward
    env.render()
    print(f"score: {rewards}")
    state = new_state

    if done == True:
        break