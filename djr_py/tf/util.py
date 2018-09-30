from tensorflow.python.client import device_lib


# lists available gpu devices
def get_available_gpus():
    devices = device_lib.list_local_devices()
    return [d.name for d in devices if d.device_type == 'GPU']
