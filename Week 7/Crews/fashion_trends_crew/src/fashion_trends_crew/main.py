#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import FashionTrendsCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Summer and Winter wears',
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    }

    FashionTrendsCrew().crew().kickoff(inputs=inputs)

run()