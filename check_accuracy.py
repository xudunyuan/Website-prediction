import pandas as pd
def Check_prediction_accuracy():
	prediction = pd.read_csv('prediction.csv')
	total_pre_column = prediction.shape[0]
	total_pre_row = prediction.shape[1]
	test = pd.read_csv('testData.csv')
	total_test_column = test.shape[0]
	total_test_row = test.shape[1]

	Scores = []
	for i in range(total_pre_column):
		data = test.iloc[i+1,:].values.tolist()
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
	total_score = 0
	for i in Scores:
		total_score = total_score + i
	print("final score: ", total_score/len(Scores))

Check_prediction_accuracy()


