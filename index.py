import sqlite3

# Connect to SQLite database. It will be created if it doesn't exist.
conn = sqlite3.connect('contact_book.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT
    )
''')

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email (optional): ")
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    print("Contact added successfully!")

def view_contacts():
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    if not contacts:
        print("No contacts found.")
    else:
        for contact in contacts:
            print(f"ID: {contact[0]} | Name: {contact[1]} | Phone: {contact[2]} | Email: {contact[3]}")

def update_contact():
    contact_id = int(input("Enter contact ID to update: "))
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    contact = cursor.fetchone()
    if not contact:
        print("Contact not found.")
    else:
        print("Enter new details (press enter to skip):")
        name = input(f"Name ({contact[1]}): ")
        phone = input(f"Phone ({contact[2]}): ")
        email = input(f"Email ({contact[3]}): ")
        if name:
            cursor.execute('UPDATE contacts SET name = ? WHERE id = ?', (name, contact_id))
        if phone:
            cursor.execute('UPDATE contacts SET phone = ? WHERE id = ?', (phone, contact_id))
        if email:
            cursor.execute('UPDATE contacts SET email = ? WHERE id = ?', (email, contact_id))
        conn.commit()
        print("Contact updated successfully!")

def delete_contact():
    contact_id = int(input("Enter contact ID to delete: "))
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    contact = cursor.fetchone()
    if not contact:
        print("Contact not found.")
    else:
        confirm = input(f"Are you sure you want to delete {contact[1]}'s contact? (y/n): ")
        if confirm.lower() == 'y':
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            conn.commit()
            print("Contact deleted successfully!")
        else:
            print("Deletion cancelled.")

def main():
    while True:
        print("\nContact Book Menu:")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Quit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_contact()
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
    conn.close()