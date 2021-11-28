# Binary Classification - Fraud Detection

The original project was supposed to be passed through an automated Data Science service on cloud. But the learning experience is less than ideal, hence the attempt to approach it locally using a combination of tools. Mainly, Python and it's suite of libraries.

### Problem

Can we predict ethereum accounts that are conducting illicit behaviors?

### Source of Dataset

The dataset was downloaded from Steven Farrugia's github. The dataset's intent is to detect illicit behavior on Ethereum network using account transaction history.

Link to Steven's github project and dataset.
https://github.com/sfarrugia15/Ethereum_Fraud_Detection/tree/master/Account_Stats

In the dataset, the Ethereum accounts that had been flagged by the community for illicit behaviors were collected via etherscam(Defunct) and MyEtherWallet.

https://etherscamdb.info/api/scams/ (Defunct)<br>
https://github.com/MyEtherWallet/ethereum-lists/blob/master/src/addresses/addresses-darklist.json

Accounts were flagged for a number of reasons such as:

* Trying to imitate other contract addresses providing tokens
* Scam lotteries
* Fake ICOs
* Imitating other users
* Ponzi schemes
* Phishing
* Mirroring websites

Accounts transactions were retrieved through the Etherscan API.

### Summary of Data cleaning and Exploratory Data Analysis

The original dataset consisted of 9841 rows with 50 columns of features. It is imbalanced with the target column consisting of 7662 negatives and 2179 positives.

9823 rows and 50 features remained after investigating and dropping duplicates.

A total of 29 features were further dropped due to various reasons as follows:<br>
* irrelevant observations
* provides poor information - 50% to 100% of the data are zeros

A total of 21 features remained.

Null & Missing values existed in 3 of the remaining 21 features. 1 numerical feature and 2 categorical features. Treatment as follows:<br>
* Replaced null & missing values with 'others' in the categorical features. 'others' existed originally.
* 8% of the numerical features were missing and the data is heavily skewed towards zero, hence 0 were filled in instead of Mean.

Feature Selection & Dimension Reduction

Although what remained was not a really large dataset, consideration was given to hypothesis requirements, the size of the DLT space and eventual processing speed. Reducing the dimension further will be helpful in execution time and overfitting.

The dataset is pass through sklearn ExtraTreesClassifier to identify and rank features importance.

![feature_importance](https://user-images.githubusercontent.com/71744941/143726359-3415e811-bb48-4225-961f-91e5f0122bab.JPG)

The top 10 features based on importance were selected and saved to csv for the model.

### Model Training, Prediction and Scores

The dataset is first trained with LightGBM using gbdt (Gradient Boosting Decision Tree). 

The parameter 'is_unbalanced' was set to true as the dataset was unbalanced. LightGBM will balanced it for us. Feature_fraction is set to 0.5 to mitigate the anticipated overfitting. (Given this is the first model, a decision is made not to 'over-complicate' the parameters if there isn't a critical need to. Optimization can be made in future iteration)

Early stop is also implemented to stop the training if additional trees are not improving the validation score for 15 rounds.

The best AUC score is 0.982091.

The average precision score is 0.9476378.

Threshold is set at 0.7 to balance out the number of false positive/false negative and f1 score is 0.863184

Confusion Matrix is as follows:

| 1508 | 55 |
|------|----|
| <b>55</b> | <b>347</b> |

### Post Project Reviews and Thoughts

"There are many tools and libraries that made a difficult subject easy to execute, but a thorough understanding is hard to come by."

<b>What's next?</b>

* Learn to code a simple decision tree from scratch to 'see' the code behind.
* Learn to access and download data from etherscan API.
* Pass the data through other algo such as random forest and lgbm GOSS and compare the results.
* Deepen knowledge in manipulation of data and statistics.
