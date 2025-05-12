from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from models.BaseModel import BaseModel
from mesa import Agent
from mesa import Model
import networkx as nx
import random


class QVoteAgent(Agent):

    def __init__(self, model, opinion):

        super().__init__(model)
        self.opinion = opinion

    def step(self):
        pass


class QVoterModel(Model, BaseModel):

    def __init__(self,
                 number_of_agents: int = 200,
                 group_size: int = 5,
                 flipping_probability: float = 0.5,
                 q_parameter: int = 3,
                 initial_ratio: float = 0.5) -> None:

        Model.__init__(self)

        # Main parameters
        self.flipping_probability: float = flipping_probability
        self.number_of_agents: int = number_of_agents
        self.initial_ratio: float = initial_ratio
        self.q_parameter: int = q_parameter
        self.group_size: int = group_size

        # Population initialisation
        self._initialize_population()


    def step(self) -> None:

        # Select a random agent...
        main_agent = random.choice(list(self.agents))

        # and random q of his neighbours...
        neighbors = self.grid.get_neighbors(main_agent.pos)
        neighbors = random.sample(neighbors, self.q_parameter)

        # to let the initial random agent adapt to their opinion, ...
        if self._is_unanimous(neighbors):
            main_agent.opinion = neighbors[0].opinion

        # unless they are not unanimous
        else:
            main_agent.opinion = random.choices(
                population = [1, -1],
                weights = [self.flipping_probability, 1 - self.flipping_probability],
                k = 1
            )[0]

        self.datacollector.collect(self)
        self.running = not self.is_unanimous()


    def is_unanimous(self) -> bool:
        return self._is_unanimous(self.agents)


    def _initialize_population(self) -> None:

        # Create a fully connected graph, ...
        self.G = nx.complete_graph(n = self.number_of_agents)
        self.grid = NetworkGrid(self.G)
        self.datacollector = DataCollector(agent_reporters = {"Opinion": "opinion"})

        # randomize opinions, ...
        number_of_positive = int(self.initial_ratio * self.number_of_agents)
        opinions = [1] * number_of_positive + [-1] * (self.number_of_agents - number_of_positive)
        self.random.shuffle(opinions)

        # and add randomised agents to the graph.
        for node, opinion in zip(self.G.nodes(), opinions):
            agent = QVoteAgent(self, opinion)
            self.agents.add(agent)
            self.grid.place_agent(agent, node)


    @staticmethod
    def _is_unanimous(group) -> bool:

        # Check if all agents have the same opinion on the matter.
        return all(agent.opinion == group[0].opinion for agent in group)
