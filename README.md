# Sentiment & Visual Based Algorithmic Trading
This repo trades stocks on a paper account using the Alpaca API.

The algorithm is designed to include a sentiment factor in addition to basic Moving Average strategy. By gathering the headlines of news articles from various sources for a specific ticker, the model analyzes the sentiment (Positive, Neutral, Negative) of each article, compounds those values [-1,1] and suggests the sentiment on a specific day. This logic is implemented after the Moving Average calculation, which will reinforce or counter the decision made by the MA.

## Setting Up Alpaca Account
1. Sign-up for a free Alpaca account at <https://app.alpaca.markets/signup>
2. Once you login to your Alpaca account you will find a Live Trading tab on the left side menu bar. Change that to Paper Trading by selecting in the drop-down list.
3. On you Paper Trading dashboard, on the right side you will find Your API Keys.
4. Click on the View button and note down your API information: Endpoint, API Key ID and Secret Key.

## Running the algorithm
1. **Update API information:** From the repo locate the secrets-alpaca.trading file and open with any text editor. Enter your API details in the relevant lines. Make sure to not leave any space between your API information and the = sign. Save the file and close it.

2. **Setup virtual environment:** It is recommended to use a virtual environment to run the script. You can setup virtual environment using Anaconda or by installing virtualenv from terminal by running the following commands.
	
	**For Mac & Linux:**
		
		sudo pip install virtualenv 
		virtualenv trading
		source trading/bin/activate
		
	**For Windows if you have PIP installed already**
		
		pip install virtualenv
		virtualenv trading
		C:\Users\Username\trading\Scripts\activate.bat
	Make sure to replace "Username" in the path with your username. 

	You will see trading in parentheses in the new command line. This indicates virtual environment is active

3. **Run script:** Run the commands below in the terminal window where virtual environment was activated.

	**For Mac and Linux:**

		make install
		python strategy.py

	**For Windows:**

		pip install -r requirements.txt
		clear
		python strategy.py

## File Descriptions

### strategy.py
This file contains the script that implements the trading strategy

### support.py
This file contains various functions that are used by the strategy.py file

### sentiment.py
This file contains a function used by the strategy.py file to get sentiment of news headlines for a given stock

### requirements.txt
Python libraries required for the algorithm

### finbert
Sentiment analyser using BERT model trained on financial news dataset

### pytorch_model
Pre-trained model used by finbert

### secrets.trading
File to store Alpaca API credentials

