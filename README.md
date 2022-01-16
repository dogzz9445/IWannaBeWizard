# I Wanna Be a Wizard

### Envrionments
```
$ python -m virtualenv venv
$ python -m pip install -r requirements.txt
```

### For generate protobuf source codes, 
> [Download Protocol Buffers](https://developers.google.com/protocol-buffers/docs/downloads) \
> [GRPC Documents](https://grpc.io/docs/languages/python/basics/) \
```
$ pip install grpcio-tools
```
```
$ python -m grpc_tools.protoc -I=./proto/ --python_out=. --grpc_python_out=. ./proto/wizard_system.proto
```

# TODO:


# Release:


