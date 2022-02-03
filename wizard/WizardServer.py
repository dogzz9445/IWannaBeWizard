
from concurrent import futures
import logging
from pyexpat import model

import grpc
import wizard_system_pb2
import wizard_system_pb2_grpc

from magic_classifier import MagicClassifier
from magic_converter import MagicConverter

class WizardSystemServicer(wizard_system_pb2_grpc.WizardServiceServicer):
    def __init__(self, model_path: str):
        if not model_path:
            model_path = 'model/model_classification'
        self.magic_classifier = MagicClassifier(model_path)
        
    def PostMagicImageRaw(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = MagicConverter.resize_image_from_bytes(request.imageData, (request.height, request.width), (299, 299))
        pred = self.magic_classifier.predict(resized_image)
        magic_type = MagicConverter.get_shape_type(pred)
        return wizard_system_pb2.Magic(type=magic_type)

    def PostMagicImagePng(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = MagicConverter.resize_image_from_png(request.imageData, (request.height, request.width), (299,  299))
        pred = self.magic_classifier.predict(resized_image)
        magic_type = MagicConverter.get_shape_type(pred)
        return wizard_system_pb2.Magic(type=magic_type)

class WizardServer:
    def __init__(self, model_path: str):
        if not model_path:
            model_path = 'model/model_classification'
        self.model_path = model_path        

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        wizard_system_pb2_grpc.add_WizardServiceServicer_to_server(WizardSystemServicer(self.model_path), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    server = WizardServer('model/model_classification')
    server.run()
    