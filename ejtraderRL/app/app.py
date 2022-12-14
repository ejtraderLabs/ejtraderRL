import streamlit as st
from ejtraderRL.app import dqn, qrdqn
from ejtraderRL import data, nn
import pandas as pd
import gc


class App:
    def __init__(self):

        self.df = None
        self.agent = None
        self.model_name = ""

    def select_data(self):
        file = None

        select = st.selectbox("", ("forex", "stock", "url or path", "file upload"))
        col1, col2 = st.columns(2)
        load_file = st.button("load file")

        if select == "forex":
            symbol = col1.selectbox("", ("AUDJPY", "AUDUSD", "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPJPY",
                                                        "GBPUSD", "USDCAD", "USDCHF", "USDJPY", "XAUUSD"))
            timeframe = col2.selectbox("", ("m15", "m30", "h1", "h4", "d1"))
            if load_file:
                self.df = data.get_forex_data(symbol, timeframe)
        elif select == "stock":
            symbol = col1.text_input("", help="enter a stock symbol name")
            if load_file:
                self.df = data.get_stock_data(symbol)
        elif select == "url or path":
            file = col1.text_input("", help="enter url or local file path")
        elif select == "file upload":
            file = col1.file_uploader("", "csv")

        if load_file and file:
            st.write(file)
            self.df = pd.read_csv(file)
            
            

        if load_file:
            st.dataframe(self.df, 700, 500)
            st.write("Data selected")

    def check_data(self):
        f"""
        # Select Data
        """
        if isinstance(self.df, pd.DataFrame):
            st.write("Data already exists")
            if st.button("change data"):
                st.warning("data and agent have been initialized")
                self.df = None
                self.agent = None

        if not isinstance(self.df, pd.DataFrame):
            self.select_data()

    def create_agent(self, agent_name, args):
        agent_dict = {"dqn": dqn.DQN, "qrdqn":qrdqn.QRDQN}
        self.agent = agent_dict[agent_name](**args)

    def agent_select(self):
        if not isinstance(self.df, pd.DataFrame):
            st.warning("data does not exist.\n"
                       "please select data")
            return None

        agent_name = st.selectbox("", ("dqn", "qrdqn"), help="select agent")

        """
        # select Args
        """
        col1, col2 = st.columns(2)
        network = col1.selectbox("select network", (nn.available_network))
        network_level = col2.selectbox("select network level", (f"b{i}" for i in range(8)))
        network += "_" + network_level
        self.model_name = network

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        lr = float(col1.text_input("lr", "1e-4"))
        n = int(col2.text_input("n", "3"))
        self.risk = float(col3.text_input("risk", "0.1"))
        balance = int(col4.text_input("balance", "1000"))
        pip_scale = int(col5.text_input("pip scale", "25"))
        col1, col2 = st.columns(2)
        gamma = float(col1.text_input("gamma", "0.99"))
        use_device = col2.selectbox("use device", ("cpu", "gpu", "tpu"))
        train_spread = float(col1.text_input("train_spread", "0.2"))
        spread = int(col2.text_input("spread", "7"))
        self.epochs = int(col2.text_input("epochs", "40"))

        kwargs = {"df": self.df, "model_name": network, "lr": lr, "pip_scale": pip_scale, "n": n,
                  "use_device": use_device, "gamma": gamma, "train_spread": train_spread,
                  "spread": spread,"balance": balance, "risk": self.risk}

        if st.button("create agent"):
            self.create_agent(agent_name, kwargs)
            st.write("Agent created")

    def agent_train(self):
        if self.agent:
            if st.button("training"):
                self.agent.train(self.epochs)
        else:
            st.warning("agent does not exist.\n"
                       "please create agent")

    def show_result(self):
        if self.agent:
            self.agent.plot_result(self.agent.best_w,self.risk)
        else:
            st.warning("agent does not exist.\n"
                       "please create agent")

    def model_save(self):
        if self.agent:
            save_name = st.text_input("save name", self.model_name)
            if st.button("model save"):
                self.agent.model.save(save_name)
                st.write("Model saved.")
        else:
            st.warning("agent does not exist.\n"
                       "please create agent")

    @staticmethod
    def clear_cache():
        if st.button("initialize"):
            st.experimental_memo.clear()
            del st.session_state["app"]
            gc.collect()

            m = """
                **Initialized.**
                """
            st.markdown(m)


def sidebar():
    return st.sidebar.radio("", ("Home", "select data", "create agent", "training",
                                 "show results", "save model", "initialize"))


def home():
    md = """
    # ejtraderRL Web Application
    This web app is intuitive to [ejtraderRL](https://github.com/ejtraderLabs/ejtraderRL).
    
    # How to Execute
    1. select data
        * Click on "select data" on the sidebar to choose your data.
    2. create agent
        * Click "create agent" on the sidebar and select an agent name and arguments to create an agent.
    3. training
        * Click on "training" on the sidebar to train your model.
    4. show results
        * Click "show results" on the sidebar to review the training results.
    """
    st.markdown(md)


if __name__ == "__main__":
    st.set_page_config(layout="wide", )

    if "app" in st.session_state:
        app = st.session_state["app"]
    else:
        app = App()

    select = sidebar()

    if select == "Home":
        home()

    if select == "select data":
        app.check_data()
    elif select == "create agent":
        app.agent_select()
    elif select == "training":
        app.agent_train()
    elif select == "save model":
        app.model_save()
    elif select == "show results":
        app.show_result()

    st.session_state["app"] = app
    if select == "initialize":
        app.clear_cache()

