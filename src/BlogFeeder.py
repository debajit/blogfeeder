import feedparser
import datetime 
import BlogServer 
import sys



RSS_URL = "ENTER RSS URL HERE"
SERVER_URL = "http://SERVER-NAME/xmlrpc.php"
USERNAME = "ENTER USERNAME HERE"
PASSWORD = "ENTER PASSWORD HERE"
DEFAULT_BLOG_ID = 1

MARKUP_BEFORE_POST = "<ul>"
MARKUP_BEFORE_ITEM = "<li>"
MARKUP_AFTER_ITEM = "</li>"
MARKUP_AFTER_POST = "</ul>"

UTC_HOURS_DIFFERENCE = -5


class TimeDifference(datetime.tzinfo):
    
    def utcoffset(self, dt):
        return datetime.timedelta(hours = UTC_HOURS_DIFFERENCE)

    def dst(self, dt):
        return datetime.timedelta(0)



class BlogFeeder:

    def __init__(self, feedUrl, blogServer):
        self.feedUrl_ = feedUrl
        self.blogServer_ = blogServer
        self.lastPostDate_ = blogServer.getLastPostDate()
        self.postsPublished_ = 0
        print "Last post date is %s\n" % self.lastPostDate_

    
    def publish(self):
        
        self.parsedFeed_ = feedparser.parse(self.feedUrl_) 
        lastPubDate = tupleToDateTime(self.parsedFeed_.entries[0].updated_parsed)
        counter = 0
        postDescription = ""
        
        for entry in self.parsedFeed_.entries:
            
            title = entry.title
#            pubDate = entry.updated_parsed
#            pubDate = datetime.datetime(pubDate[0], pubDate[1], pubDate[2], pubDate[3], pubDate[4], pubDate[5])
            pubDate = tupleToDateTime(entry.updated_parsed)
            description = entry.description
            print "**** Desc = ", description.encode("utf-8")
            
            if pubDate > self.lastPostDate_:

                # Need to publish this item
                counter += 1
                print "(%d) Found new item with timestamp %s" % (counter, pubDate)

                if pubDate == lastPubDate:
                    postDescription = postDescription + MARKUP_BEFORE_ITEM + description + MARKUP_AFTER_ITEM
                else:
                    self.publishPost(postDescription, lastPubDate)
                    postDescription = MARKUP_BEFORE_ITEM + description + MARKUP_AFTER_ITEM
                
                lastPubDate = pubDate

        if postDescription != "":
            self.publishPost(postDescription, lastPubDate)
        
        return counter, self.postsPublished_

        
    def publishPost(self, postDescription, date):
        postTitle = "Links for " + str(date)[0:10]
        postDescription = MARKUP_BEFORE_POST + postDescription + MARKUP_AFTER_POST
        post = { "title" : postTitle, 
                 "description" : postDescription,
                 "dateCreated" : date }
        print post
        self.blogServer_.newPost(post)
        self.postsPublished_ += 1
        
        
def tupleToDateTime(tuple):
    return datetime.datetime(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], 0, TimeDifference())


def main():
    
    blogServer = BlogServer.BlogServer(SERVER_URL, USERNAME, PASSWORD)
    blogFeeder = BlogFeeder(RSS_URL, blogServer)
    (itemsPublished, postsPublished) = blogFeeder.publish()
    print
    
    if postsPublished == 0:
        print "No new items were found. Nothing was published to the blog."
        sys.exit(1)
    else:
        print "%d New items were found" % itemsPublished 
        print "%d New posts were published" % postsPublished
        sys.exit(0)


if __name__ == "__main__":
    main()