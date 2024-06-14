import os
import re
import google.generativeai as genai
import datetime

# Api key
api_key = ""
genai.configure(api_key=api_key)

def generate_text(prompt):
    """
    Generates text using the Google Gemini API.

    Args:
        prompt (str): The input prompt for text generation.

    Returns:
        str: The generated text response.
    """
    try:
        response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
        return response
    except Exception as e:
        return f"Error generating text: {str(e)}"

def remove_timestamps(filename):
    """
    This function reads a .vtt file, removes lines starting with specific timestamps,
    and saves the processed text to a new .txt file with "_notimecodes" appended.

    Args:
        filename: The name of the .vtt file (including the .vtt extension).

    Returns:
        str: The path to the processed text file.
    """

    # Get the absolute path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the complete file path for input and output
    input_path = os.path.join(script_dir, filename)
    # Replace the extension with .txt for the output filename
    output_path = os.path.splitext(input_path)[0] + f"_notimecodes_{timestamp}.txt"  

    # Regular expression to match lines starting with 00:, 01:, or 02:
    pattern = r"(00|01|02):"

    try:
        # Open the file in read mode
        with open(input_path, 'r') as file:
            text = file.read()

        # Split the text by lines
        lines = text.splitlines()

        # Remove empty lines and lines matching the pattern
        filtered_lines = [line for line in lines if line and not re.match(pattern, line)]

        # Join the lines back together with no spaces
        final_text = ''.join(filtered_lines)

        # Open the output file in write mode (overwrites existing file)
        with open(output_path, 'w') as output_file:
            output_file.write(final_text)

        print(f"Processed text saved to: {output_path}")
        return output_path

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def summarize_text(file_path):
    """
    Reads the content of a .txt file and generates a summary using the generate_text function.

    Args:
        file_path (str): The path to the .txt file.

    Returns:
        str: The generated summary.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            prompt = "summarize into 500 words with main points. " + content
            summary = generate_text(prompt)
            return summary
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."



# Example usage (replace 'your_file.vtt' with your actual file name)
#filename = 'WWDC 2024 — June 10 ｜ Apple [RXeOiIDNNek].en-US.vtt'
filename = 'musk.txt'
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

processed_file_path = remove_timestamps(filename)
# Save the summary to a file with the timestamp in the filename
filename_output = f'{filename}_generated_text_{timestamp}.txt'

if processed_file_path:
    summary = summarize_text(processed_file_path).text
    # Get the current time and format it as a string


    print(summary)
    with open(filename_output, 'w') as file:
      file.write(summary)
    print(f"Summary saved to {filename_output}")
