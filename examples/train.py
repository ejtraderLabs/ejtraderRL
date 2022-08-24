from ejtraderRL import data, agent

# forex data
df = data.get_forex_data("EURUSD", "h1")
# stoch data
#df = data.get_stock_data("AAPL")

agent = agent.DQN(df=df, model_name="efficientnet_b0", lr=1e-4, pip_scale=25, n=3, use_device="cpu", 
                          gamma=0.99, train_spread=0.2, balance=1000, spread=7, risk=0.01)


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

print("Saving model")

agent.model.save("efficientnet_b0_s0_H1")