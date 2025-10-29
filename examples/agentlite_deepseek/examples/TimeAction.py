import os


from agentlite.actions.BaseAction import BaseAction
from datetime import date, datetime

class TimeAction(BaseAction):
    def __init__(self) -> None:
        action_name = "Time_Act"
        action_desc = "Using this action to get time."
        params_doc = {"query": "the search string. be simple."}
        super().__init__(
            action_name=action_name, action_desc=action_desc, params_doc=params_doc,
        )

    def __call__(self, query):
        results = query
        return results

class CurDateAction(BaseAction):
    def __init__(self) -> None:
        action_name = "CurDate_Act"
        action_desc = "Using this action to get current date."
        params_doc = {"query": "the search string. be simple."}
        super().__init__(
            action_name=action_name, action_desc=action_desc, params_doc=params_doc,
        )

    def __call__(self, query):
        results = date.today()
        return str(results)
    
class CurTimeAction(BaseAction):
    def __init__(self) -> None:
        action_name = "CurTime_Act"
        action_desc = "Using this action to get current time."
        params_doc = {""}
        super().__init__(
            action_name=action_name, action_desc=action_desc, params_doc=params_doc,
        )

    def __call__(self, query):
        results = datetime.now()
        return results
