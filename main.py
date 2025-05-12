from models.MajorityVoteModel import MajorityVoteModel
from models.QVoterModel import QVoterModel
from itertools import product
import matplotlib.pyplot as plt
import os


def run_model(model, number_of_iterations: int) -> tuple[list, list]:

    history_pos, history_neg = [], []

    for _ in range(number_of_iterations):
        model.step()
        opinions = [agent.opinion for agent in model.agents]
        history_pos.append(opinions.count(1))
        history_neg.append(opinions.count(-1))
        if not model.running: break

    return history_pos, history_neg


def generate_plot(model, number_of_iterations: int = 1000) -> None:

    if not os.path.exists("results"):
        os.makedirs("results")

    model_results_path = os.path.join(
        "results",
        f"{model.__class__.__name__}",
    )

    if not os.path.exists(model_results_path):
        os.makedirs(model_results_path)

    plot_path = os.path.join(
        model_results_path,
        f"model_{model.group_size}_{str(model.initial_ratio).replace('.', ',')}.png"
    )

    history_pos, history_neg = run_model(model, number_of_iterations)

    plt.figure(figsize = (10, 5))
    plt.plot(history_pos, label='Opinie +1')
    plt.plot(history_neg, label='Opinie -1')
    plt.xlabel('Krok')
    plt.ylabel('Liczba agentów')
    plt.title(f'Ewolucja opinii w czasie dla rozmiaru grupy {model.group_size} i initial_ratio {model.initial_ratio}')
    plt.legend()
    plt.grid()

    plt.savefig(plot_path)

    plt.clf()


def main():

    num_agents = 1000
    initial_ratio = [0.5, 0.75, 0.9]
    group_size = [3, 5, 10]
    num_steps = 1000

    for group_size, initial_ratio in product(group_size, initial_ratio):

        model = MajorityVoteModel(
            num_agents = num_agents,
            group_size = group_size,
            initial_ratio = initial_ratio
        )

        generate_plot(model, num_steps)

        model = QVoterModel(
            number_of_agents = num_agents,
            group_size = group_size,
            initial_ratio = initial_ratio
        )

        generate_plot(model, num_steps)

if __name__ == "__main__":
    main()
