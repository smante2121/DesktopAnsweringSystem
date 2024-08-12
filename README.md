# Desktop Answering System

## Overview
Welcome to the Desktop Answering System repository. This project is a revised version of the Google Conversation program, designed to run on a desktop using the computer's microphone and speaker. It leverages Deepgram's Speech-to-Text (STT) and Text-to-Speech (TTS) APIs to manage interactions with the user, collecting specific data through a series of questions and responses. The application is intended to serve as an answering system for incoming patients in medical offices, collecting key information before directing the call to the appropriate healthcare provider.

### Features
- **Speech-to-Text Integration:** Utilizes Deepgram's STT API to capture and transcribe user responses.
- **Text-to-Speech Interaction:** Uses Deepgram's TTS API to ask questions and guide the user through the data collection process.
- **Data Validation:** Extracts and validates user responses using custom extraction methods to ensure the accuracy of collected information.
- **Database Integration:** Stores validated responses in a database, making them accessible to healthcare providers for efficient patient identification and care.
- **Error Handling:** If an invalid response is detected, the system prompts the user to repeat the answer, ensuring data accuracy.

### How It Works
- **Question-Response Sequence:** The program asks the user a series of questions using TTS, captures their responses using STT, and validates the information using custom extraction methods.
- **File Management:** Captured responses are stored in a text file, which is then processed to extract valid data. The final, normalized responses are saved in a separate text file and committed to the database.
- **Future Development:** The current version runs on a desktop, but a future version will integrate with Twilio services, enabling the system to be used over the phone.

### Project Structure
- **main.py:** Runs the main logic, managing the question-response sequence and database operations.
- **STT.py:** Handles the implementation of the speech-to-text API.
- **TTS.py:** Manages the implementation of the text-to-speech API.
- **config.py:** Sets up environment variables and configuration settings.
- **database.py:** Handles database creation and insertion of validated responses.
- **extraction.py:** Contains methods for extracting and validating data from transcribed responses.
- **final_transcript.txt:** Stores the raw transcript of the user’s responses.
- **goodinfo.txt:** Contains the final, validated responses after processing.
- **prompt.py:** Contains the list of questions asked by the TTS API.

### Future Work
- **Twilio Integration:** Link the program to Twilio services for use over the phone.
- **Enhanced Validation:** Implement additional validation checks and user confirmation steps.
- **Database Expansion:** Expand the database functionality to accommodate more complex data storage needs.

