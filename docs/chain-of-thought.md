Chain of Thought

The process starts with crafting prompts that encourage the model to think through the problem in a step-by-step manner, thus generating the intermediate steps without jumping straight to the final answer. This can be done using different strategies:

1. Explicit instructions
prompt = f"""
Give me a numbered list of all coffee-related words in English from the text below:
Text: <{input_text}>
"""
prompt = f"""
Give me a numbered list of all coffee-related words in English from the text below:
The task requires the following actions:
1 - Translate the given text into English.
2 - List each coffee-related word from the English text.
Text: <{input_text}>
"""


2. Implicit instructions
by appending “Let’s think step by step” to the original question, the model reasons the answer out loud and succeeds.

3. Demonstrative examples
- One-shot prompting involves showing the model one example that is similar to the target task for guidance.
- Few-shot learning works the same as one-shot, but the number of examples given is higher, typically around a hundred. The performance of the model increases linearly with the number of examples.
- Few-shot CoT prompting. In a few-shot CoT, the model is provided with a few examples of problems along with their step-by-step solutions to guide its reasoning process.

- Reference

- https://python.plainenglish.io/zero-shot-few-shot-and-chain-of-thought-prompt-92596a7a1d59
- https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/prompts/examples/chain_of_thought_react.ipynb