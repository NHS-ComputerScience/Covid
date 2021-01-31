import praw
import re
from praw.models import MoreComments
from Project.Filter import removeDuds
from Project.Stock import Stock

symbols = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


# for using reddit's api - src=https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

def findStocks(count: int, top: int):
    reddit = praw.Reddit(client_id='iQUuWuT22lbViA', client_secret='w_lXzZ0KbS9L34z_TsyKFbo5PgrJbA',
                         user_agent='Web Scraper')

    hot_posts = reddit.subreddit('wallstreetbets').hot(limit=count)
    possibleStocks = dict()
    for post in hot_posts:
        for top_level_comment in post.comments:
            if isinstance(top_level_comment, MoreComments):
                continue

            for listOfStonks in re.findall('([' + symbols + ']*[A-Z]{3,4}[' + symbols + ']*)', top_level_comment.body):
                stonk = listOfStonks.strip(symbols)
                if stonk in possibleStocks:
                    possibleStocks[stonk] = possibleStocks.get(stonk) + 1
                else:
                    possibleStocks[stonk] = 1

    likelyStocks = (removeDuds(possibleStocks))
    likelyStocks = (dict(sorted(likelyStocks.items(), key=lambda item: -1 * item[1])))

    stockList = list()
    for stock in list(likelyStocks)[:5]:
        stockList.append(Stock(stock))

    return stockList


for Stock in findStocks(5, 5):
    print(Stock)
    print()
