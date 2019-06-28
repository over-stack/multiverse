from entity import Entity
from decoration import Decoration


class Environment:
    def __init__(self, bonus, conditions):
        self.bonus = bonus
        self.conditions = conditions

    def get_states(self):
        return list(self.bonus.keys())

    def apply(self, entity, objects_around, world_around):

        classes_count = dict(zip([value[1] for value in self.conditions.values()],
                                 [0] * len(self.conditions)))

        for obj in objects_around:
            if obj.family == 'tree':
                classes_count['tree'] += 1

            if obj.type == 'entity' and obj.id_ != entity.id_:
                classes_count['entity'] += 1
                if obj.family == entity.family:
                    classes_count['same'] += 1

        env_classes = list()
        if classes_count['tree'] > 4:
            env_classes.append('forest')
            print('forest')

        if classes_count['entity'] == 0:
            env_classes.append('alone')
            print('alone')

        if classes_count['same'] > 3:
            env_classes.append('support')

        if len(env_classes) != 0:
            entity.health_bonus = sum(
                [entity.priorities[name_class] * self.bonus[name_class]['health'] for name_class in env_classes])
            entity.strength_bonus = sum(
                [entity.priorities[name_class] * self.bonus[name_class]['strength'] for name_class in env_classes])
            entity.satiety_bonus = sum(
                [entity.priorities[name_class] * self.bonus[name_class]['satiety'] for name_class in env_classes])
