# Copyright 2020-2021 Huawei Technologies Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Mapper module."""
import abc
import importlib
import json
import os
from typing import Dict
from mindconverter.common.log import MindConverterLogger
from mindconverter.graph_based_converter.constant import ExchangeMessageKeywords, TemplateKeywords

# Define global func name.
GET_OP_NAME = "_operation_name_in_ms"
GET_OP_PARAMS = "_convert_params"
GET_OP_WEIGHTS = "_convert_trained_weights"
GET_OP_SETTINGS = "_convert_settings"
GET_OP_TEMPLATE = "_generate_snippet_template"

def get_table(framework):
    config_json = f"{framework}_to_ms.json"
    operation_table = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_json)
    table = {}
    if os.path.exists(operation_table):
        with open(operation_table) as f:
            table = json.load(f)
    return table

def get_module_name(op_name):
    """Get module_name."""
    framework_file = op_name.split("::")[0]
    config_json = f"{framework_file}_to_ms.json"
    operation_table = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_json)
    module_name = None
    if os.path.exists(operation_table):
        with open(operation_table) as f:
            table = json.load(f)
        module_name = table.get(op_name)
    return module_name


class Mapper(metaclass=abc.ABCMeta):
    """Mapper between third-party-operation and MindSpore."""

    @staticmethod
    @abc.abstractmethod
    def _operation_name_in_ms(*args, **kwargs):
        """Corresponding operation name in MindSpore."""

    @staticmethod
    @abc.abstractmethod
    def _convert_params(**kwargs):
        """Convert third party operation's param into MindSpore operation."""

    @staticmethod
    @abc.abstractmethod
    def _convert_trained_weights(**kwargs):
        """Convert third party operation's weights into MindSpore operation."""

    @classmethod
    @abc.abstractmethod
    def convert(cls, op_name: str, params: Dict, weights: Dict = None):
        """Convert third party operation's param into MindSpore operation."""

    @staticmethod
    @abc.abstractmethod
    def _generate_snippet_template(**kwargs):
        """Generate code template according to node info."""


class ONNXToMindSporeMapper(Mapper, abc.ABC):
    """ONNX operation to MindSpore."""

    @classmethod
    def convert(cls, op_name: str, params: Dict, weights: Dict = None):
        """
        Convert third party operation's param into MindSpore operation.

        Args:
            op_name (str): Operation name in ONNX.
            params (dict): Params in onnx.
            weights (dict): Weights in onnx.

        Returns:
            Tuple[str, dict, dict], operation name and params and settings.
        """
        module_name = get_module_name(op_name)

        if not module_name:
            code_template, exchange_msg, outputs_list, outputs_mapping = cls._generate_snippet_template(
                operation=op_name,
                params=params,
                weights=weights
            )
            return code_template, exchange_msg, outputs_list, outputs_mapping

        pos = module_name.rfind(".")
        try:
            converter = getattr(importlib.import_module(module_name[:pos]),
                                module_name[pos + 1:])
            op_name_converter = getattr(converter, GET_OP_NAME)
            params_converter = getattr(converter, GET_OP_PARAMS)
            weights_converter = getattr(converter, GET_OP_WEIGHTS)
            template_generator = getattr(converter, GET_OP_TEMPLATE)
        except (ModuleNotFoundError,) as e:
            # If mapper can not be found, then skip it.
            err_msg = f"Converting {op_name} failed, see {str(e)}"
            MindConverterLogger.error(err_msg)
            code_template, exchange_msg, outputs_list, outputs_mapping = cls._generate_snippet_template(
                operation=op_name,
                params=params,
                weights=weights
            )
            return code_template, exchange_msg, outputs_list, outputs_mapping

        try:
            converter_name = op_name_converter(params=params, weights=weights, op_name=op_name)
            converted_params = params_converter(params=params, weights=weights)

            if "input_shape" in converted_params:
                converted_params.pop("input_shape")
            if "output_shape" in converted_params:
                converted_params.pop("output_shape")
            # set to converted_weights to enable weight migration
            converted_weights = weights_converter(params=params, weights=weights) if weights else dict()
            code_template, exchange_msg, outputs_list, outputs_mapping = template_generator(
                operation=converter_name,
                converted_params=converted_params,
                raw_params=params,
                weights=weights,
                trainable_params=converted_weights
            )

        except (AttributeError, KeyError, ValueError, TypeError, IndexError) as e:
            err_msg = f"Converting {op_name} failed, see {str(e)}"
            MindConverterLogger.error(err_msg)
            code_template, exchange_msg, outputs_list, outputs_mapping = template_generator(
                operation=op_name,
                params=params,
                weights=weights
            )

        return code_template, exchange_msg, outputs_list, outputs_mapping

    @staticmethod
    def _operation_name_in_ms(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _convert_params(**kwargs):
        raise NotImplementedError

    @staticmethod
    def _convert_trained_weights(**kwargs):
        raise NotImplementedError

    @staticmethod
    def _generate_exchange_msg(**kwargs):
        """Generate exchange msg."""
        exchange_msg = {
            kwargs["variable_slot"]: {
                ExchangeMessageKeywords.VariableScope.value.OPERATION.value: kwargs.get("op"),
                ExchangeMessageKeywords.VariableScope.value.VARIABLE_NAME.value: None,
                ExchangeMessageKeywords.VariableScope.value.OUTPUT_TYPE.value:
                    ExchangeMessageKeywords.VariableScope.value.TSR_TYPE.value,
                ExchangeMessageKeywords.VariableScope.value.INPUTS.value: [],
                ExchangeMessageKeywords.VariableScope.value.ARGS.value: kwargs.get("args"),
                ExchangeMessageKeywords.VariableScope.value.WEIGHTS.value: kwargs.get("weights", dict()),
                ExchangeMessageKeywords.VariableScope.value.TRAINABLE_PARAMS.value:
                    kwargs.get("trainable_params", dict())
            }
        }
        return exchange_msg

    @staticmethod
    def _generate_snippet_template(**kwargs):
        op = kwargs.get("operation").replace("::", ".")
        args = kwargs.get("converted_params", dict())
        weights = kwargs.get("weights")
        trainable_params = kwargs.get("trainable_params", dict())
        if not op:
            raise ValueError("Can not get MindSpore operation name.")
        variable_slot = "var_0"
        init_template = f"self.{{{variable_slot}}} = {op}({', '.join(['%s={%s}' % (p, p) for p in args])})"
        construct_template = f"opt_{{{variable_slot}}} = self.{{{variable_slot}}}" \
                             f"({{{ExchangeMessageKeywords.VariableScope.value.INPUTS.value}}})"
        template = {
            variable_slot: {
                TemplateKeywords.INIT.value: [init_template],
                TemplateKeywords.CONSTRUCT.value: [construct_template]
            }
        }
        exchange_msg = ONNXToMindSporeMapper._generate_exchange_msg(variable_slot=variable_slot, op=op, args=args,
                                                                    weights=weights, trainable_params=trainable_params)
        outputs_list = [f"opt_{{{variable_slot}}}"]
        outputs_mapping = ((0, 0),)
        return template, exchange_msg, outputs_list, outputs_mapping

    @staticmethod
    def _find_val_by_index(loc_index, weights_list, default_val=None):
        """Find value by location index of weights_list."""
        result = default_val
        if loc_index < 0:
            return weights_list[loc_index].value

        for idx, weight in enumerate(weights_list):
            if idx == loc_index:
                result = weight.value
                break
        return result

    @staticmethod
    def _generate_snippet_template_for_math_operation(**kwargs):
        """Generate code snippet for math operation."""
        op = kwargs.get("operation").replace("onnx::", "onnx.")
        args = kwargs.get("converted_params", dict())
        if not op:
            raise ValueError("Can not get MindSpore operation name.")
        variable_slot = "var_0"
        construct_template = f"opt_{{{variable_slot}}} = {op}()" \
                             f"({{{ExchangeMessageKeywords.VariableScope.value.INPUTS.value}}})"
        template = {
            variable_slot: {
                TemplateKeywords.INIT.value: [],
                TemplateKeywords.CONSTRUCT.value: [construct_template]
            }
        }
        exchange_msg = ONNXToMindSporeMapper._generate_exchange_msg(variable_slot=variable_slot, op=op, args=args)
        outputs_list = [f"opt_{{{variable_slot}}}"]
        outputs_mapping = ((0, 0),)
        return template, exchange_msg, outputs_list, outputs_mapping

    @staticmethod
    def _find_location_by_index(loc_index, weights_list):
        """Find weight location in inputs of Node."""
        result = -1
        if loc_index < 0:
            return weights_list[loc_index].location

        for idx, weight in enumerate(weights_list):
            if idx == loc_index:
                result = weight.location
                break
        return result

    @staticmethod
    def _find_onnx_name_by_index(loc_index, weights_list):
        """Find weight onnx name in inputs of Node."""
        result = -1
        if loc_index < 0:
            return weights_list[loc_index].name

        for idx, weight in enumerate(weights_list):
            if idx == loc_index:
                result = weight.name
                break
        return result