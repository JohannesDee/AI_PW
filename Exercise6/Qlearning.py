import numpy as np
import random
import gym

def qlearn():

    # create Taxi environment
    env = gym.make('CarRacing-v1')

    # initialize q-table
    state_size = 96*96 #env.observation_space.n
    action_size = 3# env.action_space.n
    qtable = np.zeros((state_size, action_size))

    # hyperparameters
    learning_rate = 0.9
    discount_rate = 0.8
    epsilon = 1.0
    decay_rate= 0.005

    # training variables
    num_episodes = 10
    max_steps = 999 # per episode

    # training
    for episode in range(num_episodes):
        print(episode)
        # reset the environment
        state = env.reset()
        done = False

        for s in range(max_steps):

            # exploration-exploitation tradeoff
            if random.uniform(0,1) < epsilon:
                # explore
                action = np.zeros(3)
               # print(type(action))
                action_ind = random.randrange(0, 3)
                if action_ind == 0:
                    action[0] = random.randrange(-1, 1, 2)
                else:
                    action[action_ind] = 1

            else:
                # exploit
                action = np.argmax(qtable[state, :])
                if action.size != 3:
                    action = env.action_space.sample()

            # take action and observe reward
            new_state, reward, done, info = env.step(action)

            # Q-learning algorithm
            qtable[state,action_ind] = qtable[state,action_ind] + learning_rate * (reward + discount_rate * np.max(qtable[new_state,:])-qtable[state,action_ind])

            # Update to our new state
            state = new_state

            # if done, finish episode
            if done == True:
                break

        # Decrease epsilon
        epsilon = np.exp(-decay_rate*episode)

    print(f"Training completed over {num_episodes} episodes")
    input("Press Enter to watch trained agent...")

    # watch trained agent
    state = env.reset()
    done = False
    rewards = 0

    for s in range(max_steps):

        print(f"TRAINED AGENT")
        print("Step {}".format(s+1))

        action = np.argmax(qtable[state,:])
        if action.size != 3:
            action = env.action_space.sample()
        print(action)
        new_state, reward, done, info = env.step(action)
        rewards += reward
        env.render()
        print(f"score: {rewards}")
        state = new_state

        if done == True:
            break

    env.close()
