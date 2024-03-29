# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.user.adapter.grpc.stream_pb2 as stream__pb2


class StreamServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GeneratedContentStream = channel.unary_stream(
                '/pb.StreamService/GeneratedContentStream',
                request_serializer=stream__pb2.Request.SerializeToString,
                response_deserializer=stream__pb2.Response.FromString,
                )
        self.VideoContentStream = channel.unary_stream(
                '/pb.StreamService/VideoContentStream',
                request_serializer=stream__pb2.VideoRequest.SerializeToString,
                response_deserializer=stream__pb2.Response.FromString,
                )


class StreamServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GeneratedContentStream(self, request, context):
        """Focus point method
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VideoContentStream(self, request, context):
        """video content method
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StreamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GeneratedContentStream': grpc.unary_stream_rpc_method_handler(
                    servicer.GeneratedContentStream,
                    request_deserializer=stream__pb2.Request.FromString,
                    response_serializer=stream__pb2.Response.SerializeToString,
            ),
            'VideoContentStream': grpc.unary_stream_rpc_method_handler(
                    servicer.VideoContentStream,
                    request_deserializer=stream__pb2.VideoRequest.FromString,
                    response_serializer=stream__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pb.StreamService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StreamService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GeneratedContentStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/pb.StreamService/GeneratedContentStream',
            stream__pb2.Request.SerializeToString,
            stream__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VideoContentStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/pb.StreamService/VideoContentStream',
            stream__pb2.VideoRequest.SerializeToString,
            stream__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
