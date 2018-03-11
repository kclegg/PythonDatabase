from tkinter import *
from tkinter import ttk
import sqlite3

class Assignment5:
    
    data_base = 'flowers.db'
    
    def __init__(self,wind):

        self.wind = wind;
        self.wind.title('Southern Sierra Wildflower Club')

        frame = LabelFrame(self.wind)
        frame.grid(row = 0, column = 1)

        Label (frame, text = 'Name: ').grid(row = 1, column = 1)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 2)

        Label (frame, text = 'Person: ').grid(row = 2, column = 1)
        self.person = Entry(frame)
        self.person.grid(row = 2, column = 2)

        Label (frame, text = 'Location: ').grid(row = 3, column = 1)
        self.location = Entry(frame)
        self.location.grid(row = 3, column = 2)

        Label (frame, text = 'Sighted: ').grid(row = 4, column = 1)
        self.sighted = Entry(frame)
        self.sighted.grid(row = 4, column = 2)

        ttk.Button(frame, text = 'Insert Sighting', command = self.adding).grid(row = 5, column = 2)
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 5, column = 0)

        self.left_tree = ttk.Treeview(height = 10, columns = ("person","location","sighted"))
        self.left_tree.grid(row = 2, column = 0, columnspan = 4)
        self.left_tree.heading('#0', text = 'Name', anchor = W)
        self.left_tree.heading("person", text = 'Person', anchor = W)
        self.left_tree.heading("location", text = 'Location', anchor = W)
        self.left_tree.heading("sighted", text = 'Sighted', anchor = W)
        self.viewing_records()        

        self.right_tree = ttk.Treeview(height = 10, columns = ("Species","Comname"))
        self.right_tree.grid(row = 2, column = 10, columnspan = 4)
        self.right_tree.heading('#0', text = 'Genus', anchor = W)
        self.right_tree.heading("Species", text = 'Species', anchor = W)
        self.right_tree.heading("Comname", text = 'Comname', anchor = W)
        self.viewing_flower_records()

        self.lower_tree = ttk.Treeview(height = 10, columns = ("person","location","sighted"))
        self.lower_tree.grid(row = 10, column = 0, columnspan = 4)
        self.lower_tree.heading('#0', text = 'Name', anchor = W)
        self.lower_tree.heading("person", text = 'Person', anchor = W)
        self.lower_tree.heading("location", text = 'Location', anchor = W)
        self.lower_tree.heading("sighted", text = 'Sighted', anchor = W)
        
        ttk.Button(text = 'Update Tuple', command = self.editing).grid(row = 1, column = 10)
        ttk.Button(text = 'Ten Recent Sightings', command = self.ten_recent_sightings).grid(row = 1, column = 12)
        
    def run_query (self, query, parameters = ()):
        with sqlite3.connect (self.data_base) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_records (self):
        records = self.left_tree.get_children()
        for element in records:
            self.left_tree.delete (element)
        query = 'SELECT * FROM SIGHTINGS'
        data_base_rows = self.run_query(query)
        for row in data_base_rows:
            self.left_tree.insert('' , 0, text = row[0], values = [row[1],row[2],row[3]])

    def viewing_flower_records (self):
        records = self.right_tree.get_children()
        for element in records:
            self.right_tree.delete (element)
        query = 'SELECT * FROM FLOWERS'
        data_base_rows = self.run_query(query)
        for row in data_base_rows:
            self.right_tree.insert('' , 0, text = row[0], values = [row[1],row[2]])
    
    def adding (self):
        query = 'INSERT INTO SIGHTINGS VALUES (?,?,?,?)'
        parameters = (self.name.get(), self.person.get(), self.location.get(), self.sighted.get())
        self.run_query (query, parameters)
        self.message ['text'] = 'Insertion added'.format (self.name.get())
        self.name.delete (0, END)
        self.person.delete (0, END)
        self.location.delete (0, END)
        self.sighted.delete (0, END)
        self.viewing_records()

    def update_records (self, new_genus, old_genus, new_species, old_species, new_comname, old_comname):
        query = 'UPDATE FLOWERS SET genus = ?, species = ?, comname = ? WHERE genus = ? AND species = ? AND comname = ?'
        parameters = (new_genus, new_species, new_comname, old_genus, old_species, old_comname)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Flower tuple updated!'
        self.viewing_flower_records()

    def editing (self):
        self.message['text'] = ''
        try:
            self.right_tree.item (self.right_tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a flower'
            return
        
        old_genus = self.right_tree.item(self.right_tree.selection())['text']
        old_species = self.right_tree.item (self.right_tree.selection())['values'][0]
        old_comname = self.right_tree.item (self.right_tree.selection())['values'][1]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Window')
        
        Label (self.edit_wind, text = 'Old Genus: ').grid(row = 0, column = 1)
        Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_genus), state = 'readonly').grid(row = 0, column = 2)
        Label (self.edit_wind, text = 'New Genus: ').grid(row = 1, column = 1)
        new_genus = Entry(self.edit_wind)
        new_genus.grid(row = 1, column = 2)
        
        Label (self.edit_wind, text = 'Old Species: ').grid(row = 2, column = 1)
        Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_species), state = 'readonly').grid(row = 2, column = 2)
        Label (self.edit_wind, text = 'New Species: ').grid(row = 3, column = 1)
        new_species = Entry(self.edit_wind)
        new_species.grid(row = 3, column = 2)

        Label (self.edit_wind, text = 'Old Comname: ').grid(row = 4, column = 1)
        Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_comname), state = 'readonly').grid(row = 4, column = 2)
        Label (self.edit_wind, text = 'New Comname: ').grid(row = 5, column = 1)
        new_comname = Entry(self.edit_wind)
        new_comname.grid(row = 5, column = 2)

        Button(self.edit_wind, text = 'save changes', command = lambda:self.update_records(new_genus.get(), old_genus, new_species.get(), old_species, new_comname.get(), old_comname)).grid(row = 6, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def ten_recent_sightings (self):
        try:
            self.right_tree.item (self.right_tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a flower'
            return
        
        selected_flower = self.right_tree.item (self.right_tree.selection())['values'][1]
        query = 'SELECT * FROM SIGHTINGS WHERE name = (SELECT comname FROM FLOWERS WHERE comname = ?) ORDER BY sighted DESC LIMIT 10'
        parameters = (selected_flower)
        data_base_rows = self.run_query (query, (parameters,))
        
        records = self.lower_tree.get_children()
        for element in records:
            self.lower_tree.delete (element)
        for row in data_base_rows:
            self.lower_tree.insert('' , 0, text = row[0], values = [row[1],row[2],row[3]])

        
if __name__ == '__main__':
    wind = Tk ()
    appliation = Assignment5 (wind)
    wind.mainloop()
