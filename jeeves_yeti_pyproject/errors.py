from dataclasses import dataclass

from documented import Documented, DocumentedError


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


class FlakeheavenIncompatible(Documented):
    """
    ⚠️ Skipping `flakeheaven` due to compatibility issues with Python 3.12+.

    See [flakeheaven/flakeheaven#173]({self.issue_url}).
    """

    issue_url = 'https://github.com/flakeheaven/flakeheaven/issues/173'
