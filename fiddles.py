import random, json


class Branch():

    def __init__(self, obj=None):
        self.text = ""
        self.opts = {}

        if obj:
            self.load_from(obj)

    def load_from(self, obj):
        try:
            self.text = obj["text"]
            self.opts = obj["opts"]
        except Exception as e:
            raise Exception(f"Invalid Branch serialization: {e}")

    def put(self, num, event):
        self.opts[str(num)] = event

    def resolve(self):
        roll = random.randint(1, 6)
        result = self.opts[str(roll)]
        return result


class Event():
    next_id = 0
    events = {}

    def __init__(self, obj=None):
        self.text = ""
        self.tags = []
        self.branch = Branch()

        if not obj:
            self._gen_id()
        else:
            self.load_from(obj)

    def _gen_id(self):
        self.id = Event.next_id
        Event.next_id += 1
        Event.events[self.id] = self

    def activate(self, generator):
        print(self.text)
        generator.do_stuff()
        input("[Press ENTER to continue]")

        next_event_id = self.branch.resolve()

        if self.branch:
            return Event.retrieve_event(next_event_id)
        else:
            return False

    def load_from(self, obj):
        self.id = obj["id"]
        self.text = obj["text"]
        self.tags = obj["tags"]
        self.branch = Branch(obj["branch"])

        if type(self.id) is int and Event.next_id <= self.id:
            Event.next_id = self.id + 1

        if Event.retrieve_event(self.id):
            raise Exception("Duplicate Event IDs")

        Event.events[self.id] = self

    def has(self, tag):
        return tag in self.tags

    @staticmethod
    def retrieve_event(event_id):
        return Event.events.get(event_id)
    
    @staticmethod
    def find_event_with(tags):

        id_list = list(Event.events.keys())

        candidates = []

        for event_id in id_list:
            event = Event.retrieve_event(event_id)

            tag_matches = [event.has(tag) for tag in tags]

            if all(tag_matches):
                candidates.append(event)

        event = random.choice(candidates)
        return event

    @staticmethod
    def initialize_events_from(obj_list):

        for event_obj in obj_list:
            Event(event_obj)

    @staticmethod
    def random_event():
        ids = list(Event.events.keys())
        event_id = random.choice(ids)

        event = Event.retrieve_event(event_id)
        return event


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
        self.state = "ba"

        if obj:
            self.id = obj["id"]
            self.tags = obj["tags"]
            self.title = obj["title"]
            self.state = obj["state"]

            self.states = { state_obj["id"] : State(state_obj) for state_obj in obj["states"] }

            if type(self.id) is int and EventGenerator.next_id <= self.id:
                EventGenerator.next_id = self.id + 1

            if EventGenerator.retrieve_gen(self.id):
                raise Exception("Duplicate Event Generator IDs")

            EventGenerator.gens[self.id] = self
        else:
            self._gen_id()

    def _gen_id(self):
        self.id = EventGenerator.next_id
        EventGenerator.next_id += 1
        EventGenerator.gens[self.id] = self

    def gen_event(self):
        num_tags = random.randint(2, len(self.tags))
        tags = random.sample(self.tags, num_tags)

        event = Event.find_event_with(tags)

        if not event:
            raise Exception("Invalid event ID")

        while event:
            event = event.activate(self)

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


def load_from_json():
    stuff = json.load(open("stuff.json", "r"))

    events_objs = stuff["events"]
    Event.initialize_events_from(events_objs)

    gen_objs = stuff["generators"]
    EventGenerator.initialize_gens_from(gen_objs)


def main():
    load_from_json()

    gen = EventGenerator.random_generator()

    print(gen)

    event = Event.random_event()

    print(event)



if __name__ == "__main__":
    main()
