# Description of the Endgoal of the Refactoring

- All agents are isolated in their own files and folders
- Every agent can be invoked separately and independently of others
- Uniformed data structure for inputs and outputs
- Orchestration is not done "internally" by agents and instead is handled by a central orchestrator (LangGraph)
- Context Collection for each agent is done beforehand, so the agents themselves have better instructions, context and don't need to do the heavy lifting themselves (still can research if unclear)
- Templates/Data/Workflows are 100% decoupled and defined. This ensures that the context each agent get fed can be preprocessed in order to get better and more uniform results (this also ensures we can work on refining the context outside the agent)
- Agents are now in a blackbox format. This ensures we can work in the future on isolated parts without breaking the whole system.

Prototype will be build in `.docs/prototype` directory.

