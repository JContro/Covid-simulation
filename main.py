import numpy as np
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import time
import random


SIZE = 200
HM_EPISODES = 3
SIMULATION_DAYS = 20

d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)}  # GBR Colors of the player, food, and enemy


class Human:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
        self.sick = False
        self.days_sick = 0
        self.symptoms = False
        self.days_symptoms = 0
        self.times_tested = 0
        self.isolated = False
        self.immunity = False



    def __str__(self):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        # Get the distance between two humans
        return self.x - other.x, self.y - other.y

    def test(self):
        # return whether the human is sick
        return self.sick

    def isolate(self):
        # isolate the human
        self.isolated = True
        pass

    def infect(self):
        # test to see whether the person is already infected or immune
        if not self.sick and not self.immunity:
            self.sick = True

    def increase_sick_day(self):
        if self.sick:
            self.days_sick += 1
        # How do I choose whether the patient becomes sick?


def find_infected_humans(humans_dict):
    """
    Find the ids of the infected humans. This code will be inefficient as it loops over the humans multiple times,
    but for clarity I will keep it like this.
    :param humans_dict:
    :return:
    """
    infected_list = []
    for m in humans_dict.keys():
        if humans_dict[m].sick:
            infected_list.append(m)

    return infected_list


def find_neighbours(infected_list, humans_dict, distance):
    """
    Find the neighbours of each infected person and return their ids
    :param infected_list:
    :param humans_dict:
    :param distance:
    :return:
    """
    neighbours = []
    for infected in infected_list:
        for m in humans_dict.keys():
            distance_coord = humans_dict[infected] - humans_dict[m]
            d2 = distance_coord[0]**2 + distance_coord[1]**2
            if d2 < distance:
                neighbours.append(m)

    # Deduplicate the entries
    neighbours = list(set(neighbours))
    # take the already infected out of the
    return [x for x in neighbours if x not in infected_list]


def infect_neighbours(neighbours, humans, proba):
    for n in neighbours:
        if random.random() < proba:
            humans[n].infect()


def advance_sickness(infected_list, humans):
    for m in infected_list:
        humans[m].increase_sick_day()
        # TODO: add logic for symptoms and recovery
    return None


for episode in range(HM_EPISODES):
    humans = {}
    for i in [Human() for i in range(30)]:
        humans[id(i)] = i

    # Infect 2 people
    keys_list = list(humans.keys())
    random.shuffle(keys_list)
    shuffled_ids = keys_list[:2]

    for m in shuffled_ids:
        humans[m].infect()

    for d in range(SIMULATION_DAYS):
        infected_list = find_infected_humans(humans)
        advance_sickness(infected_list, humans)
        neighbours = find_neighbours(infected_list, humans, 1000)
        infect_neighbours(neighbours, humans, 0.01)


        pass
        """
        find the infected cases and +1 to their sickness days
        infect close people with a probability
        infect people 
        test people
        isolate them 
        save the stats
        """
