import requests
import argparse
from time import sleep

from pync import notify
from pyjsonq import JsonQ

parser = argparse.ArgumentParser(description="Get user's github username.")
parser.add_argument("github_handle", type=str, help="Type github username")
args = parser.parse_args()


def _match(property):
    """Triggered for match event type"""
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
