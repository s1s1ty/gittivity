import os
import platform
import subprocess
from time import sleep

import requests
from pyjsonq import JsonQ

is_mac = platform.uname().system.lower() == 'darwin'
is_win = platform.uname().system.lower() == 'windows'
if is_mac:
    from pync import notify as mac_notify
if is_win:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()

github_handle = None
notify_status = None
title = 'gittivity'


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
        "* To start command `gittivity-start`\n"
        "* To stop command `gittivity-stop`\n"
        "* To config command `gittivity-config`\n"
        "* To get hint command `gittivity` for instruction\n"
    )


def configure():
    """Set configuration"""
    global github_handle, notify_status
    github_handle = input("Your github handle: ")
    notify_status = input("Do you want only your repo status(y/n): ")
    start()


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
                        notify(msg, repo_link)
                else:
                    notify(msg, repo_link)

                old_notify_time = new_notify_time
                sleep(5)

    return old_notify_time


def notify(msg, link=None):
    """Platform agnostic notifier"""
    if is_mac:
        mac_notify(msg, title=title, open=link)
    elif is_win:
        toaster.show_toast(title, msg)
    else:
        subprocess.run(['notify-send', title, msg])


def start():
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
            notify(str(e))

        sleep(5 * 60)


def stop():
    """Stop gittivity"""
    os.system("pkill -9 -f gittivity")


def main():
    """Entry point"""
    global github_handle
    if github_handle:
        start()
    else:
        configure()
