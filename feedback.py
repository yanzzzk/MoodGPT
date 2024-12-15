import numpy as np

class RecommendationRLModel:
    def __init__(self):
        # Initialize Q-table as a dictionary for state-action mapping
        self.q_table = {}

    def update_q_value(self, state, action, reward, alpha=0.1, gamma=0.9):
        """
        Update Q-value for a given state-action pair using Q-learning.
        """
        if state not in self.q_table:
            self.q_table[state] = {}

        if action not in self.q_table[state]:
            self.q_table[state][action] = 0

        max_next_q_value = max(self.q_table[state].values(), default=0)
        self.q_table[state][action] += alpha * (reward + gamma * max_next_q_value - self.q_table[state][action])

    def get_best_action(self, state):
        """
        Get the best action for a given state.
        """
        if state not in self.q_table or not self.q_table[state]:
            return None
        return max(self.q_table[state], key=self.q_table[state].get)

    def save_model(self, filepath):
        """
        Save the Q-table to a .npy file.
        """
        np.save(filepath, self.q_table)

    def load_model(self, filepath):
        """
        Load the Q-table from a .npy file.
        """
        self.q_table = np.load(filepath, allow_pickle=True).item()
