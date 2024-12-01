
# Table of Contents

1.  [Installation](#org058ab1f)
2.  [Usage](#org828fe55)
3.  [Functionality](#orge3223b4)
4.  [Contributing](#orgfe3469e)

Literal AI Generations Downloader & Analyzer

This project provides a Python script for downloading AI generations using the
Literal AI API and analyzing the results by calculating various relevance
metrics.


<a id="org058ab1f"></a>

# Installation

-   Make sure you have Python 3 installed, then install the dependencies with.

    pip install -r requirements.txt

-   Set up your environment variables

    export CD_AI_TUTOR_LITERAL_AI_API_KEY='your-literal-ai-api-key'
    export CD_AI_TUTOR_OPEN_AI_API_KEY='your-openai-api-key'


<a id="org828fe55"></a>

# Usage

-   This script can download AI generations and calculate scores for groundedness
    and relevance.
-   Adjust `--batch_size` to control the number of generations fetched per batch.

    python src/fetch_generations.py --batch_size 50

-   After downloading generations, run the following script to generate and push
    scores to literalai

    python src/generate_scores.py --log_file logs/generations_10.json

-   Make sure you specify the correct path to your generation log file within the
    script.


<a id="orge3223b4"></a>

# Functionality

-   **Download Generations with Pagination:**
    -   Fetches AI generations from the Literal AI API.
    -   Saves the fetched data as JSON files in a specified logs directory.

-   **Score Calculation:**
    -   Calculates groundedness and relevance scores.
    -   Uses OpenAI's feedback functions to determine the quality of AI responses.
    -   Pushes the scores to literalai


<a id="orgfe3469e"></a>

# Contributing

Contributions to enhance this project are welcome! Feel free to fork the
repository and submit pull requests.

