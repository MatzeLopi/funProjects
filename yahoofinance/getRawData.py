import yfinance as yf
import pandas as pd


def getData(path):
    aktienRaw = pd.read_excel(path)
    aktien = aktienRaw[aktienRaw["Ticker"].notna()]
    aktien.reset_index(inplace=True)



    zeroTicker = aktien['Ticker'][0]
    zeroTickerInfo = yf.Ticker(zeroTicker).info
    infoDict = {}
    for key in zeroTickerInfo.keys():
        infoDict[key] = []

    for ticker in aktien['Ticker']:
        tickerInfo = yf.Ticker(ticker).info
        for k in infoDict.keys():
            try:
                infoDict[k].append(tickerInfo[k])
            except KeyError:
                infoDict[k].append(None)
                    
    aktien = pd.concat([aktien,pd.DataFrame(infoDict)],axis=1)

    return aktien