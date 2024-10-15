import asyncio
import sys
import traceback
from functools import wraps

from python_graphql_client import GraphqlClient

class NotCreatedError(Exception):
    pass

class BugHandler:
    """A class for catching exceptions and automatically creating issues on a GitHub repo.

    Attributes:
        githubKey (str): the key used to make bug reports to our github
        repoName (str): the name of the repository
        orgName (str): the name of the organization
        test (bool): whether to run in testing mode
        extraInfo (bool): whether to include extra information in the bug report
        kwargs: extra info for the bug report
    """
    githubKey: str = ''
    repoName: str = ''
    orgName: str = ''
    test: bool = False

    @classmethod
    def setVars(cls, githubKey: str, repoName: str, orgName: str, test: bool) -> None:
        cls.githubKey = githubKey
        cls.repoName = repoName
        cls.orgName = orgName
        cls.test = test

class BugReporter:
    handlers: dict = {}
    extraInfo: bool = False
    repoName: str

    def __init__(self, repoName: str, extraInfo: bool, **kwargs) -> None:
        """Initializes the BugReporter class as a decorator.
        
        Args:
            extraInfo (bool): whether to include extra information in the bug report
            **kwargs: extra info for the bug report
        """
        self.repoName = repoName
        self.extraInfo = extraInfo
        self.kwargs = kwargs

    @classmethod
    def setVars(cls, githubKey: str, repoName: str, orgName: str, test: bool) -> None:
        """Sets the necessary variables to make bug reports.

        Args:
            githubKey (str): the key used to make bug reports to our github
            repoName (str): the name of the repository
            orgName (str): the name of the organization
            test (bool): whether to run in testing mode
        """
        cls.handlers[repoName] = BugHandler.setVars(githubKey, repoName, orgName, test)

    def __call__(self, func: callable) -> None:
        """Decorator that catches exceptions and sends a bug report to the github repository.

        Args:
            func (callable): the function to be decorated
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            """Wrapper function that catches exceptions and sends a bug report to the github repository.

            Args:
                *args: the arguments for the function
                **kwargs: the keyword arguments for the function
            """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self._handleError(e, *args, **kwargs)
        return wrapper

    def _handleError(self, e: Exception, *args, **kwargs) -> None:
        """Handles error by creating a bug report.

        Args:
            e (Exception): the exception that was raised

        Raises:
            e: the exception that was raised
        """
        excType = type(e).__name__
        tb = traceback.extract_tb(sys.exc_info()[2])
        functionName = tb[-1][2]

        # title for bug report
        title = f"{self.handlers[self.repoName].repoName} had a {excType} error with the {functionName} function"

        # description for bug report
        description = f'Type: {excType}\nError text: {e}\nFunction Name: {functionName}\n\n{traceback.format_exc()}'
        description += f"\nArguments: {args}\nKeyword Arguments: {kwargs}"
        if self.extraInfo:
            description += f"\nExtra Info: {self.kwargs}"

        # Check if we need to send a bug report
        if not self.handlers[self.repoName].test:
            self._sendBugReport(title, description)

        print(title)
        print(description)
        raise e

    def _sendBugReport(self, errorTitle: str, errorMessage: str) -> None:
        """Sends a bug report to the Github repository.

        Args:
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """    
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.handlers[self.repoName].githubKey}"}

        # query variables
        repoId = self._getRepoId(self.handlers[self.repoName])
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

        issueExists = self._checkIfIssueExists(self.handlers[self.repoName], errorTitle)

        if (issueExists == False):
            result = asyncio.run(client.execute_async(query=createIssue, variables=variables, headers=headers))
            print('\nThis error has been reported to the Tree Growth team.\n')
        else:
            print('\nOur team is already aware of this issue.\n')

    def _checkIfIssueExists(self, handler: BugHandler, errorTitle: str) -> bool:
        """Checks if an issue already exists in the repository.

        Args:
            handler (BugHandler): the object of reporting details
            errorTitle (str): the title of the error

        Returns:
            bool: True if the issue exists, False if it does not
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

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
            "login": handler.orgName,
            "name": handler.repoName,
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

    def _getRepoId(self, handler: BugHandler) -> str:
        """Gets the repository ID.

        Args:
            handler (BugHandler): the object of reporting details

        Returns:
            str: the repository ID
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

        # query variables
        getID = """
            query getID($owner: String!, $name: String!) {
                repository(owner: $owner, name: $name) {
                    id
                }
            }
        """

        variables = {
            "owner": handler.orgName,
            "name": handler.repoName
        }

        repoID = asyncio.run(client.execute_async(query=getID, variables=variables, headers=headers))
        return repoID['data']['repository']['id']

    @classmethod
    def manualBugReport(cls, repoName: str, errorTitle: str, errorMessage: str) -> None:
        """Manually sends a bug report to the Github repository.

        Args:
            repoName (str): the name of the repo to report to
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """
        if repoName not in cls.handlers:
            raise NotCreatedError(f"{repoName} has not been associated with a reporter")
        handler = cls.handlers[repoName]
        if handler.test == True:
            print('This is a test run and no bug report will be sent.')
            return
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

        # query variables
        repoId = cls._getRepoId(cls, handler)
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

        issueExists = cls._checkIfIssueExists(cls, handler, errorTitle)

        if (issueExists == False):
            result = asyncio.run(client.execute_async(query=createIssue, variables=variables, headers=headers))
            print('\nThis error has been reported to the Tree Growth team.\n')
        else:
            print('\nOur team is already aware of this issue.\n')
