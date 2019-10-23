import random, json
from event import Event

class State():
    def __init__(self, obj):
        self.id = ""
        self.title = ""
        self.steps = []

        if obj:
            self.id = obj["id"]
            self.title = obj["title"]
            self.steps = obj["steps"]


class EventGenerator():
    next_id = 0
    gens = { }

    def __init__(self, obj):

        self.tags = []
        self.title = ""
        self.text = ""
        self.state = "ba"

        if obj:
            self._load_from(obj)
        else:
            self._gen_id()

    def _load_from(self, obj):
        self.id = obj["id"]
        self.tags = obj["tags"]
        self.title = obj["title"]
        self.text = obj["text"]
        self.state = obj["state"]

        self.states = { state_obj["id"] : State(state_obj) for state_obj in obj["states"] }

        if type(self.id) is int and EventGenerator.next_id <= self.id:
            EventGenerator.next_id = self.id + 1

        if EventGenerator.retrieve_gen(self.id):
            raise Exception("Duplicate Event Generator IDs")

        EventGenerator.gens[self.id] = self

    def _gen_id(self):
        self.id = EventGenerator.next_id
        EventGenerator.next_id += 1
        EventGenerator.gens[self.id] = self

    def gen_event(self):
        print(self.title)
        print(self.text)

        num_tags = random.randint(2, len(self.tags))
        tags = random.sample(self.tags, num_tags)

        event = Event.find_event_with(tags)

        if not event:
            raise Exception("Invalid event ID")

        while event:
            event = event.activate(self)

        print("Gen Turn Done")

    def do_stuff(self):
        print("stuff happened to gen!")

    @staticmethod
    def initialize_gens_from(obj_list):
        for gen_obj in obj_list:
            EventGenerator(gen_obj)

    @staticmethod
    def retrieve_gen(gen_id):
        return EventGenerator.gens.get(gen_id)

    @staticmethod
    def random_generator():
        ids = list(EventGenerator.gens.keys())
        gen_id = random.choice(ids)

        gen = EventGenerator.retrieve_gen(gen_id)
        return gen
