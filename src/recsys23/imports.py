from config import (
    _FLAX,
    _GLUONAUTO,
    _GLUONCV,
    _GLUONNLP,
    _GLUONTS,
    _JAX,
    _MXNET,
    _TF,
    _TF_GPU,
    _TORCH,
    _TORCHVISION,
    _TORCHLIGHTNING,
)
from utils.import_utils import is_installed

INSTALLED_MODULES = {
    module: is_installed(module)
    for module in (_TF, _TF_GPU,
                   _TORCH, _TORCHVISION, _TORCHLIGHTNING,
                   _JAX, _FLAX,
                   _MXNET, _GLUONCV, _GLUONNLP, _GLUONTS, _GLUONAUTO
                   )
}

_LOGURU_INSTALLED = is_installed("loguru")

def package_installed(pkg_name: str):
    """

    :param pkg_name:
    :return:
    """

    if INSTALLED_MODULES[pkg_name]:
        print(f"{pkg_name} installed.")
    else:
        print(f"{pkg_name} not installed.")


# EOF
