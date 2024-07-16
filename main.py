from prompt import questions, mistakes
from TTS import text_to_speech
from STT import speech_to_text
from config import TEXT_FILE
from STT import wait_for_activation
from extraction import(
    extract_callback_number,
    extract_is_patient,
    extract_date_of_birth,
    extract_gender,
    extract_state,
    extract_symptom,

)
import asyncio


# List of validation functions corresponding to each question
expected_responses = [
    extract_callback_number,  # Function to validate the first question
    extract_is_patient,  # Function to validate the first question
    extract_date_of_birth,  # Function to validate the second question
    extract_gender,  # Function to validate the fourth question
    extract_state,  # Function to validate the fifth question
    extract_symptom  # Function to validate the sixth question
]


async def main(): # main method to run the question-response sequence
    # clearing any previous data from files
    final_text_file= open(TEXT_FILE, "w")
    final_text_file.close()
    final_text_file= open(TEXT_FILE, "a")

    goodInfo=open("goodInfo.txt", "w")
    goodInfo.close()
    goodInfo=open("goodInfo.txt", "a")
    text_to_speech("Hello, let’s collect some information to expedite your call.")

    for idx, question in enumerate(questions): # Loop through each question

        while True: # Loop until a valid response is received
            print(f"Starting question {idx + 1}: {question}")
            final_text_file.write(question + "\n")

            # Start STT connection asynchronously but not capturing yet
            stt_task = asyncio.create_task(speech_to_text())

            # Call text_to_speech and wait for it to complete
            await asyncio.to_thread(text_to_speech, question)
            print(f"Completed TTS for question {idx + 1}")
            # Signal STT to start capturing
            wait_for_activation.set()

            # Ensure the STT is ready and capturing immediately after TTS completes
            await stt_task
            response = await stt_task

            wait_for_activation.clear()
            print(f"Received response for question {idx + 1}: {response}")


            # Read the captured response from the file
            with open(TEXT_FILE, "r") as file:
                buffer = file.read()
            print(f"Buffer content: {buffer}")


            # Validate the response
            validation_function = expected_responses[idx] # Get the validation function for the question
            extracted_info = validation_function(buffer) # Extract the information from the response
            print(f"Extracted info for question {idx + 1}: {extracted_info}")

            if extracted_info is not None: # Exit the loop if the response is valid
                goodInfo.write(extracted_info + "\n")
                break
            else: # repeat the question if the response is invalid
                print(f"Invalid response for question {idx + 1}. Repeating the question.")
                text_to_speech("Sorry, I didn't catch that, please repeat your answer.")



# Running the main coroutine
if __name__ == "__main__":
    print("Starting the question-response sequence...")
    asyncio.run(main())
    print("Finished all questions.")







