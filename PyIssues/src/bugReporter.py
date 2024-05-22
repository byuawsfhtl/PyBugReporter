import os.path
from python_graphql_client import GraphqlClient
import os
import asyncio

def checkIfIssueExists(errorTitle):
    client = GraphqlClient(endpoint="https://api.github.com/graphql")
    headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}

    # Load up values for query
    orgName = "byuawsfhtl"
    repoName = "GrowthSpurt"
    autoLabel = "auto generated"

    # Query to return all issues with auto gen label
    findIssue = """
        query findIssue ($login: String = "", $name: String = "", $labels: [String!] = "") {
            organization(login: $login) {
                repository(name: $name) {
                    issues(labels: $labels, first: 100, states: OPEN) {
                        nodes {
                            title
                        }
                    }
                }
            }
        }
    """

    variables = {
        "login": orgName,
        "name": repoName,
        "labels": autoLabel,
    }

    result = asyncio.run(client.execute_async(query=findIssue, variables=variables, headers=headers))

    print(result)

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

def sendBugReport(errorTitle, errorMessage):
    client = GraphqlClient(endpoint="https://api.github.com/graphql")
    headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}

    # Load up values for query
    repoId = "R_kgDOGz8aww"
    bugLabel = "LA_kwDOGz8aw87jO5R4"
    autoLabel = "LA_kwDOGz8aw87jO5SA"

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

    issueExists = checkIfIssueExists(errorTitle)

    if issueExists == False:
        response = asyncio.run(client.execute_async(query=createIssue, variables=variables, headers=headers))
        if 'errors' in response.keys():
            return False
        print('\nThis error has been reported to the Tree Growth team.\n')
        return True
    else:
        print('\nOur team is already aware of this issue.\n')
        return True