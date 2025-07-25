import asyncio
import copy
import jsonpatch
from pydantic import BaseModel

from llama_index.core.workflow import Context
from llama_index.llms.openai import OpenAI
from llama_index.protocols.ag_ui.router import get_ag_ui_workflow_router
from llama_index.protocols.ag_ui.events import StateDeltaWorkflowEvent, StateSnapshotWorkflowEvent

class Step(BaseModel):
    description: str

class Task(BaseModel):
    steps: list[Step]

# Genrative UI demo
async def run_task(
    ctx: Context, task: Task,
) -> str:
    """Execute any list of steps needed to complete a task. Useful for anything the user wants to do."""
    state = await ctx.get("state", default={})
    task = Task.model_validate(task)

    state = {
        "steps": [
            {
                "description": step.description,
                "status": "pending"
            }
            for step in task.steps
        ]
    }

    # Send initial state snapshot
    ctx.write_event_to_stream(
        StateSnapshotWorkflowEvent(
            snapshot=state
        )
    )

    # Sleep for 1 second
    await asyncio.sleep(1.0)

    # Create a copy to track changes for JSON patches
    previous_state = copy.deepcopy(state)

    # Update each step and send deltas
    for i, step in enumerate(state["steps"]):
        step["status"] = "completed"
        
        # Generate JSON patch from previous state to current state
        patch = jsonpatch.make_patch(previous_state, state)
        
        # Send state delta event
        ctx.write_event_to_stream(
            StateDeltaWorkflowEvent(
                delta=patch.patch
            )
        )
        
        # Update previous state for next iteration
        previous_state = copy.deepcopy(state)
        
        # Sleep for 1 second
        await asyncio.sleep(1.0)

    # Optionally send a final snapshot to the client
    ctx.write_event_to_stream(
        StateSnapshotWorkflowEvent(
            snapshot=state
        )
    )

    return "Done!"


agentic_generative_ui_router = get_ag_ui_workflow_router(
    llm=OpenAI(model="gpt-4.1"),
    frontend_tools=[run_task],
    initial_state={},
    system_prompt=(
        "You are a helpful assistant that can help the user with their task. "
        "If the user asks you to do any task, use the run_task tool to do it. "
        "Use your best judgement to describe the steps."
    )
)
