import sqlite3

# conn = sqlite3.connect('highscores.db')


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

def get_scores(n=7):
    """returns n highest scores
    or pass 0 to get all"""
    c.execute('select * from highscores order by score DESC')
    if n < 1:
        return c.fetchall()
    return c.fetchmany(n)


def clear_table(*remain):
    with conn:
        if remain != None:
            conn.execute('delete ')
        conn.execute('delete * from highscores')


def test():
    for i in range(0, 10):
        name = ''
        for char in range(0, 4):
            name += random.choice(string.ascii_lowercase)
        insertscore(name, random.randint(-10, 9999))
    print(get_scores())


# Initialization
conn = sqlite3.connect(':memory:')
c = conn.cursor()
create_table()
if __name__ == '__main__':
    import random, string
    test()
