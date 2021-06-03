# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from mindinsight.debugger.proto import debug_grpc_pb2 as mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2
from mindinsight.domain.graph.proto import ms_graph_pb2 as mindinsight_dot_domain_dot_graph_dot_proto_dot_ms__graph__pb2


class EventListenerStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.WaitCMD = channel.unary_unary(
                '/debugger.EventListener/WaitCMD',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendMetadata = channel.unary_unary(
                '/debugger.EventListener/SendMetadata',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendGraph = channel.stream_unary(
                '/debugger.EventListener/SendGraph',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendTensors = channel.stream_unary(
                '/debugger.EventListener/SendTensors',
                request_serializer=mindinsight_dot_domain_dot_graph_dot_proto_dot_ms__graph__pb2.TensorProto.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendWatchpointHits = channel.stream_unary(
                '/debugger.EventListener/SendWatchpointHits',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.WatchpointHit.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendMultiGraphs = channel.stream_unary(
                '/debugger.EventListener/SendMultiGraphs',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )
        self.SendHeartbeat = channel.unary_unary(
                '/debugger.EventListener/SendHeartbeat',
                request_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Heartbeat.SerializeToString,
                response_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
                )


class EventListenerServicer(object):
    """Missing associated documentation comment in .proto file"""

    def WaitCMD(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMetadata(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendGraph(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendTensors(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendWatchpointHits(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMultiGraphs(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendHeartbeat(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EventListenerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'WaitCMD': grpc.unary_unary_rpc_method_handler(
                    servicer.WaitCMD,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMetadata,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendGraph': grpc.stream_unary_rpc_method_handler(
                    servicer.SendGraph,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendTensors': grpc.stream_unary_rpc_method_handler(
                    servicer.SendTensors,
                    request_deserializer=mindinsight_dot_domain_dot_graph_dot_proto_dot_ms__graph__pb2.TensorProto.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendWatchpointHits': grpc.stream_unary_rpc_method_handler(
                    servicer.SendWatchpointHits,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.WatchpointHit.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendMultiGraphs': grpc.stream_unary_rpc_method_handler(
                    servicer.SendMultiGraphs,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
            'SendHeartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.SendHeartbeat,
                    request_deserializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Heartbeat.FromString,
                    response_serializer=mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'debugger.EventListener', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EventListener(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def WaitCMD(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/debugger.EventListener/WaitCMD',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/debugger.EventListener/SendMetadata',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Metadata.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendGraph(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/debugger.EventListener/SendGraph',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendTensors(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/debugger.EventListener/SendTensors',
            mindinsight_dot_domain_dot_graph_dot_proto_dot_ms__graph__pb2.TensorProto.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendWatchpointHits(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/debugger.EventListener/SendWatchpointHits',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.WatchpointHit.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMultiGraphs(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/debugger.EventListener/SendMultiGraphs',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Chunk.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendHeartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/debugger.EventListener/SendHeartbeat',
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.Heartbeat.SerializeToString,
            mindinsight_dot_debugger_dot_proto_dot_debug__grpc__pb2.EventReply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
