import sqlite3, constants

conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('./highscores.db')
c = conn.cursor()


def create_table():
    c.execute('create table if not exists highscores('
          'name text not null, score integer not null)')

def insertscore(name, score):
    with conn:
        conn.execute('insert into highscores(name, score)'
                     'values(:name, :score)',
                     {'name': name, 'score': score}
                       # 'values(?,?)',
                       # (name, score)
                     )
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
    # print(row[0])
    # print(type(row[0]) is int)
    # num
    # print(c.fetchall())
    # num = (c.fetchone()[0])//constants.SHOW
    return

create_table()

# insertscore('catalin', 2100)
# insertscore('gibson', 200)
# insertscore('luka', 2300)
# insertscore('daan', 1000)
# insertscore('freek', 125)
# insertscore('shitter', 800)
# insertscore('sinvervesdfs', 932)
insertscore('1', 1000)
insertscore('2', 950)
insertscore('3', 900)
insertscore('4', 850)
insertscore('5', 800)
insertscore('6', 750)
insertscore('7', 700)
insertscore('8', 650)
insertscore('9', 600)
insertscore('10', 550)
insertscore('11', 500)
insertscore('12', 450)
insertscore('13', 400)
insertscore('14', 350)
insertscore('15', 300)
insertscore('16', 250)


# print(get_scores())
# print('w offset:')
# print(get_scores(1))
# clear_table(remain=5)
get_pages()
