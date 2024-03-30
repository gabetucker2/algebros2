# algebros2

Welcome!

Work abandoned before deadline:

* We spent our entire first day on MultimodalSentimentStrategy, which aimed to make a system that could run all our algorithms through a single Python environment.  We abandoned this method in lieu of strategies that would yield more immediate results but plan to expand this codebase for real stock trading after the hackathon is completed.
* ACTRAttempt was a work-in-progress model attempting to implement the ACT-R cognitive architecture, a supervised learning algorithm, in an isolated environment.  We abandoned this because ACT-R had less intuitive explanatory power than our other statistical models, but we plan to complete this after the hackathon.

Final work:

* FeatureImportanceAnalysis is the feature importance analysis code that we used to understand the correlations between the dataset's features, which disconfirmed our hypothesis that CL prices affect DA prices significantly.
* Candlesticks visualizes the overall trends of the datasets.
* MultipleLinearRegression was the algorithm we used to identify the coefficients used in the MarketSentimentStrategy.
* MarketSentimentStrategy was the simulation strategy based on market sentiment with a 20% return rate (with leverage) on average.
* BrownianStrategy was the simulation strategy baseed on geometric brownian motion ODEs that had a 10.2% return rate (with leverage) on average, beating the money market.

Let me know if you struggle to access any of our scripts!
