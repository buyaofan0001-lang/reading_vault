	Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6)  ： 将个股两日成交量的变动和收益率的排名计算6日的相关性且 相关性越大的因子值越小 意味着量价越配合 量价齐升的在横截面的排名就越低 更看重量价的背离关系 背离越严重 分值越高

	Alpha#4: (-1 * Ts_Rank(rank(low), 9)) ： 先对个股在横截面的low进行排名而后在时序上对9天的