# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Define common utils."""
import os
import stat
from importlib import import_module
from typing import List, Tuple, Mapping

from mindinsight.mindconverter.common.log import logger as log
from mindinsight.mindconverter.graph_based_converter.constant import SEPARATOR_IN_ONNX_OP


def is_converted(operation: str):
    """
    Whether convert successful.

    Args:
        operation (str): Operation name.

    Returns:
        bool, true or false.
    """
    return operation and SEPARATOR_IN_ONNX_OP not in operation


def _add_outputs_of_onnx_model(model, output_nodes: List[str]):
    """
    Add output nodes of onnx model.

    Args:
        model (ModelProto): ONNX model.
        output_nodes (list[str]): Output nodes list.

    Returns:
        ModelProto, edited ONNX model.
    """
    onnx = import_module("onnx")
    for opt_name in output_nodes:
        intermediate_layer_value_info = onnx.helper.ValueInfoProto()
        intermediate_layer_value_info.name = opt_name
        model.graph.output.append(intermediate_layer_value_info)
    return model


def fetch_output_from_onnx_model(model, feed_dict: dict, output_nodes: List[str]):
    """
    Fetch specific nodes output from onnx model.

    Notes:
        Only support to get output without batch dimension.

    Args:
        model (ModelProto): ONNX model.
        feed_dict (dict): Feed forward inputs.
        output_nodes (list[str]): Output nodes list.

    Returns:
        dict, nodes' output value.
    """
    if not isinstance(feed_dict, dict) or not isinstance(output_nodes, list):
        raise TypeError("`feed_dict` should be type of dict, and `output_nodes` "
                        "should be type of List[str].")

    edit_model = _add_outputs_of_onnx_model(model, output_nodes)

    ort = import_module("onnxruntime")
    sess = ort.InferenceSession(path_or_bytes=bytes(edit_model.SerializeToString()))
    fetched_res = sess.run(output_names=output_nodes, input_feed=feed_dict)
    run_result = dict()
    for idx, opt in enumerate(output_nodes):
        run_result[opt] = fetched_res[idx]
    return run_result


def save_code_file_and_report(model_name: str, code_lines: Mapping[str, Tuple],
                              out_folder: str, report_folder: str):
    """
    Save code file and report.

    Args:
        model_name (str): Model name.
        code_lines (dict): Code lines.
        out_folder (str): Output folder.
        report_folder (str): Report output folder.

    """
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    modes = stat.S_IRUSR | stat.S_IWUSR
    modes_usr = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR

    out_folder = os.path.realpath(out_folder)
    if not report_folder:
        report_folder = out_folder
    else:
        report_folder = os.path.realpath(report_folder)

    if not os.path.exists(out_folder):
        os.makedirs(out_folder, modes_usr)
    if not os.path.exists(report_folder):
        os.makedirs(report_folder, modes_usr)

    for file_name in code_lines:
        code, report = code_lines[file_name]
        try:
            with os.fdopen(os.open(os.path.realpath(os.path.join(out_folder, f"{model_name}.py")),
                                   flags, modes), 'w') as file:
                file.write(code)
            with os.fdopen(os.open(os.path.realpath(os.path.join(report_folder,
                                                                 f"report_of_{model_name}.txt")),
                                   flags, stat.S_IRUSR), "w") as rpt_f:
                rpt_f.write(report)
        except IOError as error:
            log.error(str(error))
            log.exception(error)
            raise error


def lib_version_satisfied(current_ver: str, mini_ver_limited: str,
                          newest_ver_limited: str = ""):
    """
    Check python lib version whether is satisfied.

    Notes:
        Version number must be format of x.x.x, e.g. 1.1.0.

    Args:
        current_ver (str): Current lib version.
        mini_ver_limited (str): Mini lib version.
        newest_ver_limited (str): Newest lib version.

    Returns:
        bool, true or false.
    """
    required_version_number_len = 3
    if len(list(current_ver.split("."))) != required_version_number_len or \
            len(list(mini_ver_limited.split("."))) != required_version_number_len or \
            (newest_ver_limited and len(newest_ver_limited.split(".")) != required_version_number_len):
        raise ValueError("Version number must be format of x.x.x.")
    if current_ver < mini_ver_limited or (newest_ver_limited and current_ver > newest_ver_limited):
        return False
    return True


def get_dict_key_by_value(val, dic):
    """
    Return the first appeared key of a dictionary by given value.

    Args:
        val (Any): Value of the key.
        dic (dict): Dictionary to be checked.

    Returns:
        Any, key of the given value.
    """
    for d_key, d_val in dic.items():
        if d_val == val:
            return d_key
    return None
