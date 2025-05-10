from mesa import Agent

class VoterAgent(Agent):
    def __init__(self, model, opinion):
        super().__init__(model)
        self.opinion = opinion
        self.change_probability = 0.1

    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        if neighbors and self.random.random() < self.change_probability:
            neighbor_agent = self.random.choice(neighbors)
            neighbor_opinion = neighbor_agent.opinion
            self.opinion = neighbor_opinion
