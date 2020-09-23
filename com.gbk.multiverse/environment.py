from entity import Entity
from decoration import Decoration


class Environment:
    def __init__(self):
        self.bonus = {'forest': {'health': 10, 'strength': 10, 'satiety': 10},
                      'alone': {'health': 10, 'strength': 10, 'satiety': 10},
                      'support': {'health': 10, 'strength': 10, 'satiety': 10}}

    def get_states(self):
        return list(self.bonus.keys())

    def apply(self, entity, objects_around):
        tree_count = 0
        entity_count = 0
        same_entity_count = 0

        for obj in objects_around:
            if obj.family == 'tree':
                tree_count += 1

            if obj.type_ == 'entity' and obj.id_ != entity.id_:
                entity_count += 1
                if obj.family == entity.family:
                    same_entity_count += 1

        active_states = set()

        if tree_count > 4:
            active_states.add('forest')

        if entity_count == 0:
            active_states.add('alone')

        if same_entity_count > 3:
            active_states.add('support')

        if len(active_states) != 0:
            entity.health_bonus = sum(
                [entity.priorities[state] * self.bonus[state]['health'] for state in active_states])
            entity.strength_bonus = sum(
                [entity.priorities[state] * self.bonus[state]['strength'] for state in active_states])
            entity.satiety_bonus = sum(
                [entity.priorities[state] * self.bonus[state]['satiety'] for state in active_states])