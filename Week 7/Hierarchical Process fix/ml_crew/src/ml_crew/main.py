import warnings
from crew import MlCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

ticker = 'Google'

def run():
    """
    Run the crew.
    """
    inputs = {
        'ticker': ticker,
        'file_path': 'stock_price_history.csv',
        'image_file_path': 'price_plot.png',
        'model_path': 'model.pkl'
    }
    
    try:
        MlCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()
