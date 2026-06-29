import json
import logging

logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

FILE_NAME = "contacts.json"


class ContactNotFoundError(Exception):
    pass


def load_contacts():
    try:
        with open(FILE_NAME, "r") as file:
            contacts = json.load(file)
            logging.info("Contacts loaded successfully.")
            return contacts

    except FileNotFoundError:
        logging.warning("contacts.json not found. New file will be created.")
        return {}

    except json.JSONDecodeError:
        logging.error("Corrupted JSON file detected.")
        print(" JSON file is corrupted. Starting with empty contacts.")
        return {}

    finally:
        logging.info("Load contacts operation completed.")


def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)
        logging.info("Contacts saved successfully.")

    except Exception as e:
        logging.error(f"Error saving contacts: {e}")

    finally:
        logging.info("Save contacts operation completed.")


def add_contact(contacts):
    try:
        name = input("Enter Name: ").strip()

        if not name:
            raise ValueError("Name cannot be empty.")

        phone = input("Enter Phone Number: ").strip()

        if not phone.isdigit():
            raise ValueError("Phone number should contain only digits.")

        email = input("Enter Email: ").strip()

        contacts[name] = {
            "phone": phone,
            "email": email
        }

        save_contacts(contacts)

        print(" Contact Added Successfully!")
        logging.info(f"Contact '{name}' added.")

    except ValueError as e:
        print(f" {e}")
        logging.warning(str(e))


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("\n----- CONTACT LIST -----")

    for name, details in contacts.items():
        print(f"\nName  : {name}")
        print(f"Phone : {details['phone']}")
        print(f"Email : {details['email']}")

    logging.info("Viewed all contacts.")


def search_contact(contacts):
    try:
        name = input("Enter Contact Name to Search: ").strip()

        if name not in contacts:
            raise ContactNotFoundError("Contact not found.")

        print("\nContact Found:")
        print(f"Name  : {name}")
        print(f"Phone : {contacts[name]['phone']}")
        print(f"Email : {contacts[name]['email']}")

        logging.info(f"Contact '{name}' searched.")

    except ContactNotFoundError as e:
        print(f" {e}")
        logging.warning(str(e))


def delete_contact(contacts):
    try:
        name = input("Enter Contact Name to Delete: ").strip()

        if name not in contacts:
            raise ContactNotFoundError("Contact not found.")

        del contacts[name]
        save_contacts(contacts)

        print(" Contact Deleted Successfully!")
        logging.info(f"Contact '{name}' deleted.")

    except ContactNotFoundError as e:
        print(f" {e}")
        logging.warning(str(e))


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT MANAGEMENT SYSTEM =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")

        try:
            choice = int(input("Enter Your Choice: "))

            if choice == 1:
                add_contact(contacts)

            elif choice == 2:
                view_contacts(contacts)

            elif choice == 3:
                search_contact(contacts)

            elif choice == 4:
                delete_contact(contacts)

            elif choice == 5:
                print("Thank You!")
                logging.info("Program exited successfully.")
                break

            else:
                print(" Invalid Choice. Please select 1-5.")
                logging.warning("Invalid menu choice entered.")

        except ValueError:
            print("Please enter a valid number.")
            logging.warning("Non-numeric menu input entered.")

        finally:
            logging.info("Menu operation completed.")


if __name__ == "__main__":
    main()
