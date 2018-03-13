from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream




access_token = "970681031941607424-S6vv4Jr32ydIiUaqEq6cZGPObsUJYiH"
access_token_secret = "S1mkYstz2PUKvUc3pTONdfFLmCMjLefzW21cRGQ1icdAW"
consumer_key ="oEitQBoMR8jmbywLXYp0rKVpi"
consumer_secret = "GXFIEHWyyctRUC4RNPZLaUf4U7iogBSyQBbR4xZn6csmNwPhtE"

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


