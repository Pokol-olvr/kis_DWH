import pendulum
from airflow import DAG
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

project_config = ProjectConfig(
    dbt_project_path="/opt/airflow/dbt"
)

profile_config = ProfileConfig(
    profile_name="dwh_profile",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="dwh_postgres_connection", 
        profile_args={"schema": "public"}, 
    ),
)

with DAG(
    dag_id="dwh_dbt_transformations",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    dbt_run = DbtTaskGroup(
        group_id="dbt_models",
        project_config=project_config,
        profile_config=profile_config,
    )

    dbt_run