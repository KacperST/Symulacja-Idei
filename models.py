from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import random
from agents import MajorityRuleAgent
import matplotlib.pyplot as plt
import abc


class BaseModel(abc.ABC):

    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def is_stable(self):
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

        # Przygotuj opinie zgodnie z parametrem initial_ratio
        num_positive = int(initial_ratio * num_agents)
        opinions = [1] * num_positive + [-1] * (num_agents - num_positive)
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

        if self.is_stable():
            print("Symulacja osiągnęła stabilność.")
            self.running = False

    def is_stable(self):
        opinions = [agent.opinion for agent in self.agents]
        return len(set(opinions)) == 1


class QVoteModel(Model, BaseModel):

    def __init__(self):
        # TODO: Implement QVoteModel
        pass

    def step(self):
        # TODO: Implement the step method for QVoteModel
        pass

    def is_stable(self):
        # TODO: Implement the is_stable method for QVoteModel
        pass