from pyjsonq import JsonQ


class Manager(object):
    def __init__(self):
        self.event_mapper = {
            "ForkEvent": "fork_msg",
            "WatchEvent": "watch_msg",
            "CheckRunEvent": "check_run_msg",
            "CommitCommentEvent": "commit_comment_msg",
            "CreateEvent": "create_msg",
            "DeleteEvent": "delete_msg",
            "ForkApplyEvent": "fork_apply_msg",
            "IssueCommentEvent": "issue_comment_msg",
            "IssuesEvent": "iussue_msg",
            "LabelEvent": "lebel_msg",
            "MemberEvent": "member_msg",
            "MembershipEvent": "membership_msg",
            "MilestoneEvent": "milestone_msg",
            "PullRequestEvent": "pull_request_msg",
            "PullRequestReviewEvent": "pull_request_review_msg",
            "PullRequestReviewCommentEvent": "pull_request_review_comnt_msg",
            "RepositoryEvent": "repo_msg",
            "PushEvent": "push_msg",
            "RepositoryVulnerabilityAlertEvent": "repo_sequirity_msg",
            "TeamEvent": "team_msg",
            "TeamAddEvent": "team_add_msg",
        }

    def fork_msg(self, event_dict):
        """Triggered when a user forks a repository.
        """
        return "froked"

    def watch_msg(self, event_dict):
        """Triggered when a user star a repository.
        """
        return JsonQ(data=event_dict).at("payload.action").get()

    def _match(self, property, event_dict):
        """Triggered for match event type"""
        if property not in self.event_mapper:
            return ""

        func = getattr(self, self.event_mapper.get(property))
        return func(event_dict)
