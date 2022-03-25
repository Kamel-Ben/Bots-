import twitter,time, discord
from discord.embeds import Embed
from discord.ext import tasks

#API Keys 
CONSUMER_KEY = 'YOUR CONSUMER KEY'
CONSUMER_SECRET = 'YOUR SECRET KEY'
OAUTH_TOKEN = 'YOUR OAUTH_TOKEN'
OAUTH_TOKEN_SECRET = 'YOUR OAUTH_TOKEN_SECRET'

#Twitter connexion 
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

#List people you want to check 
list = ['ACCOUNT_1','ACCOUNT_2','ACCOUNT_3'] 

#Discord connexion + bot message 
client = discord.Client()
@tasks.loop(seconds = 1)
async def check_following():
    link = []
    for i in list:
        followers_data = twitter_api.friends.list(screen_name=i) #Take following list 
        for followers in followers_data['users'][:10]: #Take last 10 following 
            link.append("https://www.twitter.com/"+followers['screen_name'])
        channel = client.get_channel('DISCORD CHANNEL')
        embed = discord.Embed(title = 'Last 10 following - '+i,color= discord.Colour.dark_teal())
        embed.add_field(name="Account Followed : ",value=[k for k in link], inline=False)
        await channel.send(embed = embed)
        link=[]
        time.sleep(10)

@client.event
async def on_ready():
    print("Bot is ready")
    check_following.start()

client.run("DISCORD TOKEN")
