
import unittest
from SchellingSimulation import *


class SimplifiedSchellingTest(unittest.TestCase):
    """
    Test the SimplifiedSchellingSimulation class.
    """

    def testHappiness(self):
        state = [True, True, False, True, False]
        sim = SimplifiedSchellingSimulation(state, cycle=True, mistake_probability=0.0)
        self.assertEqual(sim.happiness_in_current_state(0), 1)
        self.assertEqual(sim.happiness_in_current_state(1), 1)
        self.assertEqual(sim.happiness_in_current_state(2), 0)
        self.assertEqual(sim.happiness_in_current_state(3), 0)
        self.assertEqual(sim.happiness_in_current_state(4), 0)
        sim = SimplifiedSchellingSimulation(state, cycle=False, mistake_probability=0.0)
        self.assertEqual(sim.happiness_in_current_state(0), 1)
        self.assertEqual(sim.happiness_in_current_state(1), 1)
        self.assertEqual(sim.happiness_in_current_state(2), 0)
        self.assertEqual(sim.happiness_in_current_state(3), 0)
        self.assertEqual(sim.happiness_in_current_state(4), 0)
        state = [True, True, True, True, True]
        sim = SimplifiedSchellingSimulation(state, cycle=True, mistake_probability=0.0)
        for i, _ in enumerate(state):
            self.assertEqual(sim.happiness_in_current_state(i), 1)
        state = [False, False, False, False, False]
        sim = SimplifiedSchellingSimulation(state, cycle=True, mistake_probability=0.0)
        for i, _ in enumerate(state):
            self.assertEqual(sim.happiness_in_current_state(i), 1)

    def testHypotheticalHappiness(self):
        state = [True, True, False, True, False]
        sim = SimplifiedSchellingSimulation(state, cycle=True, mistake_probability=0.0)

        # WITH CYCLE
        # [True, True, *False, *True, False] Original
        # [True, True, *True, *False, False] After
        self.assertEqual(sim.happiness_aferswap(2, 3), (1, 1))

        # [True, True, False, *True, *False] Original
        # [True, True, False, *False, *True] After
        self.assertEqual(sim.happiness_aferswap(3, 4), (1, 1))

        # NO CYCLE
        sim = SimplifiedSchellingSimulation(state, cycle=False, mistake_probability=0.0)
        # [True, True, False, *True, *False] Original
        # [True, True, False, *False, *True] After
        self.assertEqual(sim.happiness_aferswap(3, 4), (0, 1))


def main():
    unittest.main()


if __name__ == "main":
    main()






