import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from models import MajorityVoteModel

def run_simulation(num_agents, initial_ratio, num_steps, group_size):
    model = MajorityVoteModel(num_agents=num_agents, initial_ratio=initial_ratio, group_size=group_size)

    history_pos = []
    history_neg = []

    for _ in range(num_steps):
        model.step()
        opinions = [agent.opinion for agent in model.agents]
        history_pos.append(opinions.count(1))
        history_neg.append(opinions.count(-1))
        if model.running is False:
            break

    return history_pos, history_neg

def plot_results(history_pos, history_neg, group_size,initial_ratio, directory):
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.figure(figsize=(10, 5))
    plt.plot(history_pos, label='Opinie +1')
    plt.plot(history_neg, label='Opinie -1')
    plt.xlabel('Krok')
    plt.ylabel('Liczba agentów')
    plt.title(f'Ewolucja opinii w czasie dla rozmiaru grupy {group_size} i initial_ratio {initial_ratio}')
    plt.legend()
    plt.grid()
    filename = f'voter_model_{group_size}.png'
    plt.savefig(os.path.join(directory, filename))
    print("Zapisano wykres jako ", os.path.join(directory, filename))

def main():
    num_agents = 1000
    initial_ratio = [0.5, 0.6, 0.7, 0.8, 0.9]
    num_steps = 1000
    group_size = [3, 5, 9, 15, 31]

    for r in initial_ratio:
        for g in group_size:
            directory = f"results{r}/"
            print(f"Symulacja dla {num_agents} agentów, początkowy stosunek {r}, rozmiar grupy {g}")
            history_pos, history_neg = run_simulation(num_agents, r, num_steps, g)
            plot_results(history_pos, history_neg, g,r ,directory)

if __name__ == "__main__":
    main()