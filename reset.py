def resettable(f):

    def __init_and_copy__(self, *args):
        f(self, *args)
        self.__original_dict__ = copy.deepcopy(self.__dict__)

        def reset(o = self):
            o.__dict__ = o.__original_dict__

        self.reset = reset

    return __init_and_copy__

class Truel:
    @resettable
    def __init__(self, shooters, strategy, starter):
        self.hit_count = 0
        self.bullets_shot = 0
        self.shooters = shooters
        self.num_shooters = len(shooters)
        self.strategy = strategy
        self.first_shooter = starter #shooter object
        self.alive = shooters #list of shooter objects
        self.killed = [] #list of shooter objects
        self.bullet_results = [] #list of shooter objects
        self.results = [] #list of ints


class Shooter(object):
    @resettable
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# p = Point(1, 2)

# print p # 1 2

# p.x = 15
# p.y = 25

# print p # 15 25

# p.reset()

# print p # 1 2

# p2 = LabeledPoint(1, 2, "Test")

# print p2 # 1 2 (Test)

# p2.x = 3
# p2.label = "Test2"

# print p2 # 3 2 (Test2)

# p2.reset()

# print p2 # 1 2 (Test)
