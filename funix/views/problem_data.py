from django.http import HttpResponse, Http404
from judge.models.problem import Problem
from judge.models.problem_data import ProblemData, ProblemTestCase
from django.conf import settings
from pathlib import Path
from django.utils._os import safe_join
import yaml
from functools import reduce
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import get_object_or_404
from django.urls import reverse

@login_required
def beta_update_problem_data(request, problem):
    if not request.user.is_superuser: 
        raise Http404

    problem_object = get_object_or_404(Problem, code=problem)
    if not problem_object.is_editable_by(request.user):
        raise Http404

    problem_data_root = settings.DMOJ_PROBLEM_DATA_ROOT
    data_dir = Path(safe_join(problem_data_root, problem))
    init_yml_file = Path(safe_join(data_dir, 'init.yml'))
    data_loaded = ''
    pretest_test_cases = []
    test_cases = []
    cases = []

    
    if data_dir.is_dir() and init_yml_file.is_file():
        with open(init_yml_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            glob_output_limit = data_loaded.get('output_limit')
            glob_output_prefix = data_loaded.get('output_prefix')
            glob_points = data_loaded.get('points')
            
            problem_data, created = ProblemData.objects.get_or_create(problem=problem_object)
            if data_loaded.get('archive') is not None:
                archive_path = Path(safe_join(data_dir, data_loaded.get('archive')))
                
                if archive_path.is_file():
                    problem_data.zipfile.name = os.path.join(problem, data_loaded.get('archive'))
                    problem_data.save()

            if data_loaded.get('pretest_test_cases') is not None: 
                def add_is_pretest(case):
                    case['is_pretest'] = True
                    return case
                    
                pretest_test_cases = list(map(add_is_pretest, data_loaded.get('pretest_test_cases')))

            if data_loaded.get('test_cases') is not None: 
                def add_is_not_pretest(case):
                   case['is_pretest'] = False
                   return case
                    
                test_cases = list(map(add_is_not_pretest, data_loaded.get('test_cases')))
                
            cases = pretest_test_cases + test_cases
            
            # reducing for in case there are batched test cases
            def reducer(acc, case):
                if (case.get('batched')) is not None:
                    batched_points = case.get('points')
                    batched_is_pretest = case.get('is_pretest')
                    
                    if case.get('output_prefix') is None:
                        batched_output_prefix = glob_output_prefix
                        
                    if case.get('output_limit') is None:
                        batched_output_limit = case.get('glob_output_limit')
                    
                    batched_start  = {
                        'type': 'S',
                        'points': batched_points,
                        'is_pretest': batched_is_pretest,
                        'output_limit': batched_output_limit,
                        'output_prefix': batched_output_prefix
                    }
                    
                    batched_end = {
                        'type': 'E',
                        'is_pretest': batched_is_pretest,
                    }
                    
                    def mapper(sub_case):
                        sub_case['is_pretest'] = batched_is_pretest
                        sub_case['type'] = 'C'

                        if sub_case.get('output_prefix') is None:
                              sub_case['output_prefix'] = batched_output_prefix

                        if sub_case.get('output_limit') is None:
                              sub_case['output_limit'] = batched_output_prefix
                        return sub_case
                    
                    sub_cases = list(map(mapper, case.get('batched')))
                    
                    return acc + [batched_start] + sub_cases + [batched_end]
                else:
                    case['type'] = 'C'
                    if case.get("points") is None:
                        case['points'] = glob_points
                        
                    if case.get("output_limit") is None:
                        case['output_limit'] = glob_output_limit

                    if case.get("output_prefix") is None:
                        case['output_prefix'] = glob_output_prefix
                        
                    return acc + [case]
            
            cases = list(reduce(reducer, cases, []))
            
            def add_order(case_and_index):
                index, case = case_and_index
                case['order'] = index + 1
                return case

            cases = list(map(add_order, enumerate(cases)))
            
            
            ProblemTestCase.objects.filter(dataset=problem_object).delete()
            
            for case in cases: 
                test_case = ProblemTestCase.objects.create( \
                                                dataset=problem_object, \
                                                order=case.get('order'), \
                                                type=case.get('type'), \
                                                is_pretest=case.get('is_pretest') \
                                                )

                if case.get('in') is not None:
                    test_case.input_file = case.get('in')
                    
                if case.get('out') is not None:
                    test_case.output_file = case.get('out')
                    
                if case.get('points') is not None:
                    test_case.points = case.get('points')

                if case.get('output_prefix') is not None:
                    test_case.output_prefix = case.get('output_prefix')
                    
                if case.get('output_limit') is not None:
                    test_case.output_limit = case.get('output_limit')                    
           
                if case.get('generator_args') is not None:
                    test_case.generator_args = case.get('generator_args')  
                    
                test_case.save()            
   
            if data_loaded.get('generator') is not None:
                # generator
                # generator_args >>> no need
                pass
            



    html = '<h1>Problem [{}] was updated</h1>'.format(problem)
    html += '<ul>'
    for case in cases: 
        html += '<li>{}</li>'.format(case)
    
    html += '</ul>'
    
    html += "<a href='{}'><<< back</a>".format(reverse('problem_detail', kwargs={"problem": problem}))
    
    return HttpResponse(html)
    
                    
