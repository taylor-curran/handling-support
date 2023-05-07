feature_request = """
Hi T,

 

Following up on our discussion today about the Prefect sub-flow run feature we would like to replicate:

 

As you know, we sometimes have large flows with many tasks, and our tasks do not actually pass data between them, they are linked via dependencies only. We have the need to do the following under some situations: run a subset of the tasks in a flow (identified by task_name) while maintaining the dependency structure (essentially skipping all other tasks).

 

In Prefect 1, we were able  to do this by the custom context argument when we start a flow run:

1.       Pass in the list of task names as a flow run context


2.       Have a state-handler that does the following:
“If new state =Running and task_name not in context.list_of_tasks_to_run: skip”

3.       The end result is a DAG that maintains the dependency between tasks while skipping unwanted tasks:


 

In Prefect 2, our best shot on replicating this behavior is to use a flow argument, still named “partial_run_tasks”, and the process looks the following:

1.       User specify a list of task names in the custom deployment run of the flow

2.       Wrap each task’s fn with the following wrapper:

3.       def partial_flow_run_wrapper(task_name, fn) -> Callable:

    def _partial_flow_run_wrapper(*args, **kwargs):
        flow_run_ctx = get_flow_run_ctx_from_client()
        if flow_run_ctx:
            parameters = flow_run_ctx.flow_run.parameters
            list_of_tasks_covered = parameters.get('LIST_OF_TASKS')
            if list_of_tasks_covered:
                if task_name not in list_of_tasks_covered:
                    return dummy_task_fn(*args, **kwargs)
        return fn(*args, **kwargs)

    return _partial_flow_run_wrapper

4.       In the end, this approach was able to turn unwanted task runs to a no-op, but it has the following shortfalls:

a.       The task will still end in a complete state, making it impossible to distinguish “skipped” and actual task runs

                                                               i.      This is troublesome both in th UI and for calculating stats like avg runtime

                                                             ii.      We could force the task’s state to skipped using custom on_complete function, but it seems like there is currently no skipped state in Prefect 2 L

 

 

As we discussed in our previous emails on this feature (from 1.0 to 2.0 age), although the DAG in Prefect 2 is dynamic at run time, our need to having partial flow runs that can contain  an arbitrary of tasks is not scalable with other approaches like if-else statement in the flow code. Having features like below could be helpful for our migration:

1.       Add a Skipped state

2.       Make an on_running hook, which we could use to avoid getting this task into a running state in the first place

3.       Have some partial flow run support on the Prefect side in-house (always nice J )

 

Please let me know if this makes sense, happy to provide more context if necessary. Again, thanks for helping out with all the feature requests I generated J

 

Regards,

D
"""

tech_question = """
We have noticed that flow runs will start backing up as late and will not flow through our work queue until the concurrency limit is increased. 

This is weird though because there are not running or pending flow runs that would be taking up spots on the queue.
( I have tried searching through the UI with the time as far back as possible, and I have used the python client's api calls to search for running flow runs, neither has shown any )

We also have an automation that is designed to cancel flows when they have been running for too long, it appears to be working just fine.



Here is a picture of our queue backing up even though there is nothing running or pending in it.




Only once I jump the concurrency limit up to something high does it start running again.
Why is there a problem if there are no flow runs clogging the queue?
"""

# end