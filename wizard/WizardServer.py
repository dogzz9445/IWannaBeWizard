
from concurrent import futures
import logging
import grpc
from . import *
from .proto import wizard_api_pb2 as Api
from .proto import wizard_api_pb2_grpc as ApiGrpc

class WizardApiServicer(ApiGrpc.WizardServiceServicer):
    def __init__(self, model_path: str):
        if not model_path:
            model_path = 'model/model_classification'
        self.magic_classifier = MagicClassifier(model_path)
        
    def PostMagicImageRaw(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = MagicConverter.resize_image_from_bytes(request.imageData, (request.height, request.width), (299, 299))
        pred = self.magic_classifier.predict(resized_image)
        magic_type = MagicConverter.get_shape_type(pred)
        return Api.Magic(type=magic_type)

    def PostMagicImagePng(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = MagicConverter.resize_image_from_png(request.imageData, (request.height, request.width), (299,  299))
        pred = self.magic_classifier.predict(resized_image)
        magic_type = MagicConverter.get_shape_type(pred)
        return Api.Magic(type=magic_type)

class WizardServer:
    def __init__(self, model_path: str):
        if not model_path:
            model_path = 'model/model_classification'
        self.model_path = model_path 

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ApiGrpc.add_WizardServiceServicer_to_server(WizardApiServicer(self.model_path), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    server = WizardServer('model/model_classification')
    server.run()
    