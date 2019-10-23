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
        print(self.text)
        input("[Press ENTER to continue]\n")

        roll = random.randint(1, 6)
        result = self.opts[str(roll)]

        print(f"{roll} : {result}")

        return result


class Event():
    next_id = 0
    events = {}

    def __init__(self, obj=None):
        self.text = ""
        self.title = ""
        self.tags = []
        self.branch = Branch()

        if not obj:
            self._gen_id()
        else:
            self._load_from(obj)

    def _gen_id(self):
        self.id = Event.next_id
        Event.next_id += 1
        Event.events[self.id] = self

    def activate(self, generator):
        print()
        print(self.title)
        print(self.text)
        generator.do_stuff()
        input("[Press ENTER to continue]\n")

        next_event_id = self.branch.resolve()

        if self.branch:
            return Event.retrieve_event(next_event_id)
        else:
            return False

    def _load_from(self, obj):
        self.id = obj["id"]
        self.text = obj["text"]
        self.title = obj["title"]
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
