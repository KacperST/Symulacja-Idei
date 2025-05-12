from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from models.BaseModel import BaseModel
from mesa import Model
from mesa import Agent
import networkx as nx
import random


class MajorityRuleAgent(Agent):

    def __init__(self, model, opinion):

        super().__init__(model)
        self.opinion = opinion


    def step(self):
        pass


class MajorityVoteModel(Model, BaseModel):

    def __init__(self, num_agents=200, initial_ratio=0.5, group_size=5):
        Model.__init__(self)
        self.num_agents = num_agents
        self.G = nx.complete_graph(n=num_agents)  # pełny graf
        self.grid = NetworkGrid(self.G)
        self.group_size = group_size
        self.datacollector = DataCollector(
            agent_reporters={"Opinion": "opinion"}
        )
        self.initial_ratio = initial_ratio

        # Przygotuj opinie zgodnie z parametrem initial_ratio
        num_positive = int(self.initial_ratio * self.num_agents)
        opinions = [1] * num_positive + [-1] * (self.num_agents - num_positive)
        self.random.shuffle(opinions)

        for node, opinion in zip(self.G.nodes(), opinions):
            agent = MajorityRuleAgent(self, opinion)
            self.agents.add(agent)
            self.grid.place_agent(agent, node)

    def step(self):
        # Majority Rule
        group = random.sample(list(self.agents), self.group_size )
        opinions = [agent.opinion for agent in group]
        majority_opinion = 1 if opinions.count(1) > opinions.count(-1) else -1

        for agent in group:
            agent.opinion = majority_opinion

        self.datacollector.collect(self)

        if self.is_unanimous():
            print("Symulacja osiągnęła stabilność.")
            self.running = False

    def is_unanimous(self):
        opinions = [agent.opinion for agent in self.agents]
        return len(set(opinions)) == 1