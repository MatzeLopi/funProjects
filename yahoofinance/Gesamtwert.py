import pandas as pd

from getRawData import getData

def getGesamtwert(aktien):
    return (aktien["currentPrice"] * aktien['Stück']).sum()
