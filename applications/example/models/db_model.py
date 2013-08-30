import sqlite3

class DB_Model(object):
    """
    A very simple database model. You can also use sqlalchemy if you are familiar with it.
    """
    
    def __init__(self):
        self.open_connection()
        
        # check table existance
        table_exists = False
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon_list';")
        result = self.cursor.fetchall()
        if len(result)>0:
            table_exists = True
        
        print(("TABLE EXISTS : ",table_exists))
            
        
        if not table_exists:
            # create a table if not exists
            self.cursor.execute("CREATE TABLE pokemon_list (id INTEGER PRIMARY KEY, name TEXT, image TEXT)")
            # insert data
            pokemon_list = [
                            ("pikachu", "pikachu.png",), 
                            ("bubasaur", "bubasaur.png",), 
                            ("charmender", "charmender.png",), 
                            ("squirtle", "squirtle.png",), 
                            ("caterpie", "caterpie.png",)]
            sql = "INSERT INTO pokemon_list(name, image) VALUES(?,?)"
            self.cursor.executemany(sql, pokemon_list)
            # commit things
            self.conn.commit()
        
        self.close_connection()
    
    def open_connection(self):
        # define conn
        self.conn = sqlite3.connect("db/pokemon.db") # or use :memory: to put it in RAM 
        self.cursor = self.conn.cursor()
    
    def close_connection(self):
        self.conn.commit()
        self.conn.close()
    
    def get_pokemon_by_id(self, pokemon_id):
        self.open_connection()
        self.cursor.execute("SELECT id, name, image FROM pokemon_list WHERE id = " + str(pokemon_id))
        result = self.cursor.fetchall()
        if(len(result)==0):
            self.close_connection()
            return False
        else:
            row = result[0]
            self.close_connection()
            return {'id':row[0], 'name': row[1], 'image':row[2]}
    
    def get_pokemon(self, keyword=""):
        self.open_connection()
        self.cursor.execute("SELECT id, name, image FROM pokemon_list WHERE name LIKE '%" + keyword + "%'")
        result = self.cursor.fetchall()
        pokemon_list = []
        for row in result:
            pokemon_list.append({'id':row[0], 'name': row[1], 'image':row[2]})
        self.close_connection()
        return pokemon_list
    
    def delete_pokemon(self, pokemon_id):
        self.open_connection()
        self.cursor.execute("DELETE FROM pokemon_list WHERE id = "+str(pokemon_id))
        self.close_connection()
    
    def insert_pokemon(self, name, image=''):
        self.open_connection()
        self.cursor.execute("INSERT INTO pokemon_list(name, image) VALUES (?, ?)", (name,image))
        self.close_connection()
    
    def update_pokemon(self, pokemon_id, name, image=''):
        self.open_connection()
        if image=='':
            row = self.get_pokemon_by_id(pokemon_id)
            image = row['image']
        self.cursor.execute("UPDATE pokemon_list SET name=?, image=? WHERE id=?", (name,image,pokemon_id))
        self.close_connection()