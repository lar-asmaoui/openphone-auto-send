import requests
import pyfiglet
import re

phone_numbers = []
file_path = None
url = "https://api.openphone.com"
api_key = None

def transform_to_international_format(phone_number):
    # Define the regex for valid US/Canada phone numbers
    phone_regex = r"^(\+1[-.\s]?|1[-.\s]?)?(\([2-9]\d{2}\)|[2-9]\d{2})([-.\s]?)[2-9]\d{2}\3\d{4}$"
    
    match = re.match(phone_regex, phone_number)
    if not match:
        return None
        
    
    digits = re.sub(r"[^\d]", "", phone_number) 
    
    if len(digits) == 10:  # Add country code if missing
        digits = "1" + digits
    elif len(digits) != 11 or not digits.startswith("1"):
        return None
            
    return f"+{digits}"


def read_numbers_form_file():
    while True:
        file_path = input("Enter the file path (must be .txt): ")
        if not file_path.endswith('.txt'):
            print("The file must have a .txt extension.")
            # return to the beginning of the loop
            continue
        
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                for number in file:
                    if(number == '\n'):
                        continue
                    transformed_num =transform_to_international_format(number)
                    if transformed_num is None:
                        # print(f"Invalid phone number format: {number}")
                        continue
                    phone_numbers.append({'phone_number': transformed_num, 'status': 'pending'})
                print(phone_numbers)
                break
        except FileNotFoundError:
            print("File not found. Try again.")


def check_connection(api_key):
    url = "https://api.openphone.com/v1/phone_numbers"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print("Connection to the API was successful")
    else:
        print("Connection to the API was not successful")


def send_message(phone_number, message):
    url = "https://api.openphone.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        }
    payload = { "phone_number": phone_number, "message": message }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200

def save_to_csv():
    file_name = input("Enter the file name: ")
    with open(f"{file_name}.csv", 'w') as file:
        for number in phone_numbers:
            file.write(f"{number['phone_number']},{number['status']}\n")
        print("The phone numbers have been saved to a CSV file.")


if __name__ == "__main__":
 
    ascii_banner = pyfiglet.figlet_format("OpenPhone API")
    print(ascii_banner)    
    api_key = input("Enter your API key: ")
    check_connection(api_key)
    read_numbers_form_file()
    message = input("Enter the message you want to send: ")
    for number in phone_numbers:
        if send_message(number['phone_number'], message):
            number['status'] = 'sent'
        else:
            number['status'] = 'failed'
    save_to_csv()


