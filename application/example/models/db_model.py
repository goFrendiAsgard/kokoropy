import sqlite3

class DB_Model(object):
    """
    A very simple database model. You can also use sqlalchemy if you are familiar with it.
    """
    
    def __init__(self):
        # define conn
        self.conn = sqlite3.connect("db/pokemon.db") # or use :memory: to put it in RAM 
        self.cursor = self.conn.cursor()
        # create a table if not exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pokemon_list (id int, name text)")
        self.conn.commit()
    
    def reset_data(self):
        # delete from table
        self.cursor.execute("DELETE FROM pokemon_list")
        self.conn.commit()
        pokemon_list = [("1","pikachu"), ("2","bubasaur"), ("3","charmender"), ("4","squirtle"), ("5","caterpie")]
        sql = "INSERT INTO pokemon_list(id,name) VALUES(?,?)"
        self.cursor.executemany(sql, pokemon_list)
        self.conn.commit()
    
    def get_pokemon(self, keyword=""):
        self.cursor.execute("SELECT name FROM pokemon_list WHERE name LIKE '%"+keyword+"%'")
        pokemon_list = self.cursor.fetchall()
        pokemon_names = [x[0] for x in pokemon_list]
        return pokemon_names
    
    def delete_pokemon(self, pokemon_id):
        self.cursor.execute("DELETE FROM pokemon_list WHERE id = "+str(pokemon_id))
    
    def insert_pokemon(self, name):
        self.cursor.execute("INSERT INTO pokemon_list(name) VALUES ('"+str(name)+"')")
    
    def update_pokemon(self, pokemon_id, name):
        self.cursor.execute("UPDATE pokemon_list(name) SET name='"+str(name)+"' WHERE id="+str(pokemon_id))