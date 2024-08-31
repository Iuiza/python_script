from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip

def fetch_aa_sequences(accession_numbers):
    service = Service(r"C:\Users\Luiza\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    base_url = "https://mibig.secondarymetabolites.org/repository/"
    sequences = {}

    for accession in accession_numbers:
        accession = accession.strip()  # Remove any surrounding whitespace or newline characters
        url = f"{base_url}{accession}/"
        
        try:
            driver.get(url)
            print(f"Opened URL: {url}")

            # Check if the polygon element with the specified class exists before attempting to click it
            wait = WebDriverWait(driver, 10)
            try:
                polygon_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "polygon.svgene-type-biosynthetic.svgene-orf.svgene-selected-orf")))
                print(f"Polygon element found for accession {accession}. Clicking...")
                polygon_element.click()

                # Wait for the "Copy to clipboard" button to become clickable
                copy_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Copy to clipboard')]")))
                print("Clicking 'Copy to clipboard' button...")
                copy_span.click()
                time.sleep(2)  # Increased wait time for clipboard operation

                # Retrieve the AA sequence from the clipboard
                aa_sequence = pyperclip.paste().strip()
                if aa_sequence:  # Check if clipboard content is not empty
                    print(f"AA sequence retrieved for accession {accession}: {aa_sequence[:50]}...")  # Print first 50 chars for preview
                    sequences[accession] = aa_sequence
                else:
                    print(f"Clipboard is empty for accession {accession}.")

            except Exception as e:
                print(f"Polygon element or copy button issue for accession {accession}: {e}")
                continue

        except Exception as e:
            print(f"Failed to retrieve data for accession {accession}: {e}")

    driver.quit()
    return sequences

def save_sequences(sequences, filename="aa_sequences.txt"):
    with open(filename, "w") as file:
        for accession, sequence in sequences.items():
            file.write(f"Accession: {accession}\nSequence:\n{sequence}\n\n")
    print(f"Sequences saved to {filename}")

def load_accession_numbers(filepath):
    with open(filepath, "r") as file:
        accession_numbers = file.readlines()
    return accession_numbers

# Example usage:
input_file = "accession_numbers.txt"
accession_numbers = load_accession_numbers(input_file)
sequences = fetch_aa_sequences(accession_numbers)
save_sequences(sequences)