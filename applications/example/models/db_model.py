import sqlite3

class Db_Model(object):
    """
    A very simple database model. You can also use sqlalchemy if you are familiar with it.
    """
    
    def __init__(self):
        self.conn = sqlite3.connect("db/pokemon.db") # or use :memory: to put it in RAM 
        self.cursor = self.conn.cursor()
        
        # check table existance
        table_exists = False
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon_list';")
        result = self.cursor.fetchall()
        if len(result)>0:
            table_exists = True
            
        
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
    
    def get_pokemon_by_id(self, pokemon_id):
        self.cursor.execute("SELECT id, name, image FROM pokemon_list WHERE id = " + str(pokemon_id))
        result = self.cursor.fetchall()
        if(len(result)==0):
            self.conn.commit()
            return False
        else:
            row = result[0]
            return {'id':row[0], 'name': row[1], 'image':row[2]}
    
    def get_pokemon(self, keyword=""):
        self.cursor.execute("SELECT id, name, image FROM pokemon_list WHERE name LIKE '%" + keyword + "%'")
        result = self.cursor.fetchall()
        pokemon_list = []
        for row in result:
            pokemon_list.append({'id':row[0], 'name': row[1], 'image':row[2]})
        return pokemon_list
    
    def delete_pokemon(self, pokemon_id):
        self.cursor.execute("DELETE FROM pokemon_list WHERE id = "+str(pokemon_id))
        self.conn.commit()
    
    def insert_pokemon(self, name, image=''):
        self.cursor.execute("INSERT INTO pokemon_list(name, image) VALUES (?, ?)", (name,image))
        self.conn.commit()
    
    def update_pokemon(self, pokemon_id, name, image=''):
        if image=='':
            row = self.get_pokemon_by_id(pokemon_id)
            image = row['image']
        self.cursor.execute("UPDATE pokemon_list SET name=?, image=? WHERE id=?", (name,image,pokemon_id))
        self.conn.commit()