# 逐步回归 ：  “The result of marrying feature selection to linear regression is stepwise regression.”  -> 线性回归+特征选择

- 在训练集上训练得到的结果会明显好于测试集 ->
- CAGR : compound annual growth rate  -> 真实年化

### “Stepwise regression differs from multiple regression in that it starts with just one “best” predictor based on some common goodness of fit criterion such as the sum of squared error (the default for MATLAB's stepwiselm function), Akaike information criterion (AIC), or Bayesian information criterion (BIC)”

逐步回归和多元回归的方法不同 ： 
	逐步回归一开始只选一个当前看来最好的变量，然后再一步步决定要不要加入别的变量，或者删掉已经加入的变量
	 多元回归：全部特征都丢进去处理
不断丢进不同的特征基于这些指标：
	  SSE ： 残差平方和  -> 减小模型的拟合误差
	  AIC ： 赤池信息准则  -> 即看模型效果也惩罚模型太复杂 ，因为如果只使用SSE： 丢进更多的特征拟合自然好 但无法避免过拟合 因此-> 拟合的好 加分 ，拟合不好 扣分 。
	  ![[Pasted image 20260415124955.png]]
	  
	  BIC ： 贝叶斯信息准则
  ,![[Pasted image 20260415125103.png]]



<“model=stepwiselm([ret1(trainset) ret2(trainset) ret5(trainset) ret20(trainset)], retFut1(trainset), 'Upper', 'linear') >

The input parameter name/value pair “Upper” with its value “linear” indicates that we only want linear functions of the independent variables as predictors, not products of them.” upper 和 linnear 限制模型搜索的上限只允许包含线形项

摘录来自
Machine Trading
Ernest P. Chan
此材料可能受版权保护。



# Regression Tree
	所有特征共同作用于数据中 这点与逐步回归不同 
	 原理 ：“Once the algorithm picks the “best” predictor based on some criterion, it will split the data into two subsets by applying an inequality condition on this predictor (such as “previous two‐day return  1.5%”). 如果基于某个准则 算法找到了好的切分方式 它就会将数据切成两块
	 这个指标通常是使得子节点里面的方差最小化
	  在以下几种情况下要停止优化 ： 
		  1.分了之后方差相比父节点没有减小
		  2.父节点几乎没有样本了 
		   3.最大节点数达到了

# Cross Validation

	“Cross validation is a technique for reducing overfitting by testing for out‐of‐sample performance as part of model building. ”
将样本外测试表现作为构建模型的一部分用来防治过拟合
		做法 ： 1. 将训练集随机分成k个子集  2.用k-1个子集训练model 3.用该model在没被训练到的子集上进行测试 4.测试模型的精准度 5.从k个模型中选择一个最好的测试
# Bagging
	“we randomly sample N observations from the original training set with replacement to form a replica (a bag) of the original training set”也是用来防治过拟合的方法 
		做法 ： 1.随机放回抽N个样本 并重复K次 得到 K个有N样本的子集 2.训练K个模型
		3. 从k个预测里面取平均值得到预测值

#  Random Subspace and Random Forest
	random subspace : 随机抽特征 用特征去训练模型 因此得到了很多的模型。然后将这些很多模型（若学习者）合在一起让他们的预测更加健壮也就是将他们预测的结果平均起来 -> 这也叫做集成学习方法 -> 然而这个只适用于分类问题且当我们的特征够多的时候才表现的好
	 random forest ： 随机森林 也是一种集成学习方法  ， 是bagging法和random subspace的杂交
		
	

# Boosting
	从错误中学习 “Boosting involves applying a learning algorithm iteratively to the prediction errors of the model constructed in the previous iteratipn.
	做法： 应用一种学习算法 使用回归树或者其他 2. 第一棵树预测 第二棵树预测残差 第三棵树继续预测剩下的残差

# Classification Tree
	跟回归树是兄弟树 ，区别在于 回归树分类的依据是最小节点方差， 而分类树的划分依据在于该节点的纯度 

![[Pasted image 20260415152040.png]]
	如何看这个模型好不好？ 看它每一个节点GDIs的和
