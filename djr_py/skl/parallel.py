import os
import gc
import copyreg
import multiprocessing as mp
from io import BytesIO

from dill import Pickler

from sklearn.externals.joblib import register_parallel_backend
from sklearn.externals.joblib.pool import CustomizablePicklingQueue, MemmapingPool
from sklearn.externals.joblib._parallel_backends import MultiprocessingBackend, FallbackToBackend, SequentialBackend


# extends dill.Pickler
class CustomizablePickler(Pickler):

    def __init__(self, writer, reducers=None):
        Pickler.__init__(self, writer)
        if reducers is None:
            reducers = {}
        if hasattr(Pickler, 'dispatch'):
            # Make the dispatch registry an instance level attribute instead of
            # a reference to the class dictionary under Python 2
            self.dispatch = Pickler.dispatch.copy()
        else:
            # Under Python 3 initialize the dispatch table with a copy of the
            # default registry
            self.dispatch_table = copyreg.dispatch_table.copy()
        for _type, reduce_func in reducers.items():
            self.register(_type, reduce_func)

    def register(self, _type, reduce_func):
        """Attach a reducer function to a given type in the dispatch table."""
        if hasattr(Pickler, 'dispatch'):
            # Python 2 pickler dispatching is not explicitly customizable.
            # Let us use a closure to workaround this limitation.
            def dispatcher(self, obj):
                reduced = reduce_func(obj)
                self.save_reduce(obj=obj, *reduced)
            self.dispatch[_type] = dispatcher
        else:
            self.dispatch_table[_type] = reduce_func


# implement dill-based CustomizablePickler
class CustomizablePicklingQueueDill(CustomizablePicklingQueue):

    def send(self, obj):
        buffer = BytesIO()
        CustomizablePickler(buffer, self._reducers).dump(obj)
        self._writer.send_bytes(buffer.getvalue())

    def _make_methods(self):
        super(CustomizablePicklingQueueDill, self)._make_methods()
        self._send = self.send


# dill-based multiprocessing Pool
# pylint: disable=abstract-method
class PicklingPoolDill(MemmapingPool):

    def _setup_queues(self):
        context = getattr(self, '_ctx', mp)

        # pylint: disable=protected-access
        self._inqueue = CustomizablePicklingQueueDill(context, self._forward_reducers)
        self._outqueue = CustomizablePicklingQueueDill(context, self._backward_reducers)
        self._quick_put = self._inqueue._send
        self._quick_get = self._outqueue._recv


# multiprocesing backend using dill-based PicklingPool
class MultiprocessingBackendDill(MultiprocessingBackend):

    def configure(self, n_jobs=1, parallel=None, **backend_args):
        """Build a process or thread pool and return the number of workers"""
        n_jobs = self.effective_n_jobs(n_jobs)
        if n_jobs == 1:
            raise FallbackToBackend(SequentialBackend())

        already_forked = int(os.environ.get(self.JOBLIB_SPAWNED_PROCESS, 0))
        if already_forked:
            raise ImportError(
                '[joblib] Attempting to do parallel computing '
                'without protecting your import on a system that does '
                'not support forking. To use parallel-computing in a '
                'script, you must protect your main loop using "if '
                "__name__ == '__main__'"
                '". Please see the joblib documentation on Parallel '
                'for more information')

        # Set an environment variable to avoid infinite loops
        os.environ[self.JOBLIB_SPAWNED_PROCESS] = '1'

        # Make sure to free as much memory as possible before forking
        gc.collect()

        # pylint: disable=attribute-defined-outside-init
        self._pool = PicklingPoolDill(n_jobs, **backend_args)
        self.parallel = parallel

        return n_jobs


# set as default backend
def use_dill_mp_backend():
    register_parallel_backend('multiprocessing', MultiprocessingBackendDill, make_default=True)
