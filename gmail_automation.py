from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import random
import time
from unidecode import unidecode

from proxy_randomizer import RegisteredProviders

rp = RegisteredProviders()
rp.parse_providers()

# Chrome options
chrome_options = webdriver.ChromeOptions()
## print the proxy IP and port 

proxy_string = str(rp.get_random_proxy())

# Split the string to extract the IP and port part
proxy_parts = proxy_string.split(' ', 1)

# Extract the IP and port
ip_and_port = proxy_parts[0]

print(f"Proxy: {ip_and_port}")

chrome_options.add_argument("--disable-infobars")
proxy = rp.get_random_proxy()  # Ensure this returns a valid proxy string
# chrome_options.add_argument(f"--proxy-server={'13.83.94.137:3128'}")
# WebDriver service
service = ChromeService('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

french_first_names = [
    "Amélie", "Antoine", "Aurélie", "Benoît", "Camille", "Charles", "Chloé", "Claire", "Clément", "Dominique",
    "Élodie", "Émilie", "Étienne", "Fabien", "François", "Gabriel", "Hélène", "Henri", "Isabelle", "Jules",
    "Juliette", "Laurent", "Léa", "Léon", "Louise", "Lucas", "Madeleine", "Marc", "Margaux", "Marie",
    "Mathieu", "Nathalie", "Nicolas", "Noémie", "Olivier", "Pascal", "Philippe", "Pierre", "Raphaël", "René",
    "Sophie", "Stéphane", "Suzanne", "Théo", "Thomas", "Valentin", "Valérie", "Victor", "Vincent", "Yves",
    "Zoé", "Adèle", "Adrien", "Alexandre", "Alice", "Alix", "Anatole", "André", "Angèle", "Anne",
    "Baptiste", "Basile", "Bernard", "Brigitte", "Céleste", "Céline", "Christophe", "Cyril", "Denis", "Diane",
    "Édouard", "Éléonore", "Émile", "Félix", "Florence", "Georges", "Gérard", "Guillaume", "Hugo", "Inès",
    "Jacques", "Jean", "Jeanne", "Joséphine", "Julien", "Laure", "Lucie", "Maëlle", "Marcel", "Martine",
    "Maxime", "Michel", "Nina", "Océane", "Paul", "Perrine", "Quentin", "Romain", "Solène", "Thérèse"
]

french_last_names = [
    "Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre", "Mercier", "Dupont", "Fournier", "Lambert",
    "Fontaine", "Rousseau", "Vincent", "Muller", "Lefèvre", "Faure", "André", "Gauthier", "Garcia", "Perrin",
    "Robin", "Clement", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu", "Garnier", "Chevalier", "François",
    "Legrand", "Gérard", "Boyer", "Gautier", "Roche", "Roy", "Noel", "Meyer", "Lucas", "Gomez",
    "Martinez", "Caron", "Da Silva", "Lemoine", "Philippe", "Bourgeois", "Pierre", "Renard", "Girard", "Brun",
    "Gaillard", "Barbier", "Arnaud", "Martins", "Rodriguez", "Picard", "Roger", "Schmitt", "Colin", "Vidal",
    "Dupuis", "Pires", "Renaud", "Renault", "Klein", "Coulon", "Grondin", "Leclerc", "Pires", "Marchand",
    "Dufour", "Blanchard", "Gillet", "Chevallier", "Fernandez", "David", "Bouquet", "Gilles", "Fischer", "Roy",
    "Besson", "Lemoine", "Delorme", "Carpentier", "Dumas", "Marin", "Gosselin", "Mallet", "Blondel", "Adam",
    "Durant", "Laporte", "Boutin", "Lacombe", "Navarro", "Langlois", "Deschamps", "Schneider", "Pasquier", "Renaud"
]


# Randomly select a first name and a last name
your_first_name = random.choice(french_first_names)
your_last_name = random.choice(french_last_names)

# Generate a random number
random_number = random.randint(1000, 9999)

# Normalize names
your_first_name_normalized = unidecode(your_first_name).lower()
your_last_name_normalized = unidecode(your_last_name).lower()
your_username = f"{your_first_name_normalized}.{your_last_name_normalized}{random_number}"

your_birthday = "02 3 1989"  # dd m yyyy
your_gender = "1"  # 1:F 2:M 3:Not say 4:Custom
your_password = "x,nscldsj123...FDKZ"

def fill_form(driver):
    try:
        driver.get("https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

        # Fill in name fields
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys(your_first_name)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "lastName"))).send_keys(your_last_name)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe"))).click()

        # Wait for birthday fields to be visible
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "day")))

        # Fill in birthday
        birthday_elements = your_birthday.split()
        Select(driver.find_element(By.ID, "month")).select_by_value(birthday_elements[1])
        driver.find_element(By.ID, "day").send_keys(birthday_elements[0])
        driver.find_element(By.ID, "year").send_keys(birthday_elements[2])

        # Select gender
        Select(driver.find_element(By.ID, "gender")).select_by_value(your_gender)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe"))).click()

        # Create custom email
        time.sleep(2)
        create_own_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "selectionc4")))
        create_own_option.click()

        username_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "Username")))
        username_field.send_keys(your_username)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe"))).click()

        # Enter and confirm password
        password_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "Passwd")))
        password_field.send_keys(your_password)
        confirm_passwd_div = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "confirm-passwd")))
        password_confirmation_field = confirm_passwd_div.find_element(By.NAME, "PasswdAgain")
        password_confirmation_field.send_keys(your_password)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe"))).click()

        # Skip phone number and recovery email steps
        skip_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        for button in skip_buttons:
            button.click()

        # Agree to terms
        agree_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        agree_button.click()

        print(f"Your Gmail successfully created:\n{{\ngmail: {your_username}@gmail.com\npassword: {your_password}\n}}")

    except Exception as e:
        print("Failed to create your Gmail, Sorry")
        print(e)
    finally:
        driver.quit()

# Execute the function to fill out the form
fill_form(driver)
