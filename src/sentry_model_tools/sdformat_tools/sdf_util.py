import os

MODEL_URI_PREFIX = 'model://'

def _resource_paths():
    """Return model roots at lookup time instead of import time.

    The launch file sets ``SENTRY_MODEL_PATH`` from the new workspace's
    installed resource package. The standard Gazebo variables remain
    supported for standalone use, but no old workspace path is required.
    """
    paths = []
    for variable in (
        "SENTRY_MODEL_PATH",
        "GZ_SIM_RESOURCE_PATH",
        "IGN_GAZEBO_RESOURCE_PATH",
        "GAZEBO_MODEL_PATH",
    ):
        value = os.getenv(variable)
        if value:
            paths.extend(path for path in value.split(":") if path)
    return paths

def get_model_directory(model_name):
    for tmp_dir in _resource_paths():
        model_directory = os.path.join(tmp_dir, model_name)
        if(os.path.isdir(model_directory)):
            return model_directory
    return ""

# get absolute path according to uri
def parse_model_uri(uri):
    if uri.find(MODEL_URI_PREFIX) != 0:
        return ''
    tmp_uri = uri[len(MODEL_URI_PREFIX):]
    pos = tmp_uri.find('/')
    if pos == -1:
        return ''
    model_name = tmp_uri[0:pos]
    model_dir_path = get_model_directory(model_name)
    if model_dir_path == '':
        return ''
    return model_dir_path + tmp_uri[pos:]
