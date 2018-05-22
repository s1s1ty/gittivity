import requests
import argparse

from pync import notify
from pyjsonq import JsonQ

from manager import Manager

parser = argparse.ArgumentParser(description="Get user's github username.")
parser.add_argument("github_handle", type=str, help="Type github username")
args = parser.parse_args()


def main():
    try:
        old_notify_time = ""

        handle_link = "{}{}{}".format(
            "https://api.github.com/users/",
            args.github_handle,
            "/received_events"
        )
        print("checking...")

        while True:
            src = requests.get(handle_link)
            data = src.json()
            if data:
                event_dict = data[0]

                event_type = JsonQ(data=event_dict).at("type").get()

                new_notify_time = JsonQ(data=event_dict).at("created_at").get()
                action = Manager()._match(event_type, event_dict)

                if old_notify_time != new_notify_time and action:

                    actor = JsonQ(data=event_dict).at("actor.display_login").get()
                    repo_name = JsonQ(data=event_dict).at("repo.name").get()
                    repo_link = JsonQ(data=event_dict).at("repo.url").get()
                    msg = "{} {} {}".format(actor, action, repo_name)
                    notify("", title=msg, open=repo_link)
                    old_notify_time = new_notify_time

    except requests.exceptions.ConnectionError:
        print("connection issue")


if __name__ == '__main__':
    main()
