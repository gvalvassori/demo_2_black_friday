import google.cloud.aiplatform as aiplatform
from kfp import compiler
from kfp.registry import RegistryClient
from pipeline import pipeline
import argparse
import os
from os.path import join, dirname
from dotenv import load_dotenv

def main(commit):
    PROJECT_ID = "demoespecialidadgcp"
    REGION = "us-central1"
    BUCKET_URI = f"gs://demo-2-black-friday"
    SERVICE_ACCOUNT = "502688298240-compute@developer.gserviceaccount.com"
    PIPELINE_ROOT = f"{BUCKET_URI}/pipelines"
    DATASET_ID = "demo_2_black_friday"
    TABLE_TRAIN = "raw_train"
    TABLE_TEST = "raw_test"
    ARTIFACT_HOST = "https://us-central1-kfp.pkg.dev/demoespecialidadgcp/demo-2-black-friday"

    aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)

    compiler.Compiler().compile(pipeline_func=pipeline, package_path="pipeline.yaml")

    client_registry = RegistryClient(host=ARTIFACT_HOST)

    templateName, versionName = client_registry.upload_pipeline(
        file_name="pipeline.yaml",
        tags=["latest", str(commit)],
        extra_headers={"description":"Pipeline para la transformacion de datos, entrenamiento de modelos, registro de metricas y predicciones"})


    TEMPLATE_PATH=f"https://{REGION}-kfp.pkg.dev/{PROJECT_ID}/demo-2-black-friday/{templateName}/latest"

    schedules = aiplatform.PipelineJobSchedule.list(
        filter='display_name=demo_2_black_friday',
        order_by='create_time desc'
    )
    for schedule in schedules:
        SCHEDULE_ID = schedule.to_dict()["name"]
        pipeline_job_schedule = aiplatform.PipelineJobSchedule.get(schedule_id=SCHEDULE_ID)
        pipeline_job_schedule.delete()

    pipeline_job = aiplatform.PipelineJob(
        display_name="demo_2_black_friday",
        template_path=TEMPLATE_PATH,
        pipeline_root=PIPELINE_ROOT,
        parameter_values={
            'PROJECT_ID': PROJECT_ID,
            'DATASET_ID': DATASET_ID,
            'TABLE_TRAIN': TABLE_TRAIN,
            'TABLE_TEST': TABLE_TEST,
        },
        enable_caching=False,
    )

    # job.run(service_account=SERVICE_ACCOUNT, network=NETWORK)

    pipeline_job_schedule = pipeline_job.create_schedule(
        display_name="demo_2_black_friday",
        cron="TZ=America/Argentina 0 0 15 * *",
    )
    print("Se actualizo correctamente la canalización")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compile and deploy kfp pipeline template for demo-2-black-friday')
    parser.add_argument('-c', '--commit', help='SHORT_SHA of the commit in the branch to set environments variables')
    args = parser.parse_args()
    main(args.commit)