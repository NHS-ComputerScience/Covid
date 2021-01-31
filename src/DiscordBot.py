import discord
import datetime
from FocusedWebCrawler import findStocks
from Stock import Stock

from bs4 import BeautifulSoup
import requests
import datetime


class StockObj:
    abbr = ''
    name = ''
    previousClose = 0.0
    openPrice = 0.0
    price = 0.0
    status = ''
    afterHours = 0.0

    # price - previousClose
    changePastDay = 0.0
    changePastDayAH = 0.0

    # (price - previousClose) / previousClose
    changePastDayPercent = 0.0
    changePastDayPercentAH = 0.0
    marketCap = 0.0

    def __init__(self, abr):
        self.abbr = abr
        time = datetime.datetime.now()
        minuteTime = time.hour * 60 + time.minute
        if 510 <= minuteTime <= 930 and time.weekday() <= 4:
            self.duringHoursSet()
        else:
            self.afterHoursSet()

    def duringHoursSet(self):
        self.status = 'NYSE'
        website = requests.get("https://finance.yahoo.com/quote/" + self.abbr)
        soup = BeautifulSoup(website.content, 'html.parser')

        self.name = str(soup.find_all('h1', class_='D(ib) Fz(18px)')).replace("(", ">").split(">")[3]

        self.price = float(str(soup.find_all('span', class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"))
                           .replace("<", ">").split(">")[2])

        self.previousClose = float(
            str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").split(">")[4])

        self.openPrice = float(
            (str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").split(">")[12]))

        self.changePastDay = (self.price - self.previousClose)

        self.changePastDayPercent = self.changePastDay / self.previousClose

    def afterHoursSet(self):
        self.status = 'Over the Table'
        website = requests.get("https://finance.yahoo.com/quote/" + self.abbr)
        soup = BeautifulSoup(website.content, 'html.parser')

        self.name = str(soup.find_all('h1', class_='D(ib) Fz(18px)')).replace("(", ">").split(">")[3]
        self.price = float(str(soup.find_all('span', class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"))
                           .replace("<", ">").replace(',', '').split(">")[2])

        try:
            self.afterHours = float(str(soup.find_all('span', class_="C($primaryColor) Fz(24px) Fw(b)"))
                                    .replace("<", ">").split(">")[2])
        except Exception:
            self.afterHours = -1

        self.previousClose = float(
            str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").replace(',', '').split(">")[4])

        self.openPrice = float(
            (str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").replace(',', '').split(">")[12]))

        self.changePastDay = (self.price - self.previousClose)

        self.changePastDayAH = (self.afterHours - self.price)

        self.changePastDayPercent = self.changePastDay / self.previousClose

        self.changePastDayPercentAH = self.changePastDayAH / self.price

    def __str__(self):
        if self.status == 'Over the Table':
            output = f"{self.name} {str(self.abbr).upper()}\n" \
                     f"NYSE: ${self.price:,.2f}  ({self.changePastDay:.2f}, {self.changePastDayPercent * 100:,.2f}%) [CLOSED]\n" \
                     f"Previous Close: ${self.previousClose}\n" \
                     f"Open: ${self.openPrice:,.2f}"
        else:
            output = f"{self.name} {str(self.abbr).upper()}\n" \
                     f"NYSE: ${self.price:,.2f}  ({self.changePastDay:.2f}, {self.changePastDayPercent * 100:,.2f}%)\n" \
                     f"Previous Close: ${self.previousClose:,.2f}\n" \
                     f"Open: ${self.openPrice:,.2f}"
        return output


bot = discord.Client()


# When the bot starts initially
@bot.event
async def on_ready():
    guild_count = 0

    # Prints out all the guilds and their ids that the bot is currently inside.
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")

        # Increments guild count.
        guild_count = guild_count + 1

    # Prints how many guilds the bot is in.
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
    command: str = message.content
    if command[0] == '!':
        command = command.split(' ')

        if (command[0][1:]).lower() == 'stonk' and len(command) == 2:
            try:
                await message.channel.send(StockObj(command[1]))
            except Exception as e:
                await message.channel.send("error, no stonk found.")
                await message.channel.send(e)

        if command[0][1:].lower() == 'stonk' and len(command) == 1:
            await message.channel.send(StockObj("gme"))

        if command[0][1:].lower() == 'wsb' and len(command) == 3:
            pageCount: int = int(command[1])
            stockCount: int = int(command[2])
            stocksList = findStocks(pageCount, stockCount)

            output = ''
            for Stock in stocksList:
                output += str(Stock) + '\n\n'
            await message.channel.send(output)
        if command[0][1:].lower() == 'help':
            await message.channel.send("help - returns a help menu--this!\nstonk [acronym] - returns information about the stock\nwsb [web pages] [top] - returns the most talked about stocks on r/WSB")


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run("ODAzODQ4NzA0NTM2MzQ2NjU0.YBDwcQ.uNwFImisVf3cM5P7rVtuDGLBYwk")
