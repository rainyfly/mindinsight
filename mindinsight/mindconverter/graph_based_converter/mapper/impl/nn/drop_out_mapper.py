# Copyright 2021 Huawei Technologies Co., Ltd.All Rights Reserved.
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
from mindinsight.mindconverter.graph_based_converter.mapper.base import ONNXToMindSporeMapper


class DropoutMapper(ONNXToMindSporeMapper):
    """Dropout mapper."""

    @staticmethod
    def _operation_name_in_ms(*args, **kwargs):
        return "nn.Dropout"

    @staticmethod
    def _convert_params(**kwargs):
        params = kwargs["params"]
        if params.get("training_mode", False):
            ratio = 1.0 - params.get('ratio', 0.5)
        else:
            ratio = 1.0
        return {'keep_prob': ratio}

    @staticmethod
    def _convert_trained_weights(**kwargs):
        return dict()
