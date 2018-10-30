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


def test():
    for i in range(0, 10):
        name = ''
        for char in range(0, 4):
            name += random.choice(string.ascii_lowercase)
        insertscore(name, random.randint(-10, 9999))
    print(get_scores())


if __name__ == '__main__':
    import random, string
    test()
