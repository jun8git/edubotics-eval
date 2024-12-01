import os
import json
from literalai import LiteralClient
from trulens.providers.openai import OpenAI


def calculate_groundedness(context, response):
    print("Calculating groundedness...")
    return(provider.groundedness_measure_with_cot_reasons(context, response)[0])

def calculate_context_relevance(question, context):
    print("Calculating context relevance...")
    return(provider.context_relevance(question, context))

def calculate_answer_relevance(question, response):
    print("Calculating answer relevance...")
    return(provider.relevance(question, response))

def calculate_scores(generation_log_file):
    # Read the JSON log file
    with open(generation_log_file, 'r', encoding='utf-8') as f:
        log_data = json.load(f)

    generations = log_data.get("data", [])

    # Loop through each generation and calculate scores
    for generation in generations:
        # Safely extract context, question, and response from the log
        context = (generation.get("variables", {}) or {}).get("context", [{}])[0].get("content", "")
        question = (generation.get("variables", {}) or {}).get("input", [{}])[0].get("content", "")
        response = (generation.get("messageCompletion", {}) or {}).get("content", "")

        # Calculate scores using the TruLens feedback functions
        try:
            groundedness = calculate_groundedness(context, response)

            literal_client.api.create_score(
                step_id=generation["id"],
                name="groundedness",
                type="AI",
                value=groundedness,
            )

        except Exception as e:
            groundedness = -1  # Default value if calculation fails
            print(f"Error calculating groundedness: {e}")

        try:
            context_relevance = calculate_context_relevance(question, context)

            literal_client.api.create_score(
                step_id=generation["id"],
                name="context-relevancy",
                type="AI",
                value=context_relevance,
            )

        except Exception as e:
            context_relevance = -1  # Default value if calculation fails
            print(f"Error calculating context relevance: {e}")

        try:
            answer_relevance = calculate_answer_relevance(question, response)

            literal_client.api.create_score(
                step_id=generation["id"],
                name="answer-relevance",
                type="AI",
                value=answer_relevance,
            )

        except Exception as e:
            answer_relevance = -1  # Default value if calculation fails
            print(f"Error calculating answer relevance: {e}")

        # Print or store the scores
        print(f"Groundedness: {groundedness}, Context Relevance: {context_relevance}, Answer Relevance: {answer_relevance}")

# Example usage
if __name__ == "__main__":
    literal_client = LiteralClient(api_key=os.environ["CD_AI_TUTOR_LITERAL_AI_API_KEY"])
    # Initialize the OpenAI provider for feedback functions
    provider = OpenAI(api_key = os.environ["CD_AI_TUTOR_OPEN_AI_API_KEY"], model_engine = "gpt-4o")
    log_file = "../logs/generations_9.json"
    calculate_scores(log_file)
