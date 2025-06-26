# Guardrails

Guardrails are the safety checks that runs parallel to the agent's execution. They are used for checking and validation of user's input and Agent's output. 
Image we have an expensive model for customer support and we want to restrict users from sending irrelavent prompts like "hi", "hello" etc to the model. We will add an `Input Guardrail` to check the user's input before sending it to the acutal LLM. If the user's input is not correct, the guardrail will check if the input is just a "hi" or "hello", it will stop our Agent Loop and throw an error. This will help us in cost saving. 

There are two types of guardrails:

1. Input Guardrail

2. Output Guardrail

