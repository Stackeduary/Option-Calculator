### Intro to Programming II Project
### Bill Sendewicz


### graphical user interface requirement
from tkinter import * 
optionWindow = Tk() 
optionWindow.geometry("1600x1200") 

# required packages
import numpy as np
from scipy.stats import norm

# interest rate used in option pricing calculation
r = .0012
totalList = []

# tkinter variable declarations
securityVar = StringVar()
optionType = StringVar()
expiration = DoubleVar()
strike = DoubleVar()


### function requirement
# function that prices a European call option
def BlackScholesEuropeanCall(S0Var, strikeVar, expirationVar, r, sigmaVar):
    d1 = (np.log(S0Var/strikeVar) + (r + .5*sigmaVar**2)*expirationVar)/(sigmaVar*np.sqrt(expirationVar))
    d2 = d1 - sigmaVar*np.sqrt(expirationVar)
    return S0Var*norm.cdf(d1) - strikeVar*np.exp(-r*expirationVar)*norm.cdf(d2)

# function that prices a European put option
def BlackScholesEuropeanPut(S0Var, strikeVar, expirationVar, r, sigmaVar):
    d1 = (np.log(S0Var/strikeVar) + (r + .5*sigmaVar**2)*expirationVar)/(sigmaVar*np.sqrt(expirationVar))
    d2 = d1 - sigmaVar*np.sqrt(expirationVar)
    return strikeVar*np.exp(-r*expirationVar)*norm.cdf(-d2) - S0Var*norm.cdf(-d1)
     

# main function in the program that calls the pricing functions above and prints output to the tkinter window
def calculateOption():
    
    # the result of all options priced in the session
    resultList = []
    
    # get the value of variables in the radio buttons below
    typeVar = optionType.get()
    expirationVar = expiration.get()
    strikeVar = strike.get()
    
    """
    if-statement that reads from the file of stock prices to calculate sigma and S0, inputs to the pricing function
    """
    ### conditional statement requirement
    name = securityVar.get()
    if name == 'Facebook':
        pricesFile = 'FB.csv'
    elif name == 'Apple':
        pricesFile = 'AAPL.csv'
    elif name == 'Amazon':
        pricesFile = 'AMZN.csv'
    elif name == 'Netflix':
        pricesFile = 'NFLX.csv'
    elif name == 'Google':
        pricesFile = 'GOOG.csv'
        
    ### external data read-in requirement
    # reads from the file of stock price data from Yahoo Finance and calculates S0 and sigma      
    prices = np.loadtxt(pricesFile, delimiter = ',', skiprows = 1, usecols = (5, ))
    n = len(prices)
    dt = 1/n
    i = np.arange(0, n-1)
    x = np.log(prices[i+1]/prices[i])
    sigma = np.std(x)/np.sqrt(dt)
    S0 = prices[-1]
    
    # logic that determines whether to use the call or put option formula basd on user's input
    if typeVar == 'call':
        priceVar = BlackScholesEuropeanCall(S0, strikeVar, expirationVar, r, sigma)
    if typeVar == 'put':
        priceVar = BlackScholesEuropeanPut(S0, strikeVar, expirationVar, r, sigma)
    outputPriceVar = str(round(priceVar, 2))
    
    # label that displays the option price
    priceLabel = Label(optionWindow, text="The price of the option is " + outputPriceVar, width=50).grid(row=6, column=5, sticky=W, pady=2) 
    
    # collect the results of running the calculation function and store in a list called resultList
    resultList.append(name)
    resultList.append(typeVar)
    resultList.append(strikeVar)
    resultList.append(expirationVar)
    resultList.append(outputPriceVar)
    
    ### nested data structure requirement
    # store the individual resultList lists in a 2D list called totalList
    totalList.append(resultList)

    # store the 2D totalList in a 1D list called optionList
    optionList = []
    for i in range(len(totalList)):
        for j in range(len(totalList[i])):
            optionList.append(totalList[i][j])
    
    ### nested loop requirement
    # store the results of totalList in a nested dictionary called optionDict
    companyList = ['Facebook', 'Google', 'Netflix', 'Amazon', 'Apple']
    optionDict = {}
    for comp in companyList:
       compCounts = [i for i, j in enumerate(optionList) if j == comp]
       optionDict[comp] = {'call': 0, 'put': 0}
       if compCounts == []:
           continue
       for compIndex in compCounts:
           optionDict[comp][optionList[compIndex + 1]] += 1
           
    """
    display optionDict, which is a nested dictionary of the count of puts and calls priced in the session (values)
    by the key company           
    """
    dictLabel = Label(optionWindow, text="These are the options you priced in this session: " + str(optionDict), width=150).grid(row=26, column=5, pady=2, sticky=E)
    
    # return the results of the calculateOption function, which is the price of the option
    return outputPriceVar


# choose security radio buttons
securityLabel = Label(optionWindow, text="Choose a security").grid(row=0, column=0, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Facebook", variable=securityVar, value='Facebook').grid(row=1, column=0, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Apple", variable=securityVar, value='Apple').grid(row=2, column=0, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Amazon", variable=securityVar, value='Amazon').grid(row=3, column=0, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Netflix", variable=securityVar, value='Netflix').grid(row=4, column=0, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Google", variable=securityVar, value='Google').grid(row=5, column=0, sticky=W, pady=2) 


# choose option type radio buttons
optionTypeLabel = Label(optionWindow, text="Choose an option type").grid(row=0, column=1, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Call", variable=optionType, value='call').grid(row=1, column=1, sticky=W, pady=2) 
Radiobutton(optionWindow, text="Put", variable=optionType, value='put').grid(row=2, column=1, sticky=W, pady=2) 

# choose time to expiration radio buttons
expirationLabel = Label(optionWindow, text="Choose a time to expiration").grid(row=0, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="7 days", variable=expiration, value=7/365).grid(row=1, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="30 days", variable=expiration, value=30/365).grid(row=2, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="90 days", variable=expiration, value=.25).grid(row=3, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="180 days", variable=expiration, value=.5).grid(row=4, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="1 year", variable=expiration, value=1).grid(row=5, column=2, sticky=W, pady=2) 
Radiobutton(optionWindow, text="1.5 years", variable=expiration, value=1.5).grid(row=6, column=2, sticky=W, pady=2) 

# choose strike price radio buttons
strikeLabel = Label(optionWindow, text="Choose a strike price").grid(row=0, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$50", variable=strike, value=50).grid(row=1, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$100", variable=strike, value=100).grid(row=2, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$150", variable=strike, value=150).grid(row=3, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$200", variable=strike, value=200).grid(row=4, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$250", variable=strike, value=250).grid(row=5, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$300", variable=strike, value=300).grid(row=6, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$400", variable=strike, value=400).grid(row=7, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$500", variable=strike, value=500).grid(row=8, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$750", variable=strike, value=750).grid(row=9, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$1000", variable=strike, value=1000).grid(row=10, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$1250", variable=strike, value=1250).grid(row=11, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$1500", variable=strike, value=1500).grid(row=12, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$1750", variable=strike, value=1750).grid(row=13, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$2000", variable=strike, value=2000).grid(row=14, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$2500", variable=strike, value=2500).grid(row=15, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$3000", variable=strike, value=3000).grid(row=16, column=3, sticky=W, pady=2) 
Radiobutton(optionWindow, text="$3500", variable=strike, value=3500).grid(row=17, column=3, sticky=W, pady=2) 


# calculate option price button
calculateButton = Button(optionWindow, text="Calculate Option Price", command=calculateOption)
 
calculateButton.grid(row=4, column=5, sticky=W, pady=2) 

optionWindow.mainloop()