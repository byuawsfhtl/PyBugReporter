from PyBugReporter.src.BugReporter import BugReporter

import boto3

if __name__ == "__main__":
    awsSession = boto3.Session(region_name="us-west-2")
    client = awsSession.client(service_name="ssm")
    response = client.get_parameter(Name='/growth-spurt/github/access-token', WithDecryption=True)
    token = response['Parameter']['Value']
    bugReporter = BugReporter(token, "PyBugReporter", "byuawsfhtl", test=True)

    @bugReporter.report()
    def test(item, item2=None):
        int(['a'])
        raise Exception("This is a test exception")

    test(None, item2='item2')