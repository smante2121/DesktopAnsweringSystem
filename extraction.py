import re

def extract_is_patient(buffer):
    positive_responses = [
        "yes", "yeah", "i'm the patient", "i am the patient", "yep", "yup", "affirmative", "i am"
    ]

    negative_responses = [
        "no", "nope", "negative", "not the patient"
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
    month_to_number = {
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
        month, day, year = match.groups()
        if len(day) == 1 and len(year) == 4:
            return f"{int(month)}/{int(day)}/{year}"
        elif len(day) == 3 and day[1] == '1' and day[2] == '2':
            return f"{int(month)}/21/{year}"
        else:
            return f"{int(month)}/{int(day)}/{year}"

    # Handle month-day-year with possible ordinal suffixes and optional comma (e.g., June 21st, 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(st|nd|rd|th)?,?\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, _, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle more generic month-day-year formats without explicit separators (e.g., June 21 2003)
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{4})\b', buffer, re.IGNORECASE)
    if match:
        month, day, year = match.groups()
        month_number = month_to_number[month.lower()]
        return f"{int(month_number)}/{int(day)}/{year}"

    # Handle compact numeric dates without separators (e.g., 6212003)
    match = re.search(r'\b(\d{1})(\d{2})(\d{4})\b', buffer)
    if match:
        month, day, year = match.groups()
        if year[0] in ['1', '2']:
            return f"{int(month)}/{int(day)}/{year}"

    return None

def extract_last_name_letters(buffer):
    match = re.search(r'first three letters of my last name are\s+(\w)\s+(\w)\s+(\w)', buffer, re.IGNORECASE)
    if match:
        return ''.join(match.groups()).capitalize()

    match = re.search(r'my last name is (\w{3})', buffer, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()

    match = re.search(r'\b(\w)\s+(\w)\s+(\w)\b', buffer, re.IGNORECASE)
    if match:
        return ''.join(match.groups()).capitalize()

    match = re.search(r'\b(\w{3})\b', buffer, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()

    return None

def extract_gender(buffer):
    male_patterns = [
        r'\b(male)\b',
        r'\b(boy)\b'
    ]
    female_patterns = [
        r'\b(female)\b',
        r'\b(girl)\b'
    ]

    for pattern in female_patterns:
        if re.search(pattern, buffer, re.IGNORECASE):
            return "female"

    for pattern in male_patterns:
        if re.search(pattern, buffer, re.IGNORECASE):
            return "male"

    return None

def extract_state(buffer):
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
    pattern = r'reason for the call today\.\s*(.*?)[.]'
    match = re.search(pattern, buffer, re.IGNORECASE)
    if match:
        response = match.group(1).strip()
        return response
    return None
