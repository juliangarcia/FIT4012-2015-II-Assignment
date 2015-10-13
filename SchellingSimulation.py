import numpy as np
import itertools


class SimplifiedSchellingSimulation(object):
    """ A Schelling Simulation"""

    def __init__(self, state, cycle=False, mistake_probability=0.0):
        """
        Initializes the class.
        Cycle determines if agents live in a cycle or a simple linear graph
        """
        self.cycle = cycle
        self.size = len(state)
        self.state = state
        self.mistake_probability = mistake_probability
        # creates a list of all possible pairings
        self._matching_list = []
        for i in range(self.size):
            for j in range(i+1, self.size):
                self._matching_list.append((i, j))

    def _neighbour_left(self, state_list, index):
        if self.cycle is True:
            return state_list[index - 1]
        else:
            if index == 0:
                return None
            else:
                return state_list[index - 1]

    def _neighbour_right(self, state_list, index):
        if self.cycle is True:
            try:
                return state_list[index + 1]
            except IndexError:
                return state_list[0]
        else:
            if index == (len(state_list) - 1):
                return None
            else:
                return state_list[index + 1]

    def individual_happiness(self, state_list, index):
        return int((self._neighbour_right(state_list, index) == state_list[index]) or (
            self._neighbour_left(state_list, index) == state_list[index]))

    def happiness_in_current_state(self, i):
        return self.individual_happiness(self.state, i)

    def happiness_vector(self):
        ans = []
        for i in range(self.size):
            ans.append(self.happiness_in_current_state(i))
        return ans

    def happiness_aferswap(self, i, j):
        hypothetical = np.copy(self.state)
        hypothetical[i], hypothetical[j] = hypothetical[j], hypothetical[i]
        i_hypothetical_happiness = self.individual_happiness(hypothetical, j)
        j_hypothetical_happiness = self.individual_happiness(hypothetical, i)
        return i_hypothetical_happiness, j_hypothetical_happiness

    def swap(self, i, j):
        self.state[i], self.state[j] = self.state[j], self.state[i]

    def __two_random_indices(self):
        return self._matching_list[np.random.randint(len(self._matching_list))]

    def step(self):
        i, j = self.__two_random_indices()
        current_level = self.happiness_in_current_state(i) + self.happiness_in_current_state(j)
        after_swap = sum(self.happiness_aferswap(i, j))
        if after_swap > current_level:
            if np.random.binomial(1, 1.0 - self.mistake_probability):
                self.swap(i, j)
        else:
            if np.random.binomial(1, self.mistake_probability):
                self.swap(i, j)

    def is_current_state_absorbing(self):
        return sum(self.happiness_vector()) == self.size


###############################
# Estimating absorption times #
###############################

# Enumerate all transient states for a given size
def all_transient_states(size):
    # generate permutations from a basic template
    if size % 2 == 0:
        basic = (size//2)*[1] + (size//2)*[0]
    else:
        basic = (size//2)*[1] + (size//2)*[0] + [1]
    # create a set to store the permutations
    permutations = set()
    for i in itertools.permutations(basic):
        permutations.add(tuple(i))
    # the answer includes only states in which not all individuals are happy
    ans = []
    for i in permutations:
        if not SimplifiedSchellingSimulation(list(i), cycle=True, mistake_probability=0.0).is_current_state_absorbing():
            ans.append(list(i))
    return ans


def sample_absorption_time(list_of_possible_starting_states):
    # pick random starting state
    start = np.random.randint(0, len(list_of_possible_starting_states))
    # create a sim
    sim = SimplifiedSchellingSimulation(list(list_of_possible_starting_states[start]), cycle=True, mistake_probability=0.0)
    i = 0
    assert not sim.is_current_state_absorbing(), "Problem: {} is not absorbing".format(sim.state)
    while not sim.is_current_state_absorbing():
        sim.step()
        i += 1
    return i


def estimate_absorption_time(size, repetitions=1000):
    transient_states = all_transient_states(size)
    samples = []
    for _ in range(repetitions):
        samples.append(sample_absorption_time(transient_states))
    return np.average(samples)


def main():
     print(all_transient_states(5))


if __name__ == "__main__":
    main()
