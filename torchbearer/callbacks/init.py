import torchbearer
from torchbearer import cite
from torchbearer.callbacks import Callback

import torch.nn.init as init

__kaiming__ = """
@inproceedings{he2015delving,
  title={Delving deep into rectifiers: Surpassing human-level performance on imagenet classification},
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={Proceedings of the IEEE international conference on computer vision},
  pages={1026--1034},
  year={2015}
}"""

__xavier__ = """
@inproceedings{glorot2010understanding,
  title={Understanding the difficulty of training deep feedforward neural networks},
  author={Glorot, Xavier and Bengio, Yoshua},
  booktitle={Proceedings of the thirteenth international conference on artificial intelligence and statistics},
  pages={249--256},
  year={2010}
}
"""


class WeightInit(Callback):
    """Base class for weight initialisations. Performs the provided function for each module when on_init is
    called.

    Args:
        initialiser (lambda): a function which initialises an nn.Module **inplace**
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised

    State Requirements:
        - :attr:`torchbearer.state.MODEL`: Model should have the `modules` method if modules is None
    """
    def __init__(self, initialiser=lambda module: module, modules=None, targets=['Conv', 'Linear', 'Bilinear']):
        self.initialiser = initialiser
        self.modules = modules
        self.targets = targets

    def on_init(self, state):
        if self.modules is None:
            self.modules = state[torchbearer.MODEL].modules()

        for m in self.modules:
            if len(list(filter(lambda target: target in m.__class__.__name__, self.targets))) > 0:
                self.initialiser(m)


@cite(__kaiming__)
class KaimingNormal(WeightInit):
    """Kaiming Normal weight initialisation. Uses ``torch.nn.init.kaiming_normal_`` on the ``weight`` attribute of the
    filtered modules.

    Args:
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised

    See:
        `PyTorch kaiming_normal_ <https://pytorch.org/docs/stable/nn.html#torch.nn.init.kaiming_normal_>`_
    """
    def __init__(self, a=0, mode='fan_in', nonlinearity='leaky_relu', modules=None,
                 targets=['Conv', 'Linear', 'Bilinear']):
        def initialiser(module):
            init.kaiming_normal_(module.weight.data, a=a, mode=mode, nonlinearity=nonlinearity)

        super(KaimingNormal, self).__init__(initialiser, modules=modules, targets=targets)


@cite(__kaiming__)
class KaimingUniform(WeightInit):
    """Kaiming Uniform weight initialisation. Uses ``torch.nn.init.kaiming_uniform_`` on the ``weight`` attribute of the
    filtered modules.

    Args:
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised

    See:
        `PyTorch kaiming_uniform_ <https://pytorch.org/docs/stable/nn.html#torch.nn.init.kaiming_uniform_>`_
    """
    def __init__(self, a=0, mode='fan_in', nonlinearity='leaky_relu', modules=None,
                 targets=['Conv', 'Linear', 'Bilinear']):
        def initialiser(module):
            init.kaiming_uniform_(module.weight.data, a=a, mode=mode, nonlinearity=nonlinearity)

        super(KaimingUniform, self).__init__(initialiser, modules=modules, targets=targets)


@cite(__xavier__)
class XavierNormal(WeightInit):
    """Xavier Normal weight initialisation. Uses ``torch.nn.init.xavier_normal_`` on the ``weight`` attribute of the
    filtered modules.

    Args:
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised

    See:
        `PyTorch xavier_normal_ <https://pytorch.org/docs/stable/nn.html#torch.nn.init.xavier_normal_>`_
    """
    def __init__(self, gain=1, modules=None, targets=['Conv', 'Linear', 'Bilinear']):
        def initialiser(module):
            init.xavier_normal_(module.weight.data, gain=gain)

        super(XavierNormal, self).__init__(initialiser, modules=modules, targets=targets)


@cite(__xavier__)
class XavierUniform(WeightInit):
    """Xavier Uniform weight initialisation. Uses ``torch.nn.init.xavier_uniform_`` on the ``weight`` attribute of the
    filtered modules.

    Args:
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised

    See:
        `PyTorch xavier_uniform_ <https://pytorch.org/docs/stable/nn.html#torch.nn.init.xavier_uniform_>`_
    """
    def __init__(self, gain=1, modules=None, targets=['Conv', 'Linear', 'Bilinear']):
        def initialiser(module):
            init.xavier_uniform_(module.weight.data, gain=gain)

        super(XavierUniform, self).__init__(initialiser, modules=modules, targets=targets)


class ZeroBias(WeightInit):
    """Zero initialisation for the ``bias`` attributes of filtered modules. This is recommended for use in conjunction
    with weight initialisation schemes.

    Args:
        modules (Iterable[nn.Module] or nn.Module, optional): an iterable of nn.Modules or a
            single nn.Module that will have weights initialised, otherwise this is retrieved from the model
        targets (list[String]): A list of lookup strings to match which modules will be initialised
    """
    def __init__(self, modules=None, targets=['Conv', 'Linear', 'Bilinear']):
        def initialiser(module):
            module.bias.data.zero_()

        super(ZeroBias, self).__init__(initialiser, modules=modules, targets=targets)