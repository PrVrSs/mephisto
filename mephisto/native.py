import logging

from mephisto.cfa import CFG
from mephisto.worker import worker
from mephisto.logger import configure_logging


logger = logging.getLogger(__name__)


class FuzzerInput:
    def __iter__(self):
        return self

    def __next__(self):
        return 1


class Corpus:
    def __init__(self):
        self._data_generator = FuzzerInput()

    @property
    def input(self):
        return self._data_generator

    def analize(self, program_result):
        return

    def _generate_input(self):
        return 1

    def _initial_seed(self):
        return 0

    def feedback(self):
        c = self._initial_seed()

        while True:
            program_result = yield c
            # self.analize(program_result)
            c = self._generate_input()


class CovAnalytic:
    def __init__(self, branches):
        self._total_coverage: int = 0
        self._branches = set(branches)

    def add_cov(self, cov):
        miss = self._branches - set(list(cov.values())[0])

    def calculate(self):
        pass


class Native:

    def __init__(self, target):
        self._corpus = Corpus().feedback()
        self._cov_analytic = CovAnalytic(CFG().create(target).as_line())
        self._target = target

    def start(self):
        for i in range(2):
            worker_result = worker(i, __callback__=self._target)

            logger.debug(str(worker_result))

            self._cov_analytic.add_cov(worker_result.trace_data)


def main():
    configure_logging('debug')

    def simple(data):
        if data == 1:
            a = 7 / 0
        else:
            a = 3

        return a

    Native(simple).start()


if __name__ == '__main__':
    main()
