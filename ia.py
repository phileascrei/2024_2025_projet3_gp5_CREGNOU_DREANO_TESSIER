import random
import math
from collections import defaultdict
from data import *

class FighterAI:
    def __init__(self, player):
        self.player = player
        self.actions = ["left", "right", "jump", "attack", "dodge", "idle"]
        self.q_table = defaultdict(lambda: {a: 0.0 for a in self.actions})
        self.last_state = None
        self.last_action = None
        self.learning_rate = 0.1
        self.discount = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

    def get_state(self, opponent):
        """Construit un état simplifié mais stratégique."""
        distance = round((opponent.pos_x - self.player.pos_x) / 50)
        opponent_direction = int(math.copysign(1, opponent.pos_x - self.player.pos_x))  # 1 si à droite, -1 si à gauche
        state = (
            distance,
            opponent_direction,
            int(self.player.in_air),
            int(opponent.in_air),
            int(self.player.is_attacking),
            int(opponent.is_attacking),
            self.player.health // 10,
            opponent.health // 10
        )
        return state

    def choose_action(self, state):
        """Choix d'action avec epsilon-greedy."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        action_values = self.q_table[state]
        return max(action_values, key=action_values.get)

    def update_q_table(self, reward, new_state):
        """Mise à jour de la Q-table selon la règle Q-learning."""
        if self.last_state is None or self.last_action is None:
            return

        old_q = self.q_table[self.last_state][self.last_action]
        future_q = max(self.q_table[new_state].values())
        new_q = (1 - self.learning_rate) * old_q + self.learning_rate * (reward + self.discount * future_q)

        self.q_table[self.last_state][self.last_action] = new_q

        # Réduction progressive de l'exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, opponent, collision_rects):
        """Choisit et effectue une action."""
        state = self.get_state(opponent)
        action = self.choose_action(state)

        # Mémorise la dernière décision
        self.last_state = state
        self.last_action = action

        self.perform_action(action, collision_rects)

        

    def reward_feedback(self, reward, opponent):
        """Appelé par l’environnement après une action pour donner un retour."""
        new_state = self.get_state(opponent)
        self.update_q_table(reward, new_state)

    def perform_action(self, action, collision_rects):
        keys = {
            "left": self.player.left_key,
            "right": self.player.right_key,
            "jump": self.player.jump_key,
            "dodge": self.player.dodge_key,
            "attack": self.player.attack_key,
        }
        fake_touches = defaultdict(lambda: False)
        if action in keys:
            fake_touches[keys[action]] = True
        self.player.update(fake_touches, collision_rects)

        # Empêche de sortir de la map
        if action == "left" and self.player.pos_x <= 0:
            return  # Ne fait rien
        elif action == "right" and self.player.pos_x + self.player.rect.width >= CONFIG["WINDOW_WIDTH"]:
            return  # Ne fait rien
