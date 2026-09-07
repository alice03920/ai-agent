import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        if args.verbose and response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message

        # Add the assistant's response/tool request to conversation history
        messages.append(message)

        # If the model wants to use tools
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(
                    tool_call,
                    verbose=args.verbose,
                )

                if not result_message["content"]:
                    raise Exception("Function call returned empty content")

                if args.verbose:
                    print(f"-> {result_message['content']}")

                # Give the tool result back to the model
                messages.append(result_message)

            # Loop again so the model can see the tool results
            continue

        # No tool calls = model has finished
        print("Final response:")
        print(message.content)
        return

    print("Reached maximum iterations (20). Agent may not have completed the task.")


if __name__ == "__main__":
    main()
