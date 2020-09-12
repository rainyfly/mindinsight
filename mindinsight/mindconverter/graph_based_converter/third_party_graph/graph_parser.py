# Copyright 2020 Huawei Technologies Co., Ltd.All Rights Reserved.
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
"""Third party graph parser."""
import os
from .base import GraphParser


class PyTorchGraphParser(GraphParser):
    """Define pytorch graph parser."""

    @classmethod
    def parse(cls, model_path: str):
        """
        Parser pytorch graph.

        Args:
            model_path (str): Model file path.

        Returns:
            object, torch model.
        """
        import torch

        if not os.path.exists(model_path):
            raise FileNotFoundError("`model_path` must be assigned with "
                                    "an existed file path.")

        if torch.cuda.is_available():
            model = torch.load(f=model_path)
        else:
            model = torch.load(f=model_path, map_location="cpu")

        return model