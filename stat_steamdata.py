
from steam.apps import app_list
import steam
import MySQLdb

import time

# steam.api.key.set("")
from sys import argv

def connect_mysql(db_host="192.168.0.2", user="iri",
                  passwd="iri", db="steam", charset="utf8"):

    conn = MySQLdb.connect(host=db_host, user=user, passwd=passwd, db=db, charset=charset)

    return conn


def get_status():

    
    db = connect_mysql()
    conn = db.cursor()

    try:
        conn.execute('SELECT count(*) from id')
        ids=conn.fetchall()
        ids=ids[0][0]
        print 'database has  %i unretrieved IDs'%ids



        
    except Exception,e:
        print e


    try:
        conn.execute('SELECT count(*) from data')
        datas=conn.fetchall()
        datas=datas[0][0]
        print 'database has  %i retrieved IDs info'%datas

        
    except Exception,e:
        print e


    try:
        conn.execute('SELECT count(*) from xid')
        xids=conn.fetchall()
        xids=xids[0][0]
        print 'could not get %i IDs due to private setting or other causes'%xids

        
    except Exception,e:
        print e   

    

    print '\nstatistics: '
    timing=time.ctime()
    # print timing
    # timing=timing.split(':')
    # h,m,s=timing[0][-2:],timing[1],timing[2][:2]

    # print timing, time.time(), datas

    fl=open('steamlog.txt','a+')
    log=fl.readlines()
    info=log[-1]
    # print info

    got=info.split(' ')
    # print got
    date0,count0=float(got[-2]),float(got[-1].replace('\n',''))

    date1,count1=time.time(),float(datas)

    elapse, count=date1-date0,count1-count0
    gainpersecond=count/elapse

    print 'getting %i more IDs info '%int(count)
    print >> fl, 'getting %i more IDs info '%int(count)


    print 'time elapse  %.2f mins, %.2f hrs, %.2f s'%(elapse/60, elapse/3600, elapse)
    print >> fl, 'time elapse  %.2f mins, %.2f hrs, %.2f s'%(elapse/60, elapse/3600, elapse)

    print 'speed: %.2f gain/per_second'%gainpersecond
    print >> fl, '%.2f gain/per_second'%gainpersecond

    permin, perhour= gainpersecond*60, gainpersecond*60*60
    print 'at this speed, for 1000 W  info will use %.2f hours'%(10000000/gainpersecond/60/60)
    print >> fl, 'at this speed, for 1000 W  info will use %.2f hours'%(10000000/gainpersecond/60/60)
    print ''
    print timing, time.time(), datas
    print >> fl, timing, time.time(), datas

    # # getting=info.split(' ')
    # # h0,m0,s0,count0=getting[0],getting[1],getting[2],getting[3].replace('\n','')
    # # print h0,m0,s0,count0

    # # h,m,s,h0,m0,s0,datas,count0=map(float,[h,m,s,h0,m0,s0,datas,count0])
    

    # h1=h-h0 if h-h0>0 else h+24-h0
    # m1=m-m0
    # s1=s-s0
    # count1=datas-count0
    # print h1,m1,s1,count1
    # hp,mp,sp=count1/h1,count1/m1,count1/s1




    fl.close()
    conn.close()
    db.close()

if __name__=='__main__':

    db = connect_mysql()
    conn = db.cursor()

    game_table=True
    import MySQLdb
    


    get_status()
    




    try:
        game=argv[1]
    except:
        game=''
    
    if str(game).strip().lower()=='game':


        try:
            conn.execute('''CREATE TABLE `game` (
            `game_id`   INTEGER,
            `game_name` TEXT,
            PRIMARY KEY(game_id)
    );''')
            db.commit()
        except:
            # game_table=False
            print 'game table exists'

        if game_table:
            
            apps=app_list()
            for i in apps:
                try:
                    conn.execute('insert into game values(%s,%s)',(i[0],i[1]))
                except:
                    print '-',
                               
            db.commit()
        else:
            print 'game list already exists'    

 

