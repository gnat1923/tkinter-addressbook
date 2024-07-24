from tkinter import *
import sqlite3


root = Tk()
root.title("Database Tutorial")
root.geometry("400x600") # set initial size

# Create a database or connect to one
conn = sqlite3.connect("address_book.db")

# Create a db cursor
c = conn.cursor()

# Template function
def template():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    conn.commit()
    conn.close()

# Create submit function
def submit():
    # Connect to db (each function must establish a connection).
    conn = sqlite3.connect("address_book.db")
    # Create a db cursor
    c = conn.cursor()

    # Insert data into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :code)",
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'address': address.get(),
                  'city': city.get(),
                  'state': state.get(),
                  'code': code.get()
              }
              )

    # Commit changes
    conn.commit()
    # Close connection
    conn.close()
    
    # Clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    code.delete(0, END)

def query():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Create query
    c.execute("SELECT *, oid FROM addresses") # oid is primary key in sqlite
    records = c.fetchall() # or fetchone / fetchmany(x)
    #print(records)
    print_records = ''

    # Loop through results
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + \
                         " " + "\t" + str(record[6]) + "\n"

    query_label = Label(root, text= print_records)
    query_label.grid(row=12, column=0, columnspan=2)

    conn.commit()
    conn.close()

# Delete entry function
def delete():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Delete record
    c.execute("DELETE from addresses WHERE oid=" + delete_box.get())

    conn.commit()
    conn.close()

# Create edit function to update a record
def edit():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Create a new window
    editor = Tk()
    editor.title("Update record")
    editor.geometry("400x600")

    record_id = delete_box.get()
    # Query db to prepopulate fields
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id) # oid is primary key in sqlite
    records = c.fetchall() # or fetchone / fetchmany(x)

    # Add all fields from root window
    # Create text boxes
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)
    code_editor = Entry(editor, width=30)
    code_editor.grid(row=5, column=1)

    # Create text box labels
    f_name_label_editor = Label(editor, text="First name")
    f_name_label_editor.grid(row=0, column=0, pady=(10, 0))
    l_name_label_editor = Label(editor, text="Last name")
    l_name_label_editor.grid(row=1, column=0)
    address_label_editor = Label(editor, text="Address")
    address_label_editor.grid(row=2, column=0)
    city_label_editor = Label(editor, text="City")
    city_label_editor.grid(row=3, column=0)
    state_label_editor = Label(editor, text="State")
    state_label_editor.grid(row=4, column=0)
    code_label_editor = Label(editor, text="Post code")
    code_label_editor.grid(row=5, column=0)

    # Create submit button
    submit_button_editor = Button(editor, text="Save record", command=submit)
    submit_button_editor.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Loop through results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        code_editor.insert(0, record[5])

    conn.commit()
    conn.close()

# Create db table
"""
This is only run once (at the beginning) to create the table, 
and is commented out going forward
c.execute('''CREATE TABLE addresses (
         first_name text,
          last_name text,
          address text,
          city text,
          state text,
          area_code integer
          )
''')
"""

# Create text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2, column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

code = Entry(root, width=30)
code.grid(row=5, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

# Create text box labels
f_name_label = Label(root, text="First name")
f_name_label.grid(row=0, column=0, pady=(10, 0))

l_name_label = Label(root, text="Last name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

code_label = Label(root, text="Post code")
code_label.grid(row=5, column=0)

delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=9, column=0, pady=5)

# Create submit button
submit_button = Button(root, text="Add record to database", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a query button
query_btn = Button(root, text="Show records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

# Delete button
delete_btn = Button(root, text="Delete record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

# Create an update button
update_btn = Button(root, text="Update record", command=edit)
update_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=144)


# Commit changes
conn.commit()

# Close connection
conn.close()

root.mainloop()