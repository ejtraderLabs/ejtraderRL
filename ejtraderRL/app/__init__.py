import os 


from . import dqn
from . import qrdqn


def web():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'app.py')
    args = []
    os.system(f"streamlit run {filename}")

  
    
    