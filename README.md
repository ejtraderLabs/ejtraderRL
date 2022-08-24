
# Table of contents
* [Install](#install)
* [Technologies](#technologies)
* [How to run](#how-to-run)
* [Use custom model](#use-custom-model)

# Install 

```console
pip install ejtraderRL -U
```
# Install from source
```console
git clone https://github.com/ejtraderLabs/ejtraderRL.git
cd trade-rl
pip install .
```

# Technologies
| Technologies | version |
| -- | -- |
| python | >= 3.7 |
| tensorflow | >= 2.7.0 |
| numpy |>= 1.21.4 |
| pandas |>= 1.3.4 |
| ta | >= 0.7.0 |

# How to run

```python
from ejtraderRL import data, agent

# forex data
df = data.get_forex_data("EURUSD", "h1")
# stoch data
#df = data.get_stock_data("AAPL")

agent = agent.DQN(df=df, model_name="efficientnet_b0", lr=1e-4, pip_scale=25, n=3, use_device="cpu", 
                          gamma=0.99, train_spread=0.2, balance=1000, spread=10, risk=0.01)


"""
:param df: pandas dataframe or csv file. Must contain open, low, high, close
:param lr: learning rate
:param model_name: None or model name, If None -> model is not created.
:param pip_scale: Controls the degree of overfitting
:param n: int
:param use_device: tpu or gpu or cpu
:param gamma: float
:param train_spread: Determine the degree of long-term training. The smaller the value, the more short-term the trade.
:param balance: Account size
:param spread: Cost of Trade
:param risk: What percentage of the balance is at risk
"""

agent.train()
```

# Use custom model
```python
from tensorflow.keras import layers, optimizers
from ejtraderRL import nn, agent, data

# forex data
df = data.get_forex_data("EURUSD", "h1")
# stoch data
df = data.get_stock_data("AAPL")

agent = agent.DQN(df=df, model_name=None, lr=1e-4, pip_scale=25, n=3, use_device="cpu", 
                          gamma=0.99, train_spread=0.2, spread=0.7, balance=1000 risk=0.1)

def custom_model():
  dim = 32
  noise = layers.Dropout
  noise_r = 0.1
  
  inputs, x = nn.layers.inputs_f(agent.x.shape[1:], dim, 5, 1, False, "same", noise, noise_r)
  x = nn.block.ConvBlock(dim, "conv1d", "resnet", 1, True, None, noise, noise_r)(x)
  out = nn.layers.DQNOutput(2, None, noise, noise_r)(x)
  
  model = nn.model.Model(inputs, x)
  model.compile(optimizers.Adam(agent.lr, clipnorm=1.), nn.losses.DQNLoss)
  
  return model

agent._build_model = custom_model
agent.build_model()
```

first release of the project is from komo135
thanks to @komo135