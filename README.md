# I Wanna Be a Wizard

### Envrionments
```
$ python -m pip install virtualenv
$ python -m virtualenv venv
$ venv\Scripts\activate
(venv)$ python -m pip install -r requirements.txt
```

### For generate protobuf source codes, 
> [Download Protocol Buffers](https://developers.google.com/protocol-buffers/docs/downloads) \
> [GRPC Documents](https://grpc.io/docs/languages/python/basics/)

> For python
```
(venv)$ pip install grpcio-tools
(venv)$ python -m grpc_tools.protoc -I=./proto/ --python_out=. --grpc_python_out=. ./proto/wizard_system.proto
```
> For csharp
```
$ protoc -I=./proto/ --csharp_out=csharp ./proto/wizard_system.proto
```
> Start server
```
(venv)$ python wizard_system_server.py
```

# TODO:


# Release:


