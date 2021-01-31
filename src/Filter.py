# src = http://www.nasdaqtrader.com for list of stocks and securities


ignore = 'HOLD MOON ONE TWO FOUR FIVE SIX THE NINE TEN ING YOLO CRY BIG ARE FOR EVER STON AWAY SELF LOVE'.split(" ")

def removeDuds(stocks: dict):
    file = open('C:\\Py\\Programming Projects\DiscordBot\\nasdaqList.txt', 'r')
    AllSecs = list()
    for line in file:
        AllSecs.append(line.split("|")[0])
    file.close()

    file = open('C:\\Py\\Programming Projects\DiscordBot\\otherList.txt', 'r')
    for line in file:
        AllSecs.append(line.split("|")[0])
    file.close()

    actualStocks = dict()

    for stock in stocks:
        if stock in AllSecs and stock not in ignore:
            actualStocks[stock] = stocks.get(stock)

    return actualStocks
