import pandas as pd

import sys
sys.path.append(".")

from model import Model
from environment import Environment

dataset = pd.read_csv('../data/training_data.csv', parse_dates=['Date', 'Open'])
model = Model()
env = Environment(dataset, model, init_bankroll=1000., min_bet=5., max_bet=100.)
evaluation = env.run(start=pd.to_datetime('2005-07-01'))

print(f'Final bankroll: {env.bankroll:.2f}')

