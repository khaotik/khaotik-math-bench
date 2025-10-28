#!/usr/bin/env python
import sys
from dataclasses import dataclass
from blackboxreal import StochasticSortingProblem
from solution import my_solution

def baselineSolution(problem:StochasticSortingProblem, effort:int=100):
    from functools import cmp_to_key
    ret = list(range(len(problem)))
    def pairwiseCompareWithEffort(lhs:int, rhs:int) -> int:
        nonlocal problem, effort
        total = 0
        for _ in range(effort):
            total += problem.compare(lhs, rhs)
        return total
    return list(sorted(ret, key=cmp_to_key(pairwiseCompareWithEffort)))

@dataclass
class BenchmarkResult:
    solver_name:str
    problem_size:int
    sample_size:int
    avg_compare_count:float
    avg_correct_rate:float

def testSolution(fn_solution, sample_size=400, solver_name:str=None):
    if solver_name is None:
        solver_name = fn_solution.__name__
    result_li = []
    for problem_size in [2,3,5,14,42,132]:
        compare_count = 0
        correct_count = 0
        for _ in range(sample_size):
            problem = StochasticSortingProblem(problem_size)
            sol = fn_solution(problem)
            true_sol = problem.getTrueSolution()
            compare_count += problem.getCompareCount()
            if type(sol) is not list:
                continue
            if sol == true_sol:
                correct_count += 1
        avg_compare_count = compare_count / sample_size
        avg_correct_rate = correct_count / sample_size
        result_li.append(BenchmarkResult(
            solver_name=solver_name,
            problem_size=problem_size,
            sample_size=sample_size,
            avg_compare_count=avg_compare_count,
            avg_correct_rate=avg_correct_rate,
        ))
    return result_li

def main():
    baseline_bench_result_list = testSolution(baselineSolution)
    for entry in baseline_bench_result_list:
        print(entry)
    try:
        custom_bench_result_list = testSolution(my_solution)
    except Exception as e:
        print(e, file=sys.stderr)
        print('failed to benchmark custom solution, abort', file=sys.stderr)
        return
    for entry in custom_bench_result_list:
        print(entry)

if __name__ == '__main__':
    main()
