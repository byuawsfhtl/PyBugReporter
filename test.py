from PyBugReporter.src.BugReporter import BugReporter
import os
import dotenv

import boto3

if __name__ == "__main__":
    # awsSession = boto3.Session(region_name="us-west-2")
    # client = awsSession.client(service_name="ssm")
    # response = client.get_parameter(Name='/growth-spurt/github/access-token', WithDecryption=True)
    # token = response['Parameter']['Value']
    dotenv.load_dotenv("./.env")
    token = os.getenv("GITHUB_TOKEN")
    discordToken = os.getenv("DISCORD_TOKEN")
    channelId = os.getenv("CHANNEL_ID")

    BugReporter.setVars(token, 'PyBugReporter', 'byuawsfhtl', False, True, discordToken, channelId)
    
    BugReporter.manualBugReport("PyBugReporter",
                                "Testing manual bug report", 
                                "This is a test of the manual bug report functionality")

    @BugReporter('PyBugReporter', extraInfo=True, env='test')
    def test(item, item2=None):
        # raise Exception("""
        #                 This is a really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really
        #                  really really really really really really really really long test exception
        #                 """)

        # def this():
        #     def exception():
        #         def has():
        #             def an():
        #                 def insane():
        #                     def traceback():
        #                         def length():
        #                             def that():
        #                                 def just():
        #                                     def keeps():
        #                                         def going():
        #                                             def on():
        #                                                 def yep():
        #                                                     def still():
        #                                                         def more():
        #                                                             def never():
        #                                                                 def do():
        #                                                                     def this():
        #                                                                         raise Exception("This is a test exception")
        #                                                                     this()
        #                                                                 do()
        #                                                             never()
        #                                                         more()
        #                                                     still()
        #                                                 yep()
        #                                             on()
        #                                         going()
        #                                     keeps()
        #                                 just()
        #                             that()
        #                         length()
        #                     traceback()
        #                 insane()
        #             an()
        #         has()
        #     exception()
        # this()

        raise Exception("This is a test exception")
                                                

    # test(None, item2='item2')