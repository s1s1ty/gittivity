# from pyjsonq import JsonQ


class Manager(object):
    def __init__(self):
        self.event_mapper = {
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

    # def fork_msg(self, event_dict):
    #     """Triggered when a user forks a repository.
    #     """
    #     return "froked"
    #
    # def watch_msg(self, event_dict):
    #     """Triggered when a user star a repository.
    #     """
    #     return JsonQ(data=event_dict).at("payload.action").get()

    def _match(self, property, event_dict):
        """Triggered for match event type"""
        if property not in self.event_mapper:
            return ""

        # func = getattr(self, self.event_mapper.get(property))
        return self.event_mapper.get(property)
        # return func(event_dict)
