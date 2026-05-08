import os, argparse, sys

from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_ITERS

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Now we can access `args.user_prompt`
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERS):
        try:
            # call the model, handle responses, etc.
            response = generate_content(client, messages, args.verbose)

            if response is None:
                # generate_content already printed an error; exit
                sys.exit(1)

            # check response.function_calls to decide if we need to continue.
            # If the model produced a final text response (no function calls), we're done
            if not response.function_calls:
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations {MAX_ITERS} reached with no final response produced") # If the maximum number of iterations is reached and the model still hasn't produced a final response, print a message explaining what went wrong.
    sys.exit(1) # You may also want to exit the program with a code of 1 to indicate failure.


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)



    if not response.function_calls:
        print("Response:")
        print(response.text)
        return response # return the response

    # Process function calls
    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts # Checks that result.parts is non‑empty,
            or not result.parts[0].function_response  # that the first part is a function_response,
            or not result.parts[0].function_response.response # and that it has a response field.
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}") # Raises RuntimeError if anything is missing.
        if verbose: #  When verbose is True
            print(f"-> {result.parts[0].function_response.response}") # prints -> {response} for each function call.
        function_responses.append(result.parts[0]) # Appends each result to a function_responses list

    # Append the model's message (the one that contains the function calls to history)
    messages.append(response.candidates[0].content)
    # Append the user's function responses
    messages.append(types.Content(role="user", parts=function_responses))

    return response # now returns response for both branches

if __name__ == "__main__":
    main()
