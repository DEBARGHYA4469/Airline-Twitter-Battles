from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream




access_token = "<Enter your access token>"
access_token_secret = "<Enter your token secret>"
consumer_key ="<Enter your consumer key>"
consumer_secret = "<Enter your consumer secret>"

class StdOutListener(StreamListener):
	def on_data(self, data):
		print data
		return True

	def on_error(self, status):
		print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords
	stream.filter(track=['<Type the airline name>'])


