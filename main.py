from prompt import questions
from TTS import text_to_speech
from STT import speech_to_text
from config import TEXT_FILE
from extraction import(
    extract_is_patient,
    extract_date_of_birth,
    extract_last_name_letters,
    extract_gender,
    extract_state,
    extract_symptom,

)
import asyncio



# List of validation functions corresponding to each question
expected_responses = [
    extract_is_patient,  # Function to validate the first question
    extract_date_of_birth,  # Function to validate the second question
    extract_last_name_letters,  # Function to validate the third question
    extract_gender,  # Function to validate the fourth question
    extract_state,  # Function to validate the fifth question
    extract_symptom  # Function to validate the sixth question
]


async def main():
    final_text_file= open(TEXT_FILE, "w")
    final_text_file.close()
    final_text_file= open(TEXT_FILE, "a")

    goodInfo=open("goodInfo.txt", "w")
    goodInfo.close()
    goodInfo=open("goodInfo.txt", "a")

    for idx, question in enumerate(questions):

        while True:
            print(f"Starting question {idx + 1}: {question}")
            final_text_file.write(question + "\n")
            # Call text_to_speech and wait for it to complete
            await asyncio.to_thread(text_to_speech, question)
            print(f"Completed TTS for question {idx + 1}")


            # Call speech_to_text and wait for the user's response
            response = await speech_to_text()
            print(f"Received response for question {idx + 1}: {response}")

            # Read the captured response from the file
            with open(TEXT_FILE, "r") as file:
                buffer = file.read()
            print(f"Buffer content: {buffer}")


            # Validate the response

            validation_function = expected_responses[idx]
            extracted_info = validation_function(buffer)
            print(f"Extracted info for question {idx + 1}: {extracted_info}")

            if extracted_info is not None:
                goodInfo.write(extracted_info + "\n")

                break # Exit the loop if the response is valid
            else:
                print(f"Invalid response for question {idx + 1}. Repeating the question.")



# Running the main coroutine
if __name__ == "__main__":
    print("Starting the question-response sequence...")
    asyncio.run(main())
    print("Finished all questions.")

