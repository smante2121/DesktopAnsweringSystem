from prompt import questions, extract_yes_or_no, delete_last_line
from TTS import text_to_speech
from STT import speech_to_text
from config import TEXT_FILE
from database import setup_database, insert_response
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

    setup_database() # Set up the database

    # clearing any previous data from files
    final_text_file= open(TEXT_FILE, "w")
    final_text_file.close()
    final_text_file= open(TEXT_FILE, "a")
    # clearing any previous data from files
    goodInfo=open("goodInfo.txt", "w")
    goodInfo.close()
    goodInfo=open("goodInfo.txt", "a")

    text_to_speech("Hello, let’s collect some information to expedite your call.")

    responses = [] # List to store the responses

    for idx, question in enumerate(questions): # Loop through each question

        while True: # Loop until a valid response is received

            print(f"Starting question {idx + 1}: {question}")
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
                # If it's the callback number question, ask for confirmation
                if idx == 0:

                    stt_task = asyncio.create_task(speech_to_text())
                    question = f"You said your callback number is {extracted_info}. Is that correct?"
                    await asyncio.to_thread(text_to_speech, question)
                    wait_for_activation.set()

                    # Ensure the STT is ready and capturing immediately after TTS completes
                    await stt_task
                    response = await stt_task
                    wait_for_activation.clear()
                    confirmation = await stt_task

                    # Read the confirmation response from the file
                    with open(TEXT_FILE, "r") as file:
                        confirmation_buffer = file.read()

                    print(f"Confirmation Buffer content: {confirmation_buffer}")
                    confirmation_result = extract_yes_or_no(confirmation_buffer)

                    if confirmation_result is not None and confirmation_result.lower() == "yes":
                        goodInfo.write(extracted_info + "\n")
                        responses.append(extracted_info)
                        break

                    else:
                        delete_last_line(TEXT_FILE)  # Delete incorrect number
                        continue

                else:
                    goodInfo.write(extracted_info + "\n")
                    responses.append(extracted_info)
                    break

            else: # repeat the question if the response is invalid
                print(f"Invalid response for question {idx + 1}. Repeating the question.")
                text_to_speech("Sorry, I didn't catch that, please repeat your answer.")
                delete_last_line(TEXT_FILE)

    # Insert the responses into the database
    insert_response(*responses[:6])






# Running the main coroutine
if __name__ == "__main__":
    print("Starting the question-response sequence...")
    asyncio.run(main())
    print("Finished all questions.")



