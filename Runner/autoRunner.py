from Utils import load_from_cfg
from Interactor import AutoInteractor
from TestCase import TestProject
import os
import json
import concurrent.futures
from tqdm import tqdm

class AutoRunner():
    def __init__(self, cfg):
        self.cfg = cfg
        load_from_cfg(self, cfg)
        self._check()
        self.load_json()
        
    def _check(self):
        if not hasattr(self, 'llm'):
            raise ValueError("There is no llm in the configure file.")
        if not hasattr(self, 'json_paths'):
            raise ValueError("There is no json_paths in the configure file.")
        if not hasattr(self, 'interactor'):
            print("Find no interactor, default as auto interactor.")
            self.interactor_cls = AutoInteractor
        if not hasattr(self, 'register_agents'):
            print("Find no registered agents, default is empty list.")
            self.interactor = []
    
    def load_json(self):
        self.testprojects = []
        self.json_paths = [os.path.join('TestCase', x) for x in self.json_paths]
        for jsp in self.json_paths:
            with open(jsp) as f:
                jsonobj = json.load(f)
                self.testprojects.append(TestProject(jsonobj))
    
    def run(self):
        """
        Multi-threaded to run each test file to speed things up
        """
        def run_interactor(testproj, interactor_cls, cfg):
            for testcase in testproj.get_cases(cfg):
                interactor = interactor_cls(testcase)
                interactor.run()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for testproj in self.testprojects:
                future = executor.submit(run_interactor, testproj, self.interactor_cls, self.cfg)
                futures.append(future)

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                result = future.result()
    
    def analyse(self):
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """
        pass