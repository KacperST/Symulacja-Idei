from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import random
from agents import VoterAgent
import matplotlib.pyplot as plt


class VoterModel(Model):
    def __init__(self, num_agents=100, initial_ratio=0.5):
        super().__init__()
        self.num_agents = num_agents
        self.G = nx.complete_graph(n=num_agents)  # pełny graf
        self.grid = NetworkGrid(self.G)

        self.datacollector = DataCollector(
            agent_reporters={"Opinion": "opinion"}
        )

        # Przygotuj opinie zgodnie z parametrem initial_ratio
        num_positive = int(initial_ratio * num_agents)
        opinions = [1] * num_positive + [-1] * (num_agents - num_positive)
        self.random.shuffle(opinions)

        for node, opinion in zip(self.G.nodes(), opinions):
            agent = VoterAgent(self, opinion)
            self.agents.add(agent)
            self.grid.place_agent(agent, node)

    def step(self):
        self.agents.do("step")
        self.datacollector.collect(self)
        if self.is_stable():
            print("Symulacja osiągnęła stabilność.")
            self.running = False

    def is_stable(self):
        opinions = [agent.opinion for agent in self.agents]
        return len(set(opinions)) == 1

    def visualize_network(self):
        pos = nx.spring_layout(self.G)
        colors = ['red' if agent.opinion == 1 else 'blue' for agent in self.agents]
        nx.draw(self.G, pos, node_color=colors, with_labels=True, node_size=500, font_size=8)
        plt.title("Wizualizacja sieci agentów")
        plt.show()

