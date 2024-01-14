from dataclasses import dataclass

from documented import DocumentedError


@dataclass
class BranchNameError(DocumentedError):  # type: ignore
    """
    Current branch name is invalid.

        Branch: {self.branch}
        Required format:

            issue-ISSUE_ID-some_description-or_other

        where ISSUE_ID is an integer.
    """

    branch: str
