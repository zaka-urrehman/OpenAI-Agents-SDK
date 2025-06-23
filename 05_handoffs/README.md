# Handoffs

Handoffs allow an agent to delegate tasks to another agent. This is useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that handles specific tasks. 

Handoffs are represented as tools to the LLM. So if there is a handoff to an agent named `Refund_Agent`, the tool would be called `transfer_to_refund_agent`.


## Creating a Handoff

All agents have `handoffs` param, which can either take an Agent directly, or a `Handoff` object that customizes the Handoff. 

```python
   billing_agent = Agent(name="Billing Agent")
   refund_agent = Agent(name="Refund Agent")

   triage_agent = Agent(
      name = "Triage Agent",
      handoffs=[billing_agent, refund_agent]
   )
```

In this example, the `triage_agent` assesses the user's input and delegates the task to the appropriate specialist agent.

Note:

Triage AI agents are artificial intelligence systems designed to assess, categorize, and prioritize tasks, ensuring that the most critical issues receive immediate attention. By automating the initial evaluation process, these agents enhance efficiency and accuracy across various sectors. 


## Customization of Handoffs using the `handoff()` function

The `handoff()` function lets you customize things.

**Example:**
```python
   from agents import Agent, handoff
   
   refund_agent = Agent(name="Refund Agent")
    
   custom_handoff = handoff(
      agent = refund_agent,
      tool_name_override="custom_refund_handoff",
      tool_description_override="Handles refund processes with customized parameters."
   )

   triage_agent = Agent(
      name = "Triage Agent",
      handoffs=[custom_handoff]
   )
```

[see more about customization using `handoff()`](<https://openai.github.io/openai-agents-python/handoffs/#:~:text=(refund_agent)%5D)-,Customizing%20handoffs%20via%20the%20handoff()%20function,-The%20handoff()>)