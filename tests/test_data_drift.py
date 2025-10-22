import pathlib

import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.report import Snapshot
from evidently.legacy.tests.base_test import TestStatus
from evidently.metrics import ValueDrift
from evidently.presets import DataDriftPreset


@pytest.fixture
def df():
    data_dir = pathlib.Path(__file__).resolve().parent.with_name("test_data")
    return pd.read_parquet(data_dir / "demographic_data.parquet")

@pytest.fixture
def iris_frame():
    from sklearn import datasets

    iris_data = datasets.load_iris(as_frame=True)
    iris_frame = iris_data.frame
    return iris_frame

def test_value_drift_result(df):
    dates = df["data-date"].drop_duplicates().sort_values(ascending=False)

    cur_series = df[df["data-date"] == dates.iloc[0]]["age"]
    ref_series = df[df["data-date"] == dates.iloc[1]]["age"]
    reference = pd.DataFrame({"score": ref_series})
    current = pd.DataFrame({"score": cur_series})

    report = Report(metrics=[ValueDrift(column="score")], include_tests=True)
    output = report.run(reference_data=reference, current_data=current)
    payload = output.dict()

    metric_value = str(round(payload["metrics"][0]["value"], 3))
    result = payload["tests"][0]["description"]
    status_bool = payload["tests"][0]["status"]

    assert isinstance(eval(metric_value), float)
    assert result.startswith("Drift score is")
    assert status_bool == TestStatus.FAIL

def test_readme_sample(iris_frame):
    report = Report([
        DataDriftPreset(method="psi")
    ],
    include_tests="True")
    my_eval = report.run(iris_frame.iloc[:60], iris_frame.iloc[60:])

    assert isinstance(my_eval, Snapshot)
    assert len(my_eval.json()) > 0

def test_dataset(df):
    num_cols = [
        "age",
        "fnlwgt",
        "education-num",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
    ]
    cat_cols = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
        "class",
    ]
    schema = DataDefinition(
    numerical_columns = num_cols,
    categorical_columns = cat_cols,
    )
    data = Dataset.from_pandas(
        df,
        data_definition=schema
    )
    assert data.data_definition.numerical_columns == num_cols
    assert data.data_definition.categorical_columns == cat_cols
