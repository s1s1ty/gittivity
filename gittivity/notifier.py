import os
import argparse
from time import sleep

import requests
from pync import notify
from pyjsonq import JsonQ

github_handle = None
notify_status = None


def _match(property):
    """Triggered for match event type
    :@param property: string
    :@return event_type: string
    """
    event_mapper = {
        "ForkEvent": "forked",
        "WatchEvent": "starred",  # I am guessing it's a typo. When user starred a repo. There is already an event for created!
        "CheckRunEvent": "checked run",
        "CommitCommentEvent": "committed comment",
        "CreateEvent": "created",
        "DeleteEvent": "deleted",
        "ForkApplyEvent": "forked apply",
        "IssueCommentEvent": "issueed comment",
        "IssuesEvent": "iussue",
        "LabelEvent": "lebel",
        "MemberEvent": "member",
        "MembershipEvent": "membership",
        "MilestoneEvent": "milestone",
        "PullRequestEvent": "pulled a request",
        "PullRequestReviewEvent": "review pull request",
        "PullRequestReviewCommentEvent": "review & comment pull request",
        "RepositoryEvent": "repo",
        "PushEvent": "pushed",
        "RepositoryVulnerabilityAlertEvent": "repo sequirity",
        "TeamEvent": "team",
        "TeamAddEvent": "added team",
    }

    if property not in event_mapper:
        return ""

    return event_mapper.get(property)


def help_text():
    """Provide instruction about useage"""
    print(
        "Please follow the instruction\n"
        "* To start command `gittivity-start <your github_handle>`\n"
        "* To stop command `gittivity-stop`\n"
        "* To get hint command `gittivity` for instruction\n"
    )


def event_notifier(data, old_notify_time):
    """Triggered for checking notifications
    :@param data: dict/json
    :@param old_notify_time: string
    :@return string
    """
    events = []
    if old_notify_time:
        events = JsonQ(data=data).at(".")\
            .where("created_at", ">", old_notify_time)\
            .sort_by("created_at").get()
    else:
        events.append(data[0])

    if events:
        for event in events:
            event_type = event.get("type")

            new_notify_time = event.get("created_at")
            action = _match(event_type)

            if old_notify_time != new_notify_time and action:

                actor = event.get("actor").get("display_login")
                repo_name = event.get("repo").get("name")

                repo_link = "{}{}".format("https://github.com/", repo_name)
                msg = "{} {} {}".format(actor, action, repo_name)

                if (notify_status == 'y' or notify_status == 'yes'):
                    if actor == github_handle:
                        notify("", title=msg, open=repo_link)
                else:
                    notify("", title=msg, open=repo_link)

                old_notify_time = new_notify_time
                sleep(5)

    return old_notify_time


def start():
    # print("activity checking...")
    old_notify_time = ""

    while True:
        # print(datetime.now())
        try:
            handle_link = "{}{}{}".format(
                "https://api.github.com/users/",
                github_handle,
                "/received_events"
            )

            src = requests.get(handle_link)
            data = src.json()
            old_notify_time = event_notifier(data, old_notify_time)

        except Exception:
            pass

        sleep(3 * 60)


def stop():
    """Stop gittivity"""
    os.system("pkill -9 -f gittivity")


def main():
    """Entry point"""

    parser = argparse.ArgumentParser(description="Get user's github username.")
    parser.add_argument("github_handle", type=str, help="Type github username")
    parser.add_argument("notify_status", nargs='*', type=str, default='n', help="Do you want only your repo status(y/n)")
    args = parser.parse_args()

    global github_handle, notify_status
    github_handle = args.github_handle
    notify_status = args.notify_status

    start()
