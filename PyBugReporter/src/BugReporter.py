import asyncio
import sys
import traceback
from functools import wraps

from python_graphql_client import GraphqlClient

class BugReporter:
    """A class for catching exceptions and automatically creating issues on a GitHub repo.

    Attributes:
        githubKey (str): the key used to make bug reports to our github
        repoName (str): the name of the repository
        orgName (str): the name of the organization
        test (bool): whether to run in testing mode
    """

    def __init__(self, githubKey: str, repoName: str, orgName: str, test: bool = False):
        """Initializes the BugReporter class.

        Args:
            githubKey (str): the key used to make bug reports to our github
            repoName (str): the name of the repository
            orgName (str): the name of the organization
            test (bool, optional): whether to run in testing mode; Defaults to False.
        """
        self.githubKey = githubKey
        self.repoName = repoName
        self.orgName = orgName
        self.test = test

    def report(self) -> callable:
        """Decorator that catches exceptions and sends a bug report to the github repository.

        Returns:
            callable: the decorated function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self._handleError(e)
            return wrapper
        return decorator

    def _handleError(self, e: Exception):
        """Handles error by creating a bug report.

        Args:
            e (Exception): the exception that was raised

        Raises:
            e: the exception that was raised
        """
        exc_type = type(e).__name__
        tb = traceback.extract_tb(sys.exc_info()[2])
        function_name = tb[-1][2]

        # title for bug report
        title = f"{self.repoName} had a {exc_type} error with the {function_name} function"

        # description for bug report
        description = f'Type: {exc_type}\nError text: {e}\nFunction Name: {function_name}\n{traceback.format_exc()}'

        # Check if we need to send a bug report
        if not self.test:
            self._sendBugReport(title, description)

        print(title)
        print(description)
        raise e

    def _sendBugReport(self, errorTitle: str, errorMessage: str):
        """Sends a bug report to the Github repository.

        Args:
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """    
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.githubKey}"}

        # query variables
        repoId = self._getRepoId()
        bugLabel = "LA_kwDOJ3JPj88AAAABU1q15w"
        autoLabel = "LA_kwDOJ3JPj88AAAABU1q2DA"
        
        # Create new issue
        createIssue = """
            mutation createIssue($input: CreateIssueInput!) {
                createIssue(input: $input) {
                    issue {
                        title                
                        body
                        repository {
                            name
                        }
                        labels(first: 10) {
                            nodes {
                            name
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "input": {
                "repositoryId": repoId,
                "title": errorTitle,
                "body": errorMessage,
                "labelIds": [bugLabel, autoLabel]
            }
        }

        issueExists = self._checkIfIssueExists(errorTitle)

        if (issueExists == False):
            result = asyncio.run(client.execute_async(query=createIssue, variables=variables, headers=headers))
            print('\nThis error has been reported to the Tree Growth team.\n')
        else:
            print('\nOur team is already aware of this issue.\n')

    def _checkIfIssueExists(self, errorTitle: str) -> bool:
        """Checks if an issue already exists in the repository.

        Args:
            errorTitle (str): the title of the error

        Returns:
            bool: True if the issue exists, False if it does not
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.githubKey}"}

        # query variables
        autoLabel = "auto generated"

        # Query to return all issues with auto gen label
        findIssue = """
            query findIssue ($login: String = "", $name: String = "", $labels: [String!] = "") {
                organization(login: $login) {
                    repository(name: $name) {
                        issues(labels: $labels, first: 10, states: [OPEN]) {
                            nodes {
                                title,
                                state
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "login": self.orgName,
            "name": self.repoName,
            "labels": autoLabel,
        }

        result = asyncio.run(client.execute_async(query=findIssue, variables=variables, headers=headers))
        nodes = result['data']['organization']['repository']['issues']['nodes']

        index = 0
        issueExists = False

        while (len(nodes) > index) :
            title = nodes[index]['title']
            if (errorTitle == title) :
                issueExists = True
                break
            else:
                index += 1

        return issueExists

    def _getRepoId(self) -> str:
        """Gets the repository ID.

        Returns:
            str: the repository ID
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.githubKey}"}

        # query variables
        getID = """
            query getID($owner: String!, $name: String!) {
                repository(owner: $owner, name: $name) {
                    id
                }
            }
        """

        variables = {
            "owner": self.orgName,
            "name": self.repoName
        }

        repoID = asyncio.run(client.execute_async(query=getID, variables=variables, headers=headers))
        return repoID['data']['repository']['id']
