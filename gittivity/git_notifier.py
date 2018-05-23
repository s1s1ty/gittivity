import requests
import argparse
from time import sleep

from pync import notify
from pyjsonq import JsonQ

from manager import Manager

parser = argparse.ArgumentParser(description="Get user's github username.")
parser.add_argument("github_handle", type=str, help="Type github username")
args = parser.parse_args()


def event_notifier(data, old_notify_time):
    events = []
    if old_notify_time:
        events = JsonQ(data=data).at(".")\
            .where("created_at", ">", old_notify_time)\
            .sort_by("created_at").get()
    else:
        events.append(data[0])

    if events:
        for event in events:
            event_type = JsonQ(data=event).at("type").get()

            new_notify_time = JsonQ(data=event).at("created_at").get()
            action = Manager()._match(event_type, event)

            if old_notify_time != new_notify_time and action:

                actor = JsonQ(data=event).at("actor.display_login").get()
                repo_name = JsonQ(data=event).at("repo.name").get()
                repo_link = JsonQ(data=event).at("repo.url").get()
                msg = "{} {} {}".format(actor, action, repo_name)
                notify("", title=msg, open=repo_link)
                old_notify_time = new_notify_time
                sleep(5)

    return old_notify_time


def main():
    old_notify_time = ""

    while True:
        print("checking...")
        try:
            handle_link = "{}{}{}".format(
                "https://api.github.com/users/",
                args.github_handle,
                "/received_events"
            )

            src = requests.get(handle_link)
            data = src.json()
            old_notify_time = event_notifier(data, old_notify_time)

        except Exception as e:
            print(e)
            notify("", title=e)

        sleep(5 * 60)


if __name__ == '__main__':
    main()
