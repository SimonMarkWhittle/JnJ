import random


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
        self.branch = Branch(obj["branch"])

        if Event.next_id <= self.id:
            Event.next_id = self.id + 1

        if Event.retrieve_event(self.id):
            raise Exception("Duplicate Event IDs")

        Event.events[self.id] = self

    @staticmethod
    def retrieve_event(event_id):
        return Event.events.get(event_id)
    
    @staticmethod
    def find_event_with(tags):

        id_list = list(self.events.keys())

        event_id = random.choice(id_list)
        event = Event.retrieve_event(event_id)

        return event


class EventGenerator():
    def __init__(self):
        self.event_tags = []
        self.state = "ba"
    
    def gen_event(self):
        num_tags = random.randint(2, len(self.event_tags))
        tags = random.sample(self.event_tags, num_tags)

        event = Event.find_event_with(tags)

        if not event:
            raise Exception("Invalid event ID")

        while event:
            event = event.activate(self)

    def do_stuff(self):
        print("stuff happened to gen!")


