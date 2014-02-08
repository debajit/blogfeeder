import xmlrpclib
import datetime

#TODO: remove and use cmd line args / environment variables
SERVER_URL = "http://server-name/xmlrpc.php"
USERNAME = "ENTER USERNAME HERE"
PASSWORD = "ENTER PASSWORD HERE"
DEFAULT_BLOG_ID = 1
    
UTC_HOURS_DIFFERENCE = -5

class TimeDifference(datetime.tzinfo):
    
    def utcoffset(self, dt):
        return datetime.timedelta(hours = UTC_HOURS_DIFFERENCE)

    def dst(self, dt):
        return datetime.timedelta(0)


class BlogServer:

    """ Blog Server that implements the MetaWeblog API """

    def __init__(self, serverUrl, username, password, blogId = 1):
        self.serverUrl_ = serverUrl
        self.username_ = username
        self.password_ = password
        self.blogId_ = blogId
        self.server_ = xmlrpclib.Server(self.serverUrl_)


    def newPost(self, content):
        """ Adds a new post and returns its post ID """
        return self.server_.metaWeblog.newPost(self.blogId_, self.username_, self.password_, content, True)

    
    def getLastPost(self):
        """ Returns the latest post of the blog as a dictionary """
        return self.server_.metaWeblog.getRecentPosts(self.blogId_, self.username_, self.password_, 1)[0]


    def getLastPostDate(self):
        """ Returns the date of the lastest post for this blog as a datetime object """
        date = self.getLastPost().get("dateCreated")
        return atomDateToDateTime(str(date))

        
        
def atomDateToDateTime(dateString):
    
    """
    Converts a date string in ISO 8601 format to a 
    Python datetime object.
    """
    
    formatString = "%Y%m%dT%H:%M:%S"  
    result = datetime.datetime.strptime(dateString, formatString) 
    result = datetime.datetime(result.year, result.month, result.day, result.hour, result.minute, result.second, 0, TimeDifference())
    return result

def tupleToDateTime(tuple):
    return datetime.datetime(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], 0, TimeDifference())


def main():
    
    blogServer = BlogServer(SERVER_URL, USERNAME, PASSWORD)

    
    content = {"title" : "This is the title", 
               "description" : "This is the description",
               "dateCreated" : datetime.datetime(2007, 01, 11, 0, 0, 0)}
    
    newPostId = blogServer.newPost(content)
    print "Published new post with id", newPostId
   
    
#    print blogServer.getLastPost()
#    lastPostDate = blogServer.getLastPostDate() 
#    lastPostDate = atomDateToDateTime(str(lastPostDate))
#    print lastPostDate > datetime.datetime(2007, 5, 27)
        
if __name__ == "__main__":
    main()