def find_task_by_id(task_id: int, tasks: list):
    for task in tasks:
        if task['id'] == task_id:
            return task 
    return None


def find_task_index(task: dict, tasks: list):
    for i in range(len(tasks)):
        if tasks[i] == task:
            return i
    return None