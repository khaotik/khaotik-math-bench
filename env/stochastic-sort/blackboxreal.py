import random,math

__all__ = ['StochasticSortingProblem']

class BlackboxReal:
    __slots__ = ('_value',)
    def __init__(self, init_value:float):
        self._value = init_value
    def __hash__(self):
        return hash((type(self).__name__, self._value))
    def compare(self, other) -> int:
        '''
        has more chance returns 1 if self>other and otherwise -1
        '''
        logit = other._value - self._value
        # to prevent OverflowError 
        p = 0. if (logit > 709.5) else (1. / (1. + math.exp(logit)))
        return random.binomialvariate(1, p)*2-1

class StochasticSortingProblem:
    __slots__ = ('__bbox_list', '__compare_call_count')
    def __init__(self, problem_size:int, seed=None) -> list:
        assert isinstance(problem_size,int) and problem_size>=2
        # sample a list of `BlackboxReal` instance by sampling from i.i.d normal distribution
        old_state = None
        if seed is not None:
            old_state = random.getstate()
            random.seed(seed)
        self.__bbox_list = [BlackboxReal(random.normalvariate()) for _ in range(problem_size)]
        if old_state is not None:
            random.setstate(old_state)
        self.__compare_call_count = 0
    def __len__(self):
        return len(self.__bbox_list)
    def compare(self, i:int, j:int) -> int:
        ''''''
        try:
          ret = self.__bbox_list[i].compare(self.__bbox_list[j])
        except IndexError as e:
            raise IndexError(f'comparison indices {i} and {j} exceeds problem size {len(self.__bbox_list)}')
        self.__compare_call_count += 1
        return ret
    def getCompareCount(self) -> int:
        return self.__compare_call_count
    def clearCompareCount(self):
        self.__compare_call_count = 0
    def getTrueSolution(self):
        '''this function shall ONLY be called by a verifier and NOT a solver'''
        psize = len(self.__bbox_list)
        return list(sorted(range(psize), key=lambda x:self.__bbox_list[x]._value))
