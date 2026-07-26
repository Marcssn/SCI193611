import random

class Thing:
    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive

class Agent(Thing):
    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program:
            self.program = program

    def can_grab(self, thing):
        return False

class Environment:
    def __init__(self):
        self.things = []
        self.agents = []

    def object_at(self, location):
        return [thing for thing in self.things if getattr(thing, 'location', None) == location]

    def list_things_at(self, location, tclass=None):
        things = self.object_at(location)
        if tclass:
            return [thing for thing in things if isinstance(thing, tclass)]
        return things

    def add_thing(self, thing, location=None):
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            return
        thing.location = location
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def delete_thing(self, thing):
        if thing in self.things:
            self.things.remove(thing)
        if thing in self.agents:
            self.agents.remove(thing)

    def step(self):
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append(None)
            for agent, action in zip(self.agents, actions):
                self.execute_action(agent, action)

    def run(self, steps=1000):
        for _ in range(steps):
            if self.is_done():
                return
            self.step()

    def is_done(self):
        return not any(agent.is_alive() for agent in self.agents)

    def percept(self, agent):
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError

class Food(Thing):
    pass

class Water(Thing):
    pass

class Bump(Thing):
    pass

class Direction:
    R = "right"
    L = "left"
    U = "up"
    D = "down"

    def __init__(self, direction=None):
        self.direction = direction or self.R

    def __add__(self, heading):
        if heading == self.R:
            return Direction({self.R: self.D, self.D: self.L, self.L: self.U, self.U: self.R}[self.direction])
        elif heading == self.L:
            return Direction({self.R: self.U, self.U: self.L, self.L: self.D, self.D: self.R}[self.direction])
