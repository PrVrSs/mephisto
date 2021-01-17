import logging

from mephisto.cfa import CFG
from mephisto.worker import worker
from mephisto.logger import configure_logging


logger = logging.getLogger(__name__)


def branch_as_line(branches):
    return ', '.join(f'{start} -> {end}' for start, end in branches)


class Coverage:
    def __init__(self, branches):
        self._branches = set(branches)
        self._visited = set()

    def new_cov(self, cov):
        if new_cov := cov - self._visited:
            self.add_cov(new_cov)

            return True

        return False

    def add_cov(self, cov):
        logging.debug(f'new_path: {cov}')
        self._visited.update(cov)

    def diff(self, cov):
        return self._branches - set(cov)

    def miss(self):
        return self._branches - self._visited

    def total(self):
        return len(self._visited) / len(self._branches) * 100


class CorpusEngine:
    def __init__(self, branches):
        self._coverage = Coverage(branches)

    def __iter__(self):
        return self

    def __next__(self):
        return 1

    def add(self, data):
        self.analytic(list(data.trace_data.values())[0])

    def analytic(self, trace_data):
        if self._coverage.new_cov(set(trace_data)):
            logger.debug(f'coverage {self._coverage.total()}%')
            logger.debug(f'miss cov: {branch_as_line(self._coverage.miss())}')


class Native:

    def __init__(self, target, executor):
        self._target = target
        self._executor = executor
        self._corpus_engine = CorpusEngine(branches=CFG().create(target).as_line())

    def start(self):
        for seed in self._corpus_engine:
            worker_result = self._executor(seed, __callback__=self._target)
            self._corpus_engine.add(worker_result)
            break


def main():
    configure_logging('debug')

    def simple(data):
        if data == 1:
            a = 7 / 0
        else:
            a = 3

        return a

    Native(simple, worker).start()


if __name__ == '__main__':
    main()
