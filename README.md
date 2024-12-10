# AUTOMATING TRADING JOURNAL
## Objective

Given an existing trading journal and a trade transaction file from Tastytrade, update the old journal file by adding new and updating old trades. The journal file's exit date, close price, progress, and commissions/fees should be updated.

### Rules
* Use the last transaction date if exit dates for multilegged trades are different.
* If the expiration date is less than the current date and there are no closing transactions, assume the options contract expired worthless and the close price is 0.

<u>Example</u>

If a trade was opened and closed a few weeks later.

!["Opened Trade"](./img/openedTrade.png)

Using the tastytrade trade transaction file, the program should be able to detect a closed trade and update the trading journal exit date, close price, progress, and commission/fees.

!["Closed Trade"](./img/closedTrade.png)

<u>Trade Journal Sample</u>

!["Trade Journal Sample"](./img/tradeJournalSample.png)

<u>Trade Transaction Sample</u>

!["Trade Transaction Sample"](./img/tradeTransactionSample.png)

## Design Diagram
!["Design Diagram"](./img/design%20diagram.png)

## Design Documentation
**CSVFileHandling:** A class that takes in CSV files creates a copy and reference to trading journal and trade transaction files respectively.

* <span style="font-family: Courier New, monospace; font-size: 19px"> **constructor(self, journalFilePath: str, transFilePath: str)-> None** </span>

   Defines the filePath for trading journal and trade transaction files.
* <span style="font-family: Courier New, monospace; font-size: 19px"> **createCopy(self)-> csv.writer** </span>

   Duplicates trade journal and export the file to the file directory of original csv file and return <span style="font-family: Courier New, monospace; font-size: 17px"> csv.writer </span> object.
* <span style="font-family: Courier New, monospace; font-size: 19px"> **createRef(self)-> csv.reader** </span>

   Opens trade transaction file and returns <span style="font-family: Courier New, monospace; font-size: 17px"> csv.reader </span> object.
