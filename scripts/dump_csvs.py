from  pysqlite2 import dbapi2 as sqlite
import json

connection = sqlite.connect('../webappsstore1.sqlite')
cursor = connection.cursor()
cursor.execute("SELECT key,value FROM webappsstore WHERE key LIKE 'USER%'")

game_fields = []

def ssnmtree_dict(dic,id=None):
    tree = []
    for k,v in dic.items():
        if not isinstance(v,dict):
            continue
        tree.append([id,k,
                     v['disclosure'],
                     v['support'],
                     v['name'],])

    return tree

def pillgame_dict(dic,id=None):
    meds = []
    for v in dic['day_pills'].values():
        meds.append([id,v['where'],v['pill_type'], ])
    for v in dic['night_pills'].values():
        meds.append([id,v['where'],v['pill_type'], ])
    return meds

def problemsolving_dict(dic,id=None):
    my_issues = []
    for k,v in dic['my_issues'].items():
        my_issues.append([id,k,
                          v.get('action',''),
                          v.get('aim',''),
                          v.get('alternatives',''),
                          v.get('alternatives2',''),
                          v.get('alternatives3',''),
                          v.get('ask',''),
                          ])
    return my_issues

def timelog_dict(dic,id=None):
    logs = []
    for date,pages in dic.items():
        for page in pages:
            logs.append([id, date, page['page'], page['time'], ])
    return logs

exceptions = {
    'pill_game_state':{
        'path':'games.pill_game_state',
        'select':['day_pills_time_menu_selected_index','night_pills_time_menu_selected_index','treatment_line'],
        'new_table':pillgame_dict,
        'table_cols':['Patient ID','Time of Day','Pill'],
        },
    'problemsolving':{
        'path':'games.problemsolving',
        'select':['chosen-issue','default_page'],
        'new_table':problemsolving_dict,
        'table_cols':['Patient ID','Issue',
                      'Action','Aim','Alternatives',
                      'Alternatives2','Alternatives3','Ask',],
        },
    'ssnmtree':{
        'path':'games.ssnmtree',
        'select':[],
        'new_table':ssnmtree_dict,
        'table_cols':['Patient ID','Position','Disclosure','Support','Name']
        },
    'sessions':{
        'select':[],
        },
    'admin':{
        'select':[],
        },
    'timelog':{
        'path':'timelog',
        'select':[],
        'new_table':timelog_dict,
        'table_cols':['Patient ID','Date','Page','Seconds on page']
        }
}

def dict_fields(dic):
    to_return = []
    for k,v in dic.items():
        if k in exceptions:
            for a in exceptions[k]['select']:
                to_return.append([k,a])
            #ar = dict_fields(exceptions[k]['new_table'](v))
            #for a in ar:
            #    to_return.append([k]+a)
        elif isinstance(v,dict) and len(v) >0:
            ar = dict_fields(v)
            for a in ar:
                to_return.append([k]+a)
        else:
            if k != 'games':
                to_return.append([k])
    return to_return


def getval(dic,keys):
    val = dic
    for k in keys.split('.'):
        if val.has_key(k):
            val = val[k]
        else:
            return ''
    return val

def cols(rows):
    m = set()    
    for r in rows:
        data = json.loads(r[1])
        games = dict_fields(data)
        for i in games:
            m.add('.'.join(i))
    return sorted(m)

def csv_info(rows):
    main_file_cols = cols(rows)
    main = []
    main.append(['Patient ID']+main_file_cols) #header row
    extras = {}
    for k,v in exceptions.items():
        if v.has_key('new_table'):
            extras[k] = [ v['table_cols'] ] #header

    for r in rows:    
        user = [r[0]]
        data = json.loads(r[1])
        for col in main_file_cols:
            user.append( getval(data,col) )
        main.append(user)
        for k,v in extras.items():
            edata = getval(data,exceptions[k]['path'])
            if edata:
                v.extend( exceptions[k]['new_table'](edata, r[0]) )

    return main,extras

def write_csvs(stuff):
    import csv
    main = stuff[0]
    extras = stuff[1]
    
    main_csv = csv.writer(open('masivukeni.csv','wb'))
    main_csv.writerows(main)

    for k,v in extras.items():
        csv_extra = csv.writer(open('%s-masivukeni.csv'%k,'wb'))
        csv_extra.writerows(v)

rows = list(cursor.fetchall())
for line in cols(rows):
    print line

write_csvs( csv_info(rows) )




