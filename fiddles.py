import random, json
from event_gen import EventGenerator
from event import Event


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


    gen.gen_event()



if __name__ == "__main__":
    main()
