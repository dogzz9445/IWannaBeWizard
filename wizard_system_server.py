
from concurrent import futures
import logging

import grpc
import wizard_system_pb2
import wizard_system_pb2_grpc

from magic_classifier import MagicClassifier
from magic_converter import MagicConveter

class WizardSystemServicer(wizard_system_pb2_grpc.WizardServiceServicer):
    
    def __init__(self):
        self.magic_classifier = MagicClassifier('model/model_classification_20220116')
        
    def PostMagicImageRaw(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = MagicConveter.resize_image_from_bytes(request.imageData, (request.height, request.width), (299, 299))
        pred = self.magic_classifier.predict(resized_image)
        magic_type = MagicConveter.get_shape_type(pred)
        return wizard_system_pb2.Magic(type=magic_type)

    def PostMagicImagePng(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wizard_system_pb2_grpc.add_WizardServiceServicer_to_server(WizardSystemServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    