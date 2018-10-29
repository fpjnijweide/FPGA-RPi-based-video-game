import sqlite3

# conn = sqlite3.connect('highscores.db')
conn = sqlite3.connect(':memory:')
c = conn.cursor()


def create_table():
    c.execute('create table highscores('
          'name text, score integer)')

def insertscore(name, score):
    with conn:
        conn.execute('insert into highscores(name, score)'
                     'values(:name, :score)',
                     {'name': name, 'score': score}
                       # 'values(?,?)',
                       # (name, score)
                     )
# returns the 7 highest scores
def get_scores():
    c.execute('select * from highscores order by score DESC')
    return c.fetchmany(7)

def clear_table(*remain):
    with conn:
        if remain != None:
            conn.execute('delete ')
        conn.execute('delete * from highscores')
create_table()

insertscore('gibson', 200)
insertscore('gibson', 2300)
insertscore('gibson', 2100)
print(get_scores())
# for row in get_scores():
#     print(row)
