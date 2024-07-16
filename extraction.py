'''import re


def extract_callback_number(buffer):
    question = "What is your callback number?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    # Extract all sequences of digits from the buffer
    digit_sequences = re.findall(r'\d+', buffer)
    # Join all sequences of digits into a single string
    joined_digits = ''.join(digit_sequences)

    # Find all 10-digit sequences in the joined digits
    matches = re.findall(r'\d{10}', joined_digits)

    if matches:
        # Return the first valid 10-digit phone number formatted correctly
        first_match = matches[0]
        formatted_number = f"({first_match[:3]}) {first_match[3:6]}-{first_match[6:]}"
        return formatted_number

    return None

def extract_is_patient(buffer): # method to extract if the caller is the patient
    question = "Are you the patient?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:].lower() # convert buffer to lowercase for case-insensitive matching

    positive_responses = [
        "yes", "yeah", "i'm the patient", "i am the patient", "yep", "yup", "affirmative", "i am",
    ]

    negative_responses = [
        "no", "nope", "negative", "not the patient", "i am not", "i'm not", "i am not the patient", "i'm not the patient"
    ]

    for response in positive_responses: # check for positive responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "yes"

    for response in negative_responses: # check for negative responses
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "no"

    return None

def extract_date_of_birth(buffer): # method to extract date of birth
    question = "Could you please provide your date of birth?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    month_to_number = { # dictionary to map month names to month numbers
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    # Handle numerical date formats (e.g., 6/21/2003 or 6,212,003)
    match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        return f"{int(month)}/{int(day)}/{year}"

    match = re.search(r'\b(\d{1,2}),\s?(\d{1,3}),\s?(\d{1,4})\b', buffer)
    if match:
        month, day, year = match.groups() # extract month, day, and year
        if len(day) == 1 and len(year) == 4:
            return f"{int(month)}/{int(day)}/{year}"
        elif len(day) == 3 and day[1] == '1' and day[2] == '2':
            return f"{int(month)}/21/{year}"
        else:
            return f"{int(month)}/{int(day)}/{year}" # return formatted date

    # Handle month-day-year with possible ordinal suffixes and optional comma (e.g., June 21st, 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(st|nd|rd|th)?,?\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match: # extract month, day, and year
        month, day, _, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle more generic month-day-year formats without explicit separators (e.g., June 21 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match: # extract month, day, and year
        month, day, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle compact numeric dates without separators (e.g., 6212003)
    match = re.search(r'\b(\d{1})(\d{2})(\d{4})\b', buffer)
    if match: # extract month, day, and year
        month, day, year = match.groups()
        if year[0] in ['1', '2']:
            return f"{int(month)}/{int(day)}/{year}"

    return None

def extract_gender(buffer):
    question = "Got it. Are you a biological male or female?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    male_pattern = r'\b(male|boy|man)\b'
    female_pattern = r'\b(female|girl|woman)\b'

    # Look for patterns in the response
    male_matches = re.findall(male_pattern, buffer, re.IGNORECASE)
    female_matches = re.findall(female_pattern, buffer, re.IGNORECASE)

    if female_matches:
        return "female"
    elif male_matches:
        return "male"

    return None

def extract_state(buffer): # method to extract the state LOCATION
    question = "What state are you in right now?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
              "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    for state in states: # check for each state in the list
        if re.search(r'\b' + re.escape(state) + r'\b', buffer, re.IGNORECASE):
            return state
    return None

def extract_symptom(buffer): # method to extract the reason for the call
    question = "Perfect. In a few words, please tell me your main symptom or reason for the call today."
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    pattern = r'[\.\!\?]\s*(.*?)[\.\!\?]'
    match = re.search(pattern, buffer, re.IGNORECASE)
    if match:
        response = match.group(1).strip()
        return response
    return None '''
import re

def extract_callback_number(buffer):
    question = "What is your callback number?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    # Extract all sequences of digits from the buffer
    digit_sequences = re.findall(r'\d+', buffer)
    # Join all sequences of digits into a single string
    joined_digits = ''.join(digit_sequences)

    # Find all 10-digit sequences in the joined digits
    matches = re.findall(r'\d{10}', joined_digits)

    if matches:
        # Return the first valid 10-digit phone number formatted correctly
        first_match = matches[0]
        formatted_number = f"({first_match[:3]}) {first_match[3:6]}-{first_match[6:]}"
        return formatted_number

    return None

def extract_is_patient(buffer):
    question = "Are you the patient?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:].lower()  # convert buffer to lowercase for case-insensitive matching

    positive_responses = [
        "yes", "yeah", "i'm the patient", "i am the patient", "yep", "yup", "affirmative", "i am",
    ]

    negative_responses = [
        "no", "nope", "negative", "not the patient", "i am not", "i'm not", "i am not the patient", "i'm not the patient"
    ]

    for response in positive_responses:
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "yes"

    for response in negative_responses:
        pattern = rf'\b{re.escape(response)}\b'
        match = re.search(pattern, buffer, re.IGNORECASE)
        if match:
            return "no"

    return None

def extract_date_of_birth(buffer):
    question = "Could you please provide your date of birth?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    month_to_number = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        return f"{int(month)}/{int(day)}/{year}"

    match = re.search(r'\b(\d{1,2}),\s?(\d{1,3}),\s?(\d{1,4})\b', buffer)
    if match:
        month, day, year = match.groups()
        if len(day) == 1 and len(year) == 4:
            return f"{int(month)}/{int(day)}/{year}"
        elif len(day) == 3 and day[1] == '1' and day[2] == '2':
            return f"{int(month)}/21/{year}"
        else:
            return f"{int(month)}/{int(day)}/{year}"

    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(st|nd|rd|th)?,?\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, _, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    match = re.search(r'\b(\d{1})(\d{2})(\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        if year[0] in ['1', '2']:
            return f"{int(month)}/{int(day)}/{year}"

    return None

def extract_gender(buffer):
    question = "Got it. Are you a biological male or female?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    male_pattern = r'\b(male|boy|man)\b'
    female_pattern = r'\b(female|girl|woman)\b'

    male_matches = re.findall(male_pattern, buffer, re.IGNORECASE)
    female_matches = re.findall(female_pattern, buffer, re.IGNORECASE)

    if female_matches:
        return "female"
    elif male_matches:
        return "male"

    return None

def extract_state(buffer):
    question = "What state are you in right now?"
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
              "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
              "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    for state in states:
        if re.search(r'\b' + re.escape(state) + r'\b', buffer, re.IGNORECASE):
            return state
    return None

def extract_symptom(buffer):
    question = "Perfect. In a few words, please tell me your main symptom or reason for the call today."
    start_index = buffer.find(question) + len(question)
    buffer = buffer[start_index:]

    pattern = r'[\.\!\?]\s*(.*?)[\.\!\?]'
    match = re.search(pattern, buffer, re.IGNORECASE)
    if match:
        response = match.group(1).strip()
        return response
    return None

