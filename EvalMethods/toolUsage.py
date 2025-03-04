from Core import EvalMethods
from Utils import to_list
import warnings

class ToolUse(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        if not self.evalinfo.get("tool", None):
            warnings.warn("There is no tool usage.", RuntimeWarning)
        self.tools = to_list(self.evalinfo.get("tool"))
    
    def set_ans(self,ans):
        self.ans=ans

    def eval1(self):
        """
        A method for scoring models based on toolUsage.
        Rule:Suppose there are n prompts in total, unit_point = 1/n, for each prompt, the model gets a score of unit_point * (2/3) if it chooses the correct tool, and it gets a score of unit_point * (1/3) if the model sends the correct arguments.
        Returns:Score of the model.

        """
        unit_point = 1. / len(self.prompt)
        res = 0.
        for ind, pt in enumerate(self.prompt):
            target_tool = self.tools[ind]['name']
            target_arg = self.tools[ind]['args']
            if self.ans[ind].find(f'{target_tool}') != -1:
                res += unit_point * (2/3)
            if self.ans[ind].find(f'{target_arg}') != -1:
                res += unit_point * (1/3)
        return res
    
    def eval2(self):
        """
        A method for scoring models based on toolUsage.
        Rule:Suppose there are n prompts in total, unit_point = 1/n, for each prompt, the model gets a score of unit_point if it both chooses the correct tool and sends the correct arguments.
        Returns:Score of the model.

        """
        unit_point = 1. / len(self.prompt)
        res = 0.
        for ind, pt in enumerate(self.prompt):
            target_tool = self.tools[ind]['name']
            target_arg = self.tools[ind]['args']
            if self.ans[ind].find(f'{target_tool}') != -1 and self.ans[ind].find(f'{target_arg}') != -1:
                res += unit_point
        return res
    
    def score(self,method_num):
        """
        A method for choosing one of the methods in toolUsage to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score.
        The function will return a string like 'The model gets ***{score}*** points in this testcase by toolUsage method.'
        
        """
        eval_dict={1:self.eval1,2:self.eval2}
        eval_method=eval_dict[method_num]
        score=eval_method()
        score_info=f'The model gets ***{score}*** points in this testcase by toolUsage method.'
        return(score_info)
    
    