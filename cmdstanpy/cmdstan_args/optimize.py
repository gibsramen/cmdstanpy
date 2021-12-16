"""Arguments for the optimize subcommand"""

from typing import List, Optional

from cmdstanpy.cmdstan_args.cmdstan import RunConfiguration

from .cmdstan import CmdStanArgs
from .util import Method


class OptimizeArgs:
    """Container for arguments for the optimizer."""

    OPTIMIZE_ALGOS = {'bfgs', 'lbfgs', 'newton'}

    def __init__(
        self,
        args: CmdStanArgs,
        algorithm: Optional[str] = None,
        init_alpha: Optional[float] = None,
        iter: Optional[int] = None,
        save_iterations: bool = False,
        tol_obj: Optional[float] = None,
        tol_rel_obj: Optional[float] = None,
        tol_grad: Optional[float] = None,
        tol_rel_grad: Optional[float] = None,
        tol_param: Optional[float] = None,
        history_size: Optional[int] = None,
    ) -> None:

        self.cmdstan_args = args
        self.algorithm = algorithm.lower() if algorithm else None
        self.init_alpha = init_alpha
        self.iter = iter
        self.save_iterations = save_iterations
        self.tol_obj = tol_obj
        self.tol_rel_obj = tol_rel_obj
        self.tol_grad = tol_grad
        self.tol_rel_grad = tol_rel_grad
        self.tol_param = tol_param
        self.history_size = history_size
        self.thin = None
        self.validate()

    def validate(self) -> None:
        """
        Check arguments correctness and consistency.
        """
        if (
            self.algorithm is not None
            and self.algorithm not in self.OPTIMIZE_ALGOS
        ):
            raise ValueError(
                'Please specify optimizer algorithms as one of [{}]'.format(
                    ', '.join(self.OPTIMIZE_ALGOS)
                )
            )

        if self.init_alpha is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'init_alpha must not be set when algorithm is newton'
                )
            if isinstance(self.init_alpha, float):
                if self.init_alpha <= 0:
                    raise ValueError('init_alpha must be greater than 0')
            else:
                raise ValueError('init_alpha must be type of float')

        if self.iter is not None:
            if isinstance(self.iter, int):
                if self.iter < 0:
                    raise ValueError('iter must be greater than 0')
            else:
                raise ValueError('iter must be type of int')

        if self.tol_obj is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'tol_obj must not be set when algorithm is newton'
                )
            if isinstance(self.tol_obj, float):
                if self.tol_obj <= 0:
                    raise ValueError('tol_obj must be greater than 0')
            else:
                raise ValueError('tol_obj must be type of float')

        if self.tol_rel_obj is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'tol_rel_obj must not be set when algorithm is newton'
                )
            if isinstance(self.tol_rel_obj, float):
                if self.tol_rel_obj <= 0:
                    raise ValueError('tol_rel_obj must be greater than 0')
            else:
                raise ValueError('tol_rel_obj must be type of float')

        if self.tol_grad is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'tol_grad must not be set when algorithm is newton'
                )
            if isinstance(self.tol_grad, float):
                if self.tol_grad <= 0:
                    raise ValueError('tol_grad must be greater than 0')
            else:
                raise ValueError('tol_grad must be type of float')

        if self.tol_rel_grad is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'tol_rel_grad must not be set when algorithm is newton'
                )
            if isinstance(self.tol_rel_grad, float):
                if self.tol_rel_grad <= 0:
                    raise ValueError('tol_rel_grad must be greater than 0')
            else:
                raise ValueError('tol_rel_grad must be type of float')

        if self.tol_param is not None:
            if self.algorithm == 'newton':
                raise ValueError(
                    'tol_param must not be set when algorithm is newton'
                )
            if isinstance(self.tol_param, float):
                if self.tol_param <= 0:
                    raise ValueError('tol_param must be greater than 0')
            else:
                raise ValueError('tol_param must be type of float')

        if self.history_size is not None:
            if self.algorithm == 'newton' or self.algorithm == 'BFGS':
                raise ValueError(
                    'history_size must not be set when algorithm is '
                    'newton or BFGS'
                )
            if isinstance(self.history_size, int):
                if self.history_size < 0:
                    raise ValueError('history_size must be greater than 0')
            else:
                raise ValueError('history_size must be type of int')

    @classmethod
    def method(cls) -> Method:
        return Method.OPTIMIZE

    def compose_command(self, rs: RunConfiguration, idx: int) -> List[str]:
        """
        Compose CmdStan command for method-specific non-default arguments.
        """
        cmd = self.cmdstan_args.begin_command(rs, idx)

        cmd.append('method=optimize')
        if self.algorithm:
            cmd.append('algorithm={}'.format(self.algorithm))
        if self.init_alpha is not None:
            cmd.append('init_alpha={}'.format(self.init_alpha))
        if self.tol_obj is not None:
            cmd.append('tol_obj={}'.format(self.tol_obj))
        if self.tol_rel_obj is not None:
            cmd.append('tol_rel_obj={}'.format(self.tol_rel_obj))
        if self.tol_grad is not None:
            cmd.append('tol_grad={}'.format(self.tol_grad))
        if self.tol_rel_grad is not None:
            cmd.append('tol_rel_grad={}'.format(self.tol_rel_grad))
        if self.tol_param is not None:
            cmd.append('tol_param={}'.format(self.tol_param))
        if self.history_size is not None:
            cmd.append('history_size={}'.format(self.history_size))
        if self.iter is not None:
            cmd.append('iter={}'.format(self.iter))
        if self.save_iterations:
            cmd.append('save_iterations=1')

        return cmd
