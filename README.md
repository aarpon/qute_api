# qute_api

API to manage deep-learning models and other artifacts. It is used primarily by [qute](https://github.com/aarpon/qute).

## How to install

```bash
$ conda create -n qute-api-env python=3.11  # or 3.10
$ conda activate qute-api-env
$ git clone https://github.com/aarpon/qute_api /path/to/qute_api
$ cd /path/to/qute_api
$ python -m pip install -e .
$ pip install -r dev-requirements.txt
```

## How to run

```bash
$ cd qute_api/qute_api
```

* Copy `config.ini.template` to `config.ini` and set the `MODELS_DIR` variable to point to the models collection. The description of the models collection structure will follow soon.

```bash
$ export FLASK_APP=qute_api/app.py; flask run
```

To test, point your browser to http://127.0.0.1:5000.

To get a list of modes: `/models`

To get a list of versions of a specific model: `/models/<model_name>`

To download a specific model and version: `/models/<model_name>/<model_version>`

To download the hyper-parameters YAML file: `/models/<model_name>/<model_version>/hparams`

## Example client

See `qute_api/qute_client/example.py`.
