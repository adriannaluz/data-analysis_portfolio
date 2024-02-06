# Customer segmentation

Once built the ETL pipeline that clean the e-commerce data ([check repo here](https://github.com/adriannaluz/data-engineering_portfolio/tree/main/ETL_pipeline)), the analysis
of such data is going to be performance on this project. The aim is to segment the customer 
data.

## Data Exploration
In the data exploration notebook ([here](https://github.com/adriannaluz/data-analysis_portfolio/blob/customer_segmentation/customer_segmentation/notebooks/data_exploration.ipynb)), I had a rough look on the data to check for inconsistencies overseen during the data engineering. As a general overview, I found that:
- There are 34 transactions with price equal to zero
- There are 8507 transactions with quantity smaller than zero. These transactions were considered returns 
- There are 18 stock codes with 'Unknown' descriptions. The reason why is still unclear
- The price variable is positively skewed. The outliers represent 8.4% of the data (based on the IQR method)
- The best seller item in the whole dataset is also the most return one.
