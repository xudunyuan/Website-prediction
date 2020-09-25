import pandas as pd
def Check_prediction_accuracy():
	prediction = pd.read_csv('prediction1.csv')
	total_pre_column = prediction.shape[0]
	total_pre_row = prediction.shape[1]
	test = pd.read_csv('testData.csv')
	total_test_column = test.shape[0]
	total_test_row = test.shape[1]

	a = [   40,    70,   105,   139,   193,   272,   466,   540,   645]
	Scores = []
	i = 0
	for j in a:
		data = test.iloc[j,:].values.tolist()
		pre = prediction.iloc[i,:].values.tolist()
		data.pop(0)
		predicted_vote = 0
		for k in range(len(data)):
			predicted_vote = predicted_vote + data[k]
		sum = 0
		for j in range(len(data)):
			sum = sum + abs(pre[j] - data[j])
		Sa = sum / predicted_vote
		Scores.append(Sa)
		i+=1
	total_score = 0
	for i in Scores:
		total_score = total_score + i
	print("final score: ", total_score/len(Scores))
Check_prediction_accuracy()


