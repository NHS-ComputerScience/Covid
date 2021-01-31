from src.FocusedWebCrawler import findStocks


# https://www.geeksforgeeks.org/clear-screen-python/


def main():
    name: str = input("Enter your name > ")

    while True:
        command = input(name + " > ").split(' ')

        if command[0] == 'help':
            print("help - prints help menu\n" +
                  "exit - exits the program\n" +
                  "wsb [page count] [number of stocks] - returns with a brief about the stocks that have WSB talking.")
        if command[0] == 'wsb' and len(command) == 3:
            pageCount: int = int(command[1])
            stockCount: int = int(command[2])
            stocksList = findStocks(pageCount, stockCount)

            for Stock in stocksList:
                print(str(Stock) + '\n')

        if command[0] == 'exit':
            break;

        else:
            print("Error, command not found. Consult 'help'.")
main()
