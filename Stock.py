from bs4 import BeautifulSoup
import requests
import datetime


class Stock:
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
                           .replace("<", ">").split(">")[2])

        try:
            self.afterHours = float(str(soup.find_all('span', class_="C($primaryColor) Fz(24px) Fw(b)"))
                                    .replace("<", ">").split(">")[2])
        except Exception:
            self.afterHours = -1

        self.previousClose = float(
            str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").split(">")[4])

        self.openPrice = float(
            (str(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)')).replace("<", ">").split(">")[12]))

        self.changePastDay = (self.price - self.previousClose)

        self.changePastDayAH = (self.afterHours - self.price)

        self.changePastDayPercent = self.changePastDay / self.previousClose

        self.changePastDayPercentAH = self.changePastDayAH / self.price

    def __str__(self):
        if self.status == 'Over the Table':
            output = f"{self.name} {str(self.abbr).upper()}\n" \
                     f"NYSE: ${self.price}  ({self.changePastDay:.2f}, {self.changePastDayPercent * 100:.2f}%) [CLOSED]\n" \
                     f"Previous Close: ${self.previousClose}\n" \
                     f"Open: ${self.openPrice}"
        else:
            output = f"{self.name} {str(self.abbr).upper()}\n" \
                     f"NYSE: ${self.price}  ({self.changePastDay:.2f}, {self.changePastDayPercent * 100:.2f}%)\n" \
                     f"Previous Close: ${self.previousClose}\n" \
                     f"Open: ${self.openPrice}"
        return output
