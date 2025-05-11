from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import random
from agents import VoterAgent
import matplotlib.pyplot as plt


class VoterModel(Model):
    def __init__(self, num_agents=100, group_size=5):
        super().__init__()
        self.num_agents = num_agents
        self.group_size = group_size

        # Pełny graf: każdy z każdym
        self.G = nx.complete_graph(n=num_agents)
        self.grid = NetworkGrid(self.G)

        # DataCollector do zbierania danych
        self.datacollector = DataCollector(agent_reporters={"Opinion": "opinion"})

        for i, node in enumerate(self.G.nodes()):
            opinion = random.choice([-1, 1])
            agent = VoterAgent(self, opinion)
            self.agents.add(agent)
            self.grid.place_agent(agent, node)

    def step(self):
        # Majority Rule
        group = random.sample(list(self.agents), self.group_size)
        opinions = [agent.opinion for agent in group]
        majority_opinion = 1 if opinions.count(1) > opinions.count(-1) else -1

        for agent in group:
            agent.opinion = majority_opinion

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

