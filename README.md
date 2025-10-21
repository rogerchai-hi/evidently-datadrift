<h1 align="center">Evidently (Data Drift Only)</h1>


> ⚠️ This is a lightweight fork of [Evidently](https://github.com/evidentlyai/evidently),
> keeping only the **Data Drift** functionality,
> all other UI and dashboard components were removed to simplify dependencies.
> Maintained for personal integration purpose.
>
> Original project: [Evidently AI](https://github.com/evidentlyai/evidently) — Apache 2.0 License.



## Overview
A stripped-down fork of [Evidently](https://github.com/evidentlyai/evidently), keeping only the Data Drift functionality.


## License
Licensed under the [Apache 2.0 License](./LICENSE) from the original project.


<br>

# 👩‍💻 Install

WIP

# ▶️  Getting started

## Reports


### Data drift evals

> This is a simple Hello World. Check the Tutorials for more: [Tabular data](https://docs.evidentlyai.com/quickstart_ml).

Import the Report, evaluation Preset and toy tabular dataset.

```python
import pandas as pd
from sklearn import datasets

from evidently import Report
from evidently.presets import DataDriftPreset

iris_data = datasets.load_iris(as_frame=True)
iris_frame = iris_data.frame
```

Run the **Data Drift** evaluation preset that will test for shift in column distributions. Take the first 60 rows of the dataframe as "current" data and the following as reference.  Get the output in Jupyter notebook:

```python
report = Report([
    DataDriftPreset(method="psi")
],
include_tests="True")
my_eval = report.run(iris_frame.iloc[:60], iris_frame.iloc[60:])
my_eval
```

You can also save an HTML file. You'll need to open it from the destination folder.

```python
my_eval.save_html("file.html")
```

To get the output as JSON or Python dictionary:
```python
my_eval.json()
# my_eval.dict()
```
You can choose other Presets, create Reports from indiviudal Metrics and configure pass/fail conditions.



# 🚦 What can you evaluate?

Evidently has 100+ built-in evals. You can also add custom ones.

Here are examples of things you can check:

|                           |
|:-------------------------:|
| **📊 Data distribution drift** |
| 20+ statistical tests and distance metrics to compare shifts in data distribution.
| **🛢 Data quality**        |
| Missing values, duplicates, min-max ranges, new categorical values, correlations, etc.
| **🔡 Text descriptors**   |
| Length, sentiment, sentence count, OOV words percentage, non-letter character percentage.

