# EPICS-MCP-Server
[![smithery badge](https://smithery.ai/badge/@Jacky1-Jiang/EPICS-MCP-Server)](https://smithery.ai/server/@Jacky1-Jiang/EPICS-MCP-Server)

# Overview
- The EPICS MCP Server is a Python-based server designed to interact with EPICS (Experimental Physics and Industrial Control System) process variables (PVs). It provides a set of tools to retrieve PV values, set PV values, and fetch detailed information about PVs. The server is built 
  using the mcp framework and communicates over stdio, making it suitable for integration into larger control systems or workflows.

- This tool is particularly useful in environments where EPICS PVs are used for monitoring and controlling hardware or software parameters.

# Features
- The EPICS MCP Server provides the following tools:

1. **get_pv_value**
   - Create or update a single file in a repository
   - Inputs:
     - `pv_name` (string): The name of the PV variable.
   - Returns: A JSON object containing the status (`success` or `error`) and the retrieved value or an error message.

2. **set_pv_value**
   - Set a new value for a specified PV.
   - Inputs:
     - `pv_name` (string): The name of the PV variable.
     - `pv_value` (string): The new value to be set for the PV.
   - Returns: A JSON object containing the status (`success` or `error`) and a confirmation message or an error message.

3. **get_pv_info**
   - Fetches detailed information about a specified PV.
   - Inputs:
     - `pv_name` (string): The name of the PV variable.
   - Returns: A JSON object containing the status (`success` or `error`) and the detailed information about the PV or an error message.

# Usage with Langchain
- To use this with Langchain, you must install the dependencies required for the project.
```python
pip install -r requirements.txt
```

- ### Langchain

```python
server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["/path/server.py"],
)
```
- ### EPICS
- Before using the EPCIS mcp server, you must successfully install EPCIS on your local machine, ensure that IOC can start normally, and verify that functions such as `caget`, `caput`, and `cainfo` are working properly. For detailed installation instructions, please refer to [https://epics-controls.org/resources-and-support/base/](https://epics-controls.org/resources-and-support/base/).
```python
jiangyan@DESKTOP-84CO9VB:~$ softIoc -d ~/EPICS/DB/test.db
Starting iocInit
############################################################################
## EPICS R7.0.8
## Rev. 2025-02-13T14:29+0800
## Rev. Date build date/time:
############################################################################
iocRun: All initialization complete
epics>
```
```python
jiangyan@DESKTOP-84CO9VB:~$ caget temperature:water
temperature:water              88
jiangyan@DESKTOP-84CO9VB:~$ caput temperature:water 100
Old : temperature:water              88
New : temperature:water              100
jiangyan@DESKTOP-84CO9VB:~$ cainfo temperature:water
temperature:water
    State:            connected
    Host:             127.0.0.1:5056
    Access:           read, write
    Native data type: DBF_DOUBLE
    Request type:     DBR_DOUBLE
    Element count:    1

```
  
# Test Result
- Mcp client:
```python
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "To query the value of a PV (Process Variable) named temperature:water"})
            return agent_response
)
```



- Result:
 ```python
================================[1m Human Message [0m=================================

To query the value of a PV (Process Variable) named temperature:water
==================================[1m Ai Message [0m==================================
Tool Calls:
  get_pv_value (call_vvbXwi51CyYUxEM0hcyvCFCY)
 Call ID: call_vvbXwi51CyYUxEM0hcyvCFCY
  Args:
    pv_name: temperature:water
=================================[1m Tool Message [0m=================================
Name: get_pv_value

{
  "status": "success",
  "value": 88.0
}
==================================[1m Ai Message [0m==================================

The current value of the PV named `temperature:water` is 88.0.
```


