# Handoffs

Handoffs allow an agent to delegate tasks to another agent. This is useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that handles specific tasks. 

Handoffs are represented as tools to the LLM. So if there is a handoff to an agent named `Refund_Agent`, the tool would be called `transfer_to_refund_agent`.


## Creating a Handoff

All agents have `handoffs` param, which can either take an Agent directly, or a `Handoff` object that customizes the Handoff. 

```python
   billin_agent = Agent(name="Billing Agent")
   refund_agent = Agent(name="Refund Agent")

   triage_agent = Agent(
      name = "Triage Agent",
      handoffs=[billing_agent, refund_agent]
   )
```