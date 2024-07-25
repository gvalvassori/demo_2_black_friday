from kfp.dsl import Dataset, Output, component

@component(
    packages_to_install=["google-cloud-bigquery[pandas]==3.15.0"],
    base_image="python:3.10"
)
def export_datasets(
    project_id: str,
    dataset_id: str,
    table_train: str,
    table_test: str,
    dataset_train: Output[Dataset],
    dataset_test: Output[Dataset]
):
    """
    Args:
        project_id: The Project ID.
        dataset_id: The BigQuery Dataset ID. Must be pre-created in the project.
        table_train: The BigQuery train table name.
        table_test: The BigQuery test table name.
        
    Returns:
        dataset_train: The Dataset artifact with exported CSV file.
        dataset_test: The Dataset artifact with exported CSV file.
    """
    from google.cloud import bigquery
    import pandas as pd
    import numpy as np

    client = bigquery.Client(project=project_id)
    table_name = f"{project_id}.{dataset_id}.{table_train}"
    query = """
        SELECT * 
        FROM {table_name}
    """.format(
        table_name=table_name
    )
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query=query, job_config=job_config)    
    df_train = query_job.result().to_dataframe()
    
    table_name = f"{project_id}.{dataset_id}.{table_test}"
    query = """
        SELECT * 
        FROM {table_name}
    """.format(
        table_name=table_name
    )
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query=query, job_config=job_config)    
    df_test = query_job.result().to_dataframe()
    
    df_train['source'] = 'train'
    df_test['source'] = 'test'
    
    dataset = pd.concat([df_train, df_test])
    
    dataset['Age'] = dataset['Age'].apply(lambda x : str(x).replace('55+', '55'))
    dataset['Stay_In_Current_City_Years'] = dataset['Stay_In_Current_City_Years'].apply(lambda x : str(x).replace('4+', '4'))
    dataset.drop('Product_Category_3', axis = 1, inplace = True)
    dataset.drop('User_ID', axis = 1, inplace = True)
    dataset.drop('Product_ID', axis = 1, inplace = True)
    dataset['Product_Category_2'].fillna(dataset['Product_Category_2'].median(), inplace = True)
    dataset['Stay_In_Current_City_Years'] = dataset['Stay_In_Current_City_Years'].astype('int')
    dataset.drop(['Gender', 'City_Category', 'Marital_Status'], axis = 1, inplace = True)
    
    train = dataset.loc[dataset['source'] == 'train']
    test = dataset.loc[dataset['source'] == 'test']
    train.drop('source', axis = 1, inplace = True)
    test.drop('source', axis = 1, inplace = True)
    
    train.to_csv(dataset_train.path + '.csv', index=False)
    test.to_csv(dataset_test.path + '.csv', index=False)
