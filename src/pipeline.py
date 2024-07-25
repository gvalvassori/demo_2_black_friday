from kfp import dsl
from kfp.dsl import Condition
from components.datasets import export_datasets
from components.train import train_model

@dsl.pipeline(
    name="demo_2_black_friday",
)
def pipeline(
    PROJECT_ID: str,
    DATASET_ID: str,
    TABLE_TRAIN: str,
    TABLE_TEST: str,
    ):
    export_dataset_task = export_datasets(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_train=TABLE_TRAIN,
        table_test=TABLE_TEST,
    )
    
    train_model_task = train_model(
        dataset_train=export_dataset_task.outputs["dataset_train"],
    )