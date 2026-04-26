	Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6)  ： 将个股两日成交量的变动和收益率的排名计算6日的相关性且 相关性越大的因子值越小 意味着量价越配合 量价齐升的在横截面的排名就越低 更看重量价的背离关系 背离越严重 分值越高

	Alpha#4: (-1 * Ts_Rank(rank(low), 9)) ： 先对个股在横截面的low进行排名而后在时序上对9天的在市场上相对的low位置进行排序 ， 意思是我们想看在9天的市场波动中个股i今天的低位的相对位置怎么变化了，如果变高了就给予更高的负值 更低了就给予更低的负值 也就是容易被选中 它在奖励那些今天的低点位置相对于平时9天更弱的股票

	Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))：sum(vwap, 10)最近10天的平均成交价，(rank((open - (sum(vwap, 10) / 10)))开盘相离最近10日均价的偏离程度 (-1 * abs(rank((close - vwap))))) -> close-vwap今天收盘对价格的偏离程度，如果太大那么就对这个因子进行扣分惩罚 -> 这捕捉的是如果一个股价偏离10天均值 大高开那么如果收盘他还能延续 没有大幅回撤 则给他高分 要买入 ->这是个动量因子

 

	Alpha#6: (-1 * correlation(open, volume, 10) ：10天开盘和当日总成交量的相关系数开盘价格如果和总量在10天内高度相关则给他打低分  ->如果10天里面 高开+放量 同时低开加少量则放在低位不买入 ：它在捕捉什么？在捕捉背离 如果高开加单日放量我们认为这里太狂热不对劲 
	如果低开加大量这里背离了 我们认为有人承接 给高分。
	回测结果：

	  long_only   CAGR 22.89%, Sharpe 1.00, MaxDD -39.86%, Final NAV 2.690
	  short_only  CAGR 17.03%, Sharpe 0.72, MaxDD -32.76%, Final NAV 2.127
	  long_short  CAGR 23.39%, Sharpe 2.90, MaxDD  -5.18%, Final NAV 2.743

	既然在捕捉背离：如果单日价差大 -> 量小 & 价差小量大 都代表市场的一种不寻常的状态  
						价差小 ->量小 & 价差大->量大 更加常规
						
	alpha6 变体 (-1 * correlation(high-low, volume, 10)）
		回测结果
	  long_only   CAGR 53.30%, Sharpe 1.89, MaxDD -29.17%, Final NAV 7.779
	  short_only  CAGR -6.08%, Sharpe -0.14, MaxDD -46.43%, Final NAV 0.740
	  long_short  CAGR 23.30%, Sharpe 3.07, MaxDD  -8.38%, Final NAV 2.734


	Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))：
	(adv20 < volume）平均20天的交易量如果小于当日volume 即当日放量 ->((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7)))
	sign（delta(close, 7)）当日收盘相比7天前收盘的价格差为正则+ 负则-
	ts_rank(abs(delta(close, 7)), 60)) 在时间序列上排序 如果今天的close相较于7天的差值在过去60天的振幅 越大给分越高 
		抓的是放量+60日超跌

	Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))
		(sum(open, 5) * sum(returns, 5))：5天开盘价总和 ** 五天收益总和 
		 delay((sum(open, 5) * sum(returns, 5)), 10)：延迟10天的5天开盘价总和 ** 五天收益总和 
			

