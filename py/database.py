import sqlite3

# conn = sqlite3.connect('highscores.db')
conn = sqlite3.connect('highscores.db')
c = conn.cursor()


def create_table():
    c.execute('create table if not exists highscores('
          'name text, score integer)')

create_table()

def insertscore(name, score):
    with conn:
        conn.execute('insert into highscores(name, score)'
                     # 'values(:name, :score)', 
                     # {'name': name, 'score':score}
                       'values(?,?)',
                       (name, score)
                     )


def get_scores():
    c.execute('select * from highscores order by score')
    return c.fetchmany(5)

insertscore('gibson', 200)
# insertscore('gibson', 2300)
# insertscore('gibson', 2100)
print(get_scores())
# for row in get_scores():
#     print(row)
