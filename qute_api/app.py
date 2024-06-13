# ******************************************************************************
# Copyright © 2022 - 2024, ETH Zurich, D-BSSE, Aaron Ponti
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License Version 2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0.txt
#
# Contributors:
#   Aaron Ponti - initial API and implementation
# ******************************************************************************

import configparser
import sys
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

# Initialize application
app = Flask(__name__)

# Read the configuration file
config = configparser.ConfigParser()
config_file_path = Path(__file__).parent / "config.ini"
if not config_file_path.is_file():
    print("config.ini not found!")
    sys.exit(1)

config.read(Path(__file__).parent / "config.ini")

# Get the models directory from the configuration file
MODELS_DIR = config.get("settings", "MODELS_DIR", fallback="/tmp")

# Turn MODELS_DIR into a pathlib.Path
MODELS_DIR = Path(MODELS_DIR)

# Make sure thr MODELS_DIR exists
if not MODELS_DIR.is_dir():
    raise IOError(f"The models directory {MODELS_DIR} does not exist.")


@app.route("/", methods=["GET"])
def landing_page():
    """Landing page."""
    return "Welcome to <b>qute-api</b>!"


@app.route("/models", methods=["GET"])
def list_models():
    """List all models and their versions."""
    models = {}
    if MODELS_DIR.exists() and MODELS_DIR.is_dir():
        for model_path in sorted(MODELS_DIR.iterdir()):
            if model_path.is_dir() and model_path.name != ".git":
                versions = {}
                for version_path in sorted(model_path.iterdir()):
                    if version_path.is_dir():
                        files = sorted(
                            [
                                file.name
                                for file in version_path.iterdir()
                                if file.is_file()
                            ]
                        )
                        versions[version_path.name] = files
                models[model_path.name] = versions
        sorted_models = {k: models[k] for k in sorted(models)}
        return jsonify(sorted_models)
    else:
        return jsonify({"error": "Models directory not found"}), 404


@app.route("/models/<model_name>", methods=["GET"])
def list_model_versions(model_name):
    """List all versions of a specified model."""
    model_path = MODELS_DIR / model_name
    if model_path.is_dir():
        versions = {}
        for version_path in sorted(model_path.iterdir()):
            if version_path.is_dir():
                files = sorted(
                    [file.name for file in version_path.iterdir() if file.is_file()]
                )
                versions[version_path.name] = files
        return jsonify({model_name: versions})
    else:
        return jsonify({"error": "Model not found"}), 404


@app.route("/models/<model_name>/<version>", methods=["GET"])
def download_model(model_name, version):
    """Download a specific version of a model."""
    if version.isdigit():
        version = f"version_{int(version):03}"
    model_version_path = MODELS_DIR / model_name / version
    if model_version_path.is_dir():
        filename = list(model_version_path.glob("*.ckpt"))
        if len(filename) != 1:
            return (
                jsonify(
                    {"error": f"One model checkpoint expected. Found {len(filename)}"}
                ),
                404,
            )
        return send_from_directory(
            str(model_version_path), filename[0].name, as_attachment=True
        )
    else:
        return jsonify({"error": "Model or version not found"}), 404


@app.route("/models/<model_name>/<version>/hparams", methods=["GET"])
def download_model_hparams(model_name, version):
    """Download the hyper-parameters of a specific version of a model."""
    if version.isdigit():
        version = f"version_{int(version):03}"
    model_version_path = MODELS_DIR / model_name / version
    if model_version_path.is_dir():
        filename = model_version_path / "hparams.yaml"
        if not filename.is_file():
            return (
                jsonify({"error": f"Could not find hyper-parameters file"}),
                404,
            )
        return send_from_directory(
            str(model_version_path), filename.name, as_attachment=True
        )
    else:
        return jsonify({"error": "Model or version not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
