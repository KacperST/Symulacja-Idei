from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import random
from agents import VoterAgent
import matplotlib.pyplot as plt


class VoterModel(Model):
    def __init__(self, num_agents=100):
        super().__init__()
        self.num_agents = num_agents
        self.G = nx.erdos_renyi_graph(n=num_agents, p=0.1)
        self.grid = NetworkGrid(self.G)
        
        # Inicjalizowanie DataCollector
        self.datacollector = DataCollector(
            agent_reporters={"Opinion": "opinion"}
        )
        
        for i, node in enumerate(self.G.nodes()):
            opinion = random.choice([-1, 1])  # Przypisanie losowej opinii
            agent = VoterAgent(self, opinion)
            self.agents.add(agent)
            self.grid.place_agent(agent, node)

    def step(self):
        self.agents.do("step")  # Przeprowadź krok dla każdego agenta
        self.datacollector.collect(self)  # Zbieranie danych
        if self.is_stable():  # Sprawdzamy, czy symulacja osiągnęła stabilność
            print("Symulacja osiągnęła stabilność.")
            self.running = False

    def is_stable(self):
        """Zatrzymuje symulację, jeśli wszystkie opinie są takie same."""
        opinions = [agent.opinion for agent in self.agents]
        return len(set(opinions)) == 1  # Wszystkie opinie muszą być takie same

    def visualize_network(self):
        """Wizualizacja sieci agentów."""
        pos = nx.spring_layout(self.G)  # Rozmieszczenie węzłów
        colors = ['red' if agent.opinion == 1 else 'blue' for agent in self.agents]  # Kolory węzłów zależnie od opinii
        nx.draw(self.G, pos, node_color=colors, with_labels=True, node_size=500, font_size=8)
        plt.title("Wizualizacja sieci agentów")
        plt.show()
