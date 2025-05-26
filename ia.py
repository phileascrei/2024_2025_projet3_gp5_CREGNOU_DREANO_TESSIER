
import random
from collections import defaultdict

class FighterAI:
    def __init__(self, player):
        self.player = player
        self.q_table = {}
        self.actions = ["left", "right", "jump", "attack", "dodge", "idle"]
        self.last_state = None
        self.last_action = None

    def get_state(self, opponent):
        # Simplification de l'état pour le Q-learning
        state = (
            round((opponent.pos_x - self.player.pos_x) / 100),
            self.player.in_air,
            self.player.is_attacking,
            opponent.is_attacking,
            self.player.health // 10,
            opponent.health // 10
        )
        return state

    def choose_action(self, state, epsilon=0.1):
        if random.random() < epsilon or state not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get, default="idle")

    def update_q_table(self, reward, new_state):
        if self.last_state is None or self.last_action is None:
            return
        old_q = self.q_table.get(self.last_state, {}).get(self.last_action, 0)
        max_future_q = max(self.q_table.get(new_state, {}).values(), default=0)
        new_q = (1 - 0.1) * old_q + 0.1 * (reward + 0.95 * max_future_q)
        if self.last_state not in self.q_table:
            self.q_table[self.last_state] = {}
        self.q_table[self.last_state][self.last_action] = new_q

    def act(self, opponent, collision_rects):
        state = self.get_state(opponent)
        action = self.choose_action(state)
        self.last_state = state
        self.last_action = action
        self.perform_action(action, collision_rects)

    def perform_action(self, action, collision_rects):
        keys = {
        "left": self.player.left_key,
        "right": self.player.right_key,
        "jump": self.player.jump_key,
        "dodge": self.player.dodge_key,
        "attack": self.player.attack_key,
    }
        fake_touches = defaultdict(lambda: False)  # ← ne lève jamais d’erreur
        if action in keys:
            fake_touches[keys[action]] = True
        self.player.update(fake_touches, collision_rects)