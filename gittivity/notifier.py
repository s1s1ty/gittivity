import sys
import os
import argparse
from time import sleep

import requests
from pync import notify
from pyjsonq import JsonQ


def _match(property):
    """Triggered for match event type
    :@param property: string
    :@return event_type: string
    """
    event_mapper = {
        "ForkEvent": "forked",
        "WatchEvent": "started",
        "CheckRunEvent": "check_run",
        "CommitCommentEvent": "commit_comment",
        "CreateEvent": "created",
        "DeleteEvent": "deleted",
        "ForkApplyEvent": "fork_apply",
        "IssueCommentEvent": "issue_comment",
        "IssuesEvent": "iussue",
        "LabelEvent": "lebel",
        "MemberEvent": "member",
        "MembershipEvent": "membership",
        "MilestoneEvent": "milestone",
        "PullRequestEvent": "pull_request",
        "PullRequestReviewEvent": "pull_request_review",
        "PullRequestReviewCommentEvent": "pull_request_review_comnt",
        "RepositoryEvent": "repo",
        "PushEvent": "pushed",
        "RepositoryVulnerabilityAlertEvent": "repo_sequirity",
        "TeamEvent": "team",
        "TeamAddEvent": "team_add",
    }

    if property not in event_mapper:
        return ""

    return event_mapper.get(property)


def help_text():
    """Provide instruction about useage"""
    print(
        "Please follow the instruction\n"
        "* Use argument `-c config` to config github handle\n"
        "* Use argument `-s start` to start application\n"
        "* Use argument `-k kill` to kill application\n"
        "* Use argument `-i hint` for instruction\n"
    )


def start():
    """Start gittivity"""
    main()


def stop():
    """Stop gittivity"""
    os.system("pkill -9 -f notifier.py")


def configure():
    with open("config.txt") as f:
        line = f.readline().split(":")
    return None if not line else line[1]


github_handle = configure()


def parse_arguments():
    """Return parsed argument"""
    parser = argparse.ArgumentParser(
        description='Github desktop notifier',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-s", "--start", type=str, help="start gittivity")
    parser.add_argument("-k", "--kill", type=str, help="stop gittivity")
    parser.add_argument("-c", "--config", type=str, help="configure git profile")
    parser.add_argument("-i", "--hint", type=str, help="provide instruction")

    return parser.parse_args()


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

                notify("", title=msg, open=repo_link)
                old_notify_time = new_notify_time
                sleep(5)

    return old_notify_time


def main():
    print("checking...")
    old_notify_time = ""

    while True:
        try:
            handle_link = "{}{}{}".format(
                "https://api.github.com/users/",
                github_handle,
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
    try:
        arg = parse_arguments()
        if arg.kill == "kill":
            stop()

        if arg.start == "start":
            if github_handle:
                start()
            else:
                print("Please configure first. See help `-i hint`")

        if arg.config == "config":
            if not github_handle:
                github_handle = input("Your github handle: ")
                with open("config.txt", "w") as text_file:
                    text_file.write("github_handle:{}".format(github_handle))
            start()

        if arg.hint == "hint":
            help_text()
    except:
        help_text()
