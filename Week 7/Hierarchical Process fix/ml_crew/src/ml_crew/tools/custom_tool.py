# from crewai.tools import BaseTool
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
import json
from datetime import datetime, timedelta



class StockRetrieverInput(BaseModel):
    """Input schema for MyCustomTool."""
    ticker: str = Field(..., description="The ticker symbol of the stock being asked for")

class StockRetriever(BaseTool):
    name: str = "Stock Price Retriever"
    description: str = (
        "This function, named get_daily_stock_price_history, fetches the daily stock price history \
        for a specified stock ticker using Yahoo Finance. It automatically retrieves data from one year \
        prior to today up to the current date. The function validates the ticker and handles errors if \
        the data is unavailable or the ticker is invalid. The output is a Pandas DataFrame with columns \
        like Open, High, Low, Close, Adj Close, and Volume. It can also save the data to a CSV file for further analysis."
    )
    args_schema: Type[BaseModel] = StockRetrieverInput

    def _run(self, ticker: str) -> str:
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

            stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if stock_data.empty:
                print(f"No data found for ticker '{ticker}'. Please check the ticker symbol or the date range.")
                return None

            stock_data.index.name = None
            if 'Ticker' in stock_data.columns:
                stock_data = stock_data.drop(columns=['Ticker'])

            stock_data.columns = stock_data.columns.droplevel('Ticker')
            stock_data.to_csv(f"stock_price_history.csv")

            return f"Stock price of {ticker} has been saved to stock_price_history.csv"

        except Exception as e:
            return f"An error occurred while fetching data for ticker '{ticker}': {e}"


class StringToCodeInput(BaseModel):
    """Input schema for MyCustomTool."""
    code: str = Field(description="Input code. Must be a string that houses the code to be executed")

class StringToCode(BaseTool):
    name: str = "Code Executor"
    description: str = (
        "This function is used to execute python code, inputted as a string."
    )
    args_schema: Type[BaseModel] = StringToCodeInput

    def _run(self, code: str) -> str:
        local_vars = {}
        try:
            exec(code, {}, local_vars)
            return local_vars

        except Exception as e:
            try:
                exec(json.dumps(code), {}, local_vars)
                # return "Code ran successfully", local_vars
                return eval(json.dumps(code))
            except:
                return f"The following error occurred: {e}"
    
