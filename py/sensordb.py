import sqlite3, constants


def create_table():
    c.execute('create table if not exists highscores('
          'name text not null, score integer not null)')


def insertscore(name, score):
    # TODO return True if its a new highscore?
    with conn:
        c.execute('select * from highscores order by score DESC limit 1')
        highest = c.fetchone()
        if highest:
            is_hiscore = highest[1] < score and score > 0
        else:
            is_hiscore = True

        conn.execute('insert into highscores(name, score)'
                     'values(:name, :score)',
                     {'name': name, 'score': score}
                       # 'values(?,?)',
                       # (name, score)
                     )
        return is_hiscore


# returns the 7 highest scores
def get_scores(offset=None):
    if type(offset) is int:
        c.execute('select * from highscores order by score DESC limit ? offset ?',
                  (constants.SHOW, offset))
    else:
        c.execute('select * from highscores order by score DESC limit ?',
                  (constants.SHOW,))
    return c.fetchall()


def clear_table(remain=None):
    with conn:
        if remain == None:
            conn.execute('delete from highscores')
        else:
            print('trying to keep ' + str(remain))
            conn.execute('delete from highscores where oid not in(select oid from highscores order by score DESC limit :remain)', {'remain':remain} )


def get_pages():
    c.execute('select count(oid) from highscores')
    num = c.fetchone()[0]
    return num//constants.SHOW


conn = sqlite3.connect(':memory:')
c = conn.cursor()

create_table()
