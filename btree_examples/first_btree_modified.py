import py_trees

# Shared blackboard
blackboard = py_trees.blackboard.Client(name="FruitState")
blackboard.register_key(key="has_apple", access=py_trees.common.Access.WRITE)
blackboard.register_key(key="has_pear", access=py_trees.common.Access.WRITE)

# Initial inventory
blackboard.has_apple = True
blackboard.has_pear = True


class HasApple(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name)

    def update(self):
        return (
            py_trees.common.Status.SUCCESS
            if blackboard.has_apple
            else py_trees.common.Status.FAILURE
        )


class EatApple(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name)

    def update(self):
        if blackboard.has_apple:
            print("Eating apple")
            blackboard.has_apple = False
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class HasPear(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name)

    def update(self):
        return (
            py_trees.common.Status.SUCCESS
            if blackboard.has_pear
            else py_trees.common.Status.FAILURE
        )


class EatPear(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name)

    def update(self):
        if blackboard.has_pear:
            print("Eating pear")
            blackboard.has_pear = False
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


# Build tree
has_apple = HasApple("Has apple")
eat_apple = EatApple("Eat apple")
sequence_1 = py_trees.composites.Sequence(name="Sequence 1", memory=True)
sequence_1.add_children([has_apple, eat_apple])

has_pear = HasPear("Has pear")
eat_pear = EatPear("Eat pear")
sequence_2 = py_trees.composites.Sequence(name="Sequence 2", memory=True)
sequence_2.add_children([has_pear, eat_pear])

root = py_trees.composites.Selector(name="Selector", memory=True)
root.add_children([sequence_1, sequence_2])

# Run tree
behavior_tree = py_trees.trees.BehaviourTree(root)
py_trees.logging.level = py_trees.logging.Level.DEBUG

for i in range(1, 4):
    print(f"\n------------------ Tick {i} ------------------")
    behavior_tree.tick()

