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
"""
Function:
    Test query debugger restful api.
Usage:
    pytest tests/st/func/debugger/test_restful_api.py
"""
import os

import pytest

from mindinsight.conf import settings
from tests.st.func.debugger.conftest import DEBUGGER_BASE_URL
from tests.st.func.debugger.mock_ms_client import MockDebuggerClient
from tests.st.func.debugger.utils import check_waiting_state, get_request_result, \
    send_and_compare_result


def send_terminate_cmd(app_client):
    """Send terminate command to debugger client."""
    url = os.path.join(DEBUGGER_BASE_URL, 'control')
    body_data = {'mode': 'terminate'}
    send_and_compare_result(app_client, url, body_data)


class TestAscendDebugger:
    """Test debugger on Ascend backend."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls._debugger_client = MockDebuggerClient(backend='Ascend')

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_before_train_begin(self, app_client):
        """Test retrieve all."""
        url = 'retrieve'
        body_data = {'mode': 'all'}
        expect_file = 'before_train_begin.json'
        send_and_compare_result(app_client, url, body_data, expect_file)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'mode': 'all'}, 'retrieve_all.json'),
        ({'mode': 'node', 'params': {'name': 'Default'}}, 'retrieve_scope_node.json'),
        ({'mode': 'node', 'params': {'name': 'Default/optimizer-Momentum/Parameter[18]_7'}},
         'retrieve_aggregation_scope_node.json'),
        ({'mode': 'node', 'params': {
            'name': 'Default/TransData-op99',
            'single_node': True}}, 'retrieve_single_node.json'),
        ({'mode': 'watchpoint_hit'}, 'retrieve_empty_watchpoint_hit_list')
    ])
    def test_retrieve_when_train_begin(self, app_client, body_data, expect_file):
        """Test retrieve when train_begin."""
        url = 'retrieve'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)

    def test_get_conditions(self, app_client):
        """Test get conditions for ascend."""
        url = '/v1/mindinsight/conditionmgr/train-jobs/train-id/conditions'
        body_data = {}
        expect_file = 'get_conditions_for_ascend.json'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file, method='get', full_url=True)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'mode': 'all'}, 'multi_retrieve_all.json'),
        ({'mode': 'node', 'params': {'name': 'Default', 'graph_name': 'graph_1'}}, 'retrieve_scope_node.json'),
        ({'mode': 'node', 'params': {'name': 'graph_0'}}, 'multi_retrieve_scope_node.json'),
        ({'mode': 'node', 'params': {'name': 'graph_0/Default/optimizer-Momentum/Parameter[18]_7'}},
         'multi_retrieve_aggregation_scope_node.json'),
        ({'mode': 'node', 'params': {
            'name': 'graph_0/Default/TransData-op99',
            'single_node': True}}, 'multi_retrieve_single_node.json'),
        ({'mode': 'node', 'params': {
            'name': 'Default/TransData-op99',
            'single_node': True, 'graph_name': 'graph_0'}}, 'retrieve_single_node.json')
    ])
    def test_multi_retrieve_when_train_begin(self, app_client, body_data, expect_file):
        """Test retrieve when train_begin."""
        url = 'retrieve'
        debugger_client = MockDebuggerClient(backend='Ascend', graph_num=2)
        with debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_create_and_delete_watchpoint(self, app_client):
        """Test create and delete watchpoint."""
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            conditions = [
                {'id': 'max_gt', 'params': [{'name': 'param', 'value': 1.0, 'disable': False}]},
                {'id': 'max_lt', 'params': [{'name': 'param', 'value': -1.0, 'disable': False}]},
                {'id': 'min_gt', 'params': [{'name': 'param', 'value': 1e+32, 'disable': False}]},
                {'id': 'min_lt', 'params': [{'name': 'param', 'value': -1e+32, 'disable': False}]},
                {'id': 'max_min_gt', 'params': [{'name': 'param', 'value': 0, 'disable': False}]},
                {'id': 'max_min_lt', 'params': [{'name': 'param', 'value': 0, 'disable': False}]},
                {'id': 'mean_gt', 'params': [{'name': 'param', 'value': 0, 'disable': False}]},
                {'id': 'mean_lt', 'params': [{'name': 'param', 'value': 0, 'disable': False}]},
                {'id': 'inf', 'params': []},
                {'id': 'overflow', 'params': []},
            ]
            for idx, condition in enumerate(conditions):
                create_watchpoint(app_client, condition, idx + 1)
            # delete 4-th watchpoint
            url = 'delete_watchpoint'
            body_data = {'watch_point_id': 4}
            get_request_result(app_client, url, body_data)
            # test watchpoint list
            url = 'retrieve'
            body_data = {'mode': 'watchpoint'}
            expect_file = 'create_and_delete_watchpoint.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_update_watchpoint(self, app_client):
        """Test retrieve when train_begin."""
        watch_point_id = 1
        leaf_node_name = 'Default/optimizer-Momentum/Parameter[18]_7/moments.fc3.bias'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            condition = {'id': 'inf', 'params': []}
            create_watchpoint(app_client, condition, watch_point_id)
            # update watchpoint watchpoint list
            url = 'update_watchpoint'
            body_data = {'watch_point_id': watch_point_id,
                         'watch_nodes': [leaf_node_name],
                         'mode': 0}
            get_request_result(app_client, url, body_data)
            # get updated nodes
            url = 'search'
            body_data = {'name': leaf_node_name, 'watch_point_id': watch_point_id}
            expect_file = 'search_unwatched_leaf_node.json'
            send_and_compare_result(app_client, url, body_data, expect_file, method='get')
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_watchpoint_hit(self, app_client):
        """Test retrieve watchpoint hit."""
        with self._debugger_client.get_thread_instance():
            create_watchpoint_and_wait(app_client)
            # check watchpoint hit list
            url = 'retrieve'
            body_data = {'mode': 'watchpoint_hit'}
            expect_file = 'retrieve_watchpoint_hit.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            # check single watchpoint hit
            body_data = {
                'mode': 'watchpoint_hit',
                'params': {
                    'name': 'Default/TransData-op99',
                    'single_node': True,
                    'watch_point_id': 1
                }
            }
            expect_file = 'retrieve_single_watchpoint_hit.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_retrieve_tensor_value(self, app_client):
        """Test retrieve tensor value."""
        node_name = 'Default/TransData-op99'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            # prepare tensor value
            url = 'retrieve_tensor_history'
            body_data = {'name': node_name}
            expect_file = 'retrieve_empty_tensor_history.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            # check full tensor history from poll data
            res = get_request_result(
                app_client=app_client, url='poll_data', body_data={'pos': 0}, method='get')
            assert res.get('receive_tensor', {}).get('node_name') == node_name
            expect_file = 'retrieve_full_tensor_history.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            # check tensor value
            url = 'tensors'
            body_data = {
                'name': node_name + ':0',
                'detail': 'data',
                'shape': '[1, 1:3]'
            }
            expect_file = 'retrieve_tensor_value.json'
            send_and_compare_result(app_client, url, body_data, expect_file, method='get')
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_compare_tensor_value(self, app_client):
        """Test compare tensor value."""
        node_name = 'Default/args0'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            # prepare tensor values
            url = 'control'
            body_data = {'mode': 'continue',
                         'steps': 2}
            get_request_result(app_client, url, body_data)
            check_waiting_state(app_client)
            get_request_result(
                app_client=app_client, url='retrieve_tensor_history', body_data={'name': node_name})
            res = get_request_result(
                app_client=app_client, url='poll_data', body_data={'pos': 0}, method='get')
            assert res.get('receive_tensor', {}).get('node_name') == node_name
            # get compare results
            url = 'tensor-comparisons'
            body_data = {
                'name': node_name + ':0',
                'detail': 'data',
                'shape': '[:, :]',
                'tolerance': 1
            }
            expect_file = 'compare_tensors.json'
            send_and_compare_result(app_client, url, body_data, expect_file, method='get')
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'ascend': True}, 'retrieve_node_by_bfs_ascend.json'),
        ({'name': 'Default/args0', 'ascend': False}, 'retrieve_node_by_bfs.json')
    ])
    def test_retrieve_bfs_node(self, app_client, body_data, expect_file):
        """Test retrieve bfs node."""
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            # prepare tensor values
            url = 'retrieve_node_by_bfs'
            send_and_compare_result(app_client, url, body_data, expect_file, method='get')
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_pause(self, app_client):
        """Test pause the training."""
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            # send run command to execute to next node
            url = 'control'
            body_data = {'mode': 'continue',
                         'steps': -1}
            res = get_request_result(app_client, url, body_data)
            assert res == {'metadata': {'state': 'running', 'enable_recheck': False}}
            # send pause command
            url = 'control'
            body_data = {'mode': 'pause'}
            res = get_request_result(app_client, url, body_data)
            assert res == {'metadata': {'state': 'waiting', 'enable_recheck': False}}
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("url, body_data, enable_recheck", [
        ('create_watchpoint',
         {'condition': {'id': 'inf', 'params': []},
          'watch_nodes': ['Default']}, True),
        ('update_watchpoint',
         {'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum/Parameter[18]_7'],
          'mode': 0}, True),
        ('update_watchpoint',
         {'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum'],
          'mode': 1}, True),
        ('delete_watchpoint', {}, True)
    ])
    def test_recheck(self, app_client, url, body_data, enable_recheck):
        """Test recheck."""
        with self._debugger_client.get_thread_instance():
            create_watchpoint_and_wait(app_client)
            # create watchpoint
            res = get_request_result(app_client, url, body_data, method='post')
            assert res['metadata']['enable_recheck'] is enable_recheck
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_recommend_watchpoints(self, app_client):
        """Test generating recommended watchpoints."""
        original_value = settings.ENABLE_RECOMMENDED_WATCHPOINTS
        settings.ENABLE_RECOMMENDED_WATCHPOINTS = True
        try:
            with self._debugger_client.get_thread_instance():
                check_waiting_state(app_client)
                url = 'retrieve'
                body_data = {'mode': 'watchpoint'}
                expect_file = 'recommended_watchpoints_at_startup.json'
                send_and_compare_result(app_client, url, body_data, expect_file, method='post')
                send_terminate_cmd(app_client)
        finally:
            settings.ENABLE_RECOMMENDED_WATCHPOINTS = original_value

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'tensor_name': 'Default/TransData-op99:0', 'graph_name': 'graph_0'}, 'retrieve_tensor_graph-0.json'),
        ({'tensor_name': 'Default/optimizer-Momentum/Parameter[18]_7/moments.fc1.bias:0', 'graph_name': 'graph_0'},
         'retrieve_tensor_graph-1.json')
    ])
    def test_retrieve_tensor_graph(self, app_client, body_data, expect_file):
        """Test retrieve tensor graph."""
        url = 'tensor-graphs'
        with self._debugger_client.get_thread_instance():
            create_watchpoint_and_wait(app_client)
            get_request_result(app_client, url, body_data, method='GET')
            # check full tensor history from poll data
            res = get_request_result(
                app_client=app_client, url='poll_data', body_data={'pos': 0}, method='get')
            assert res.get('receive_tensor', {}).get('tensor_name') == body_data.get('tensor_name')
            send_and_compare_result(app_client, url, body_data, expect_file, method='GET')
            send_terminate_cmd(app_client)


class TestGPUDebugger:
    """Test debugger on Ascend backend."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls._debugger_client = MockDebuggerClient(backend='GPU')

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_next_node_on_gpu(self, app_client):
        """Test get next node on GPU."""
        gpu_debugger_client = MockDebuggerClient(backend='GPU')
        with gpu_debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            # send run command to get watchpoint hit
            url = 'control'
            body_data = {'mode': 'continue',
                         'level': 'node',
                         'name': 'Default/TransData-op99'}
            res = get_request_result(app_client, url, body_data)
            assert res == {'metadata': {'state': 'running', 'enable_recheck': False}}
            # get metadata
            check_waiting_state(app_client)
            url = 'retrieve'
            body_data = {'mode': 'all'}
            expect_file = 'retrieve_next_node_on_gpu.json'
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("url, body_data, enable_recheck", [
        ('create_watchpoint',
         {'condition': {'id': 'inf', 'params': []},
          'watch_nodes': ['Default']}, True),
        ('create_watchpoint',
         {'condition': {'id': 'inf', 'params': []},
          'watch_nodes': ['Default/TransData-op99']}, True),
        ('update_watchpoint',
         {'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum/Parameter[18]_7'],
          'mode': 0}, True),
        ('update_watchpoint',
         {'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum'],
          'mode': 1}, True),
        ('update_watchpoint',
         [{'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum'],
           'mode': 1},
          {'watch_point_id': 1, 'watch_nodes': ['Default/optimizer-Momentum'],
           'mode': 0}
          ], True),
        ('update_watchpoint',
         [{'watch_point_id': 1, 'watch_nodes': ['Default/TransData-op99'],
           'mode': 0},
          {'watch_point_id': 1, 'watch_nodes': ['Default/TransData-op99'],
           'mode': 1}
          ], True),
        ('delete_watchpoint', {'watch_point_id': 1}, True)
    ])
    def test_recheck_state(self, app_client, url, body_data, enable_recheck):
        """Test update watchpoint and check the value of enable_recheck."""
        with self._debugger_client.get_thread_instance():
            create_watchpoint_and_wait(app_client)
            if not isinstance(body_data, list):
                body_data = [body_data]
            for sub_body_data in body_data:
                res = get_request_result(app_client, url, sub_body_data, method='post')
            assert res['metadata']['enable_recheck'] is enable_recheck
            send_terminate_cmd(app_client)

    def test_get_conditions(self, app_client):
        """Test get conditions for gpu."""
        url = '/v1/mindinsight/conditionmgr/train-jobs/train-id/conditions'
        body_data = {}
        expect_file = 'get_conditions_for_gpu.json'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file, method='get', full_url=True)
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    def test_recheck(self, app_client):
        """Test recheck request."""
        with self._debugger_client.get_thread_instance():
            create_watchpoint_and_wait(app_client)
            # send recheck when disable to do recheck
            get_request_result(app_client, 'recheck', {}, method='post', expect_code=400)
            # send recheck when enable to do recheck
            create_watchpoint(app_client, {'id': 'inf', 'params': []}, 2)
            res = get_request_result(app_client, 'recheck', {}, method='post')
            assert res['metadata']['enable_recheck'] is False

            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("filter_condition, expect_file", [
        ({'name': 'fc', 'node_category': 'weight'}, 'search_weight.json'),
        ({'name': 'fc', 'node_category': 'gradient'}, 'search_gradient.json'),
        ({'node_category': 'activation'}, 'search_activation.json')
    ])
    def test_search_by_category(self, app_client, filter_condition, expect_file):
        """Test recheck request."""
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, 'search', filter_condition, expect_file,
                                    method='get')
            send_terminate_cmd(app_client)


class TestMultiGraphDebugger:
    """Test debugger on Ascend backend."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls._debugger_client = MockDebuggerClient(backend='Ascend', graph_num=2)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'mode': 'all'}, 'multi_retrieve_all.json'),
        ({'mode': 'node', 'params': {'name': 'Default', 'graph_name': 'graph_1'}}, 'retrieve_scope_node.json'),
        ({'mode': 'node', 'params': {'name': 'graph_0'}}, 'multi_retrieve_scope_node.json'),
        ({'mode': 'node', 'params': {'name': 'graph_0/Default/optimizer-Momentum/Parameter[18]_7'}},
         'multi_retrieve_aggregation_scope_node.json'),
        ({'mode': 'node', 'params': {
            'name': 'graph_0/Default/TransData-op99',
            'single_node': True}}, 'multi_retrieve_single_node.json'),
        ({'mode': 'node', 'params': {
            'name': 'Default/TransData-op99',
            'single_node': True, 'graph_name': 'graph_0'}}, 'retrieve_single_node.json')
    ])
    def test_multi_retrieve_when_train_begin(self, app_client, body_data, expect_file):
        """Test retrieve when train_begin."""
        url = 'retrieve'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file)
            send_terminate_cmd(app_client)


    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("filter_condition, expect_file", [
        ({'name': '', 'node_category': 'weight'}, 'search_weight_multi_graph.json'),
        ({'node_category': 'activation'}, 'search_activation_multi_graph.json')
    ])
    def test_search_by_category_with_multi_graph(self, app_client, filter_condition, expect_file):
        """Test search by category request."""
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, 'search', filter_condition, expect_file, method='get')
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("filter_condition, expect_id", [
        ({'condition': {'id': 'inf'},
          'watch_nodes': ['Default/optimizer-Momentum/Parameter[18]_7'],
          'graph_name': 'graph_0'}, 1),
        ({'condition': {'id': 'inf'},
          'watch_nodes': ['graph_0/Default/optimizer-Momentum/ApplyMomentum[8]_1'],
          'graph_name': None}, 1)
    ])
    def test_create_watchpoint(self, app_client, filter_condition, expect_id):
        """Test create watchpoint with multiple graphs."""
        url = 'create_watchpoint'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            res = get_request_result(app_client, url, filter_condition)
            assert res.get('id') == expect_id
            send_terminate_cmd(app_client)

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("params, expect_file", [
        ({'level': 'node'}, 'multi_next_node.json'),
        ({'level': 'node', 'node_name': 'graph_0/Default/TransData-op99'}, 'multi_next_node.json'),
        ({'level': 'node', 'node_name': 'Default/TransData-op99', 'graph_name': 'graph_0'},
         'multi_next_node.json')
    ])
    def test_continue_on_gpu(self, app_client, params, expect_file):
        """Test get next node on GPU."""
        gpu_debugger_client = MockDebuggerClient(backend='GPU', graph_num=2)
        original_value = settings.ENABLE_RECOMMENDED_WATCHPOINTS
        settings.ENABLE_RECOMMENDED_WATCHPOINTS = True
        try:
            with gpu_debugger_client.get_thread_instance():
                check_waiting_state(app_client)
                # send run command to get watchpoint hit
                url = 'control'
                body_data = {'mode': 'continue'}
                body_data.update(params)
                res = get_request_result(app_client, url, body_data)
                assert res == {'metadata': {'state': 'running', 'enable_recheck': False}}
                # get metadata
                check_waiting_state(app_client)
                url = 'retrieve'
                body_data = {'mode': 'all'}
                send_and_compare_result(app_client, url, body_data, expect_file)
                send_terminate_cmd(app_client)
        finally:
            settings.ENABLE_RECOMMENDED_WATCHPOINTS = original_value

    @pytest.mark.level0
    @pytest.mark.env_single
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_gpu_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.parametrize("body_data, expect_file", [
        ({'tensor_name': 'Default/TransData-op99:0', 'graph_name': 'graph_0'}, 'retrieve_tensor_hits-0.json'),
        ({'tensor_name': 'Default/optimizer-Momentum/Parameter[18]_7/moments.fc1.bias:0', 'graph_name': 'graph_0'},
         'retrieve_tensor_hits-1.json')
    ])
    def test_retrieve_tensor_hits(self, app_client, body_data, expect_file):
        """Test retrieve tensor graph."""
        url = 'tensor-hits'
        with self._debugger_client.get_thread_instance():
            check_waiting_state(app_client)
            send_and_compare_result(app_client, url, body_data, expect_file, method='GET')
            send_terminate_cmd(app_client)


def create_watchpoint(app_client, condition, expect_id):
    """Create watchpoint."""
    url = 'create_watchpoint'
    body_data = {'condition': condition,
                 'watch_nodes': ['Default/optimizer-Momentum/Parameter[18]_7',
                                 'Default/optimizer-Momentum/Parameter[18]_7/moments.fc3.bias',
                                 'Default/optimizer-Momentum/Parameter[18]_7/moments.fc1.bias',
                                 'Default/TransData-op99']}
    res = get_request_result(app_client, url, body_data)
    assert res.get('id') == expect_id


def create_watchpoint_and_wait(app_client):
    """Preparation for recheck."""
    check_waiting_state(app_client)
    create_watchpoint(app_client, condition={'id': 'inf', 'params': []}, expect_id=1)
    # send run command to get watchpoint hit
    url = 'control'
    body_data = {'mode': 'continue',
                 'steps': 2}
    res = get_request_result(app_client, url, body_data)
    assert res == {'metadata': {'state': 'running', 'enable_recheck': False}}
    # wait for server has received watchpoint hit
    check_waiting_state(app_client)
