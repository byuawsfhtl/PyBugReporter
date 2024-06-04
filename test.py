from PyBugReporter.src.BugReporter import BugReporter

import boto3

if __name__ == "__main__":
    awsSession = boto3.Session(region_name="us-west-2")
    client = awsSession.client(service_name="ssm")
    response = client.get_parameter(Name='/growth-spurt/github/access-token', WithDecryption=True)
    token = response['Parameter']['Value']
    BugReporter.setVars(token, 'PyBugReporter', 'byuawsfhtl', True)
    
    @BugReporter(extraInfo=True, env='test')
    def test(item, item2=None):
        raise Exception("This is a test exception")

    test(None, item2='item2')
