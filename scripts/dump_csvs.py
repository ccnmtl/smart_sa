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
        tree.append(id +[k,
                     v['disclosure'],
                     v['support'],
                     v['name'][0:1],])

    return tree

def pillgame_dict(dic,id=None):
    meds = []
    for v in dic['day_pills'].values():
        meds.append(id +[v['where'],v['pill_type'], ])
    for v in dic['night_pills'].values():
        meds.append(id +[v['where'],v['pill_type'], ])
    return meds

def problemsolving_dict(dic,id=None):
    my_issues = []
    for k,v in dic['my_issues'].items():
        my_issues.append(id +[k,
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
            logs.append(id+[date, page['page'], page['time'], ])
    return logs

#users that were tests or admins
user_black_list = [
    "USER_4e984ae0fa98ceecb5fdb3db80fd265a55fb6d0a",
    "USER_d035ce90cf96be0fa6c91a36ef2e1d00e461d336",
    "USER_15c9983829fe923e298cd4cf4e4767d0b1eb4e43",
    "USER_769e3afd72746555185c2e66705bc0897ab6e025",
    "USER_5601d1fc537373afb9d021f5743eb99f8491de99",
    "USER_2ac506652286b4f89fb44940e8fa5f9ce898dab6",
    "USER_c528642096fa0242b8930dadff0c30822b0591af",
    "USER_e886af071c9a8745c6145bf2b03ef6ff5b8ffc68",
    "USER_4afe44e3a373d52a070140962b037bf02c08d37a",
    "USER_672fcb6ac2f8fbd233918fbe4ce23735c212ad3e",
    "USER_267cec60ea376dcf874551ea03b24f9fa85bf91e",
    "USER_e2ea40b14c51fd43c1e193052314020d4c5a8557",
    "USER_d2ca85bc2f22a9866cdaea9fca59d1e254092e81",
    "USER_fa4d413862abcd1571e6c009624950277a98ddcd",
    "USER_b1c2d721c00db749d28614ae68dffa3be5c457fd",
    "USER_030c222b6d1d60284504658c6172cf043147c5b8",
    "USER_2d682ba0bc87c8d194534c575e15e36b29432c8c",
    "USER_d15f6ed60f293f659451bee296ea36507ce5b7bf",
    "USER_b1c2d721c00db749d28614ae68dffa3be5c457fd",
    ]

exceptions = {
    'pill_game_state':{
        'path':'games.pill_game_state',
        'select':['day_pills_time_menu_selected_index','night_pills_time_menu_selected_index','treatment_line'],
        'new_table':pillgame_dict,
        'table_cols':['Time of Day','Pill'],
        },
    'problemsolving':{
        'path':'games.problemsolving',
        'select':['chosen-issue','default_page'],
        'new_table':problemsolving_dict,
        'table_cols':['Issue',
                      'Action','Aim','Alternatives',
                      'Alternatives2','Alternatives3','Ask',],
        },
    'ssnmtree':{
        'path':'games.ssnmtree',
        'select':[],
        'new_table':ssnmtree_dict,
        'table_cols':['Position','Disclosure','Support','Name']
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
        'table_cols':['Date','Page','Seconds on page']
        },
    'firstname':{
        'select':[],
        },
    'fullname':{
        'select':[],
        },
}

def dict_fields(dic):
    "recursively return fields that are not"
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
    "returns unique list of all column names"
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
            extras[k] = [['Patient ID','patientnumber']+v['table_cols'] ] #header

    for r in rows:
        if r[0] in user_black_list:
            continue
        user = [r[0]]
        data = json.loads(r[1])
        for col in main_file_cols:
            user.append( getval(data,col) )
        main.append(user)
        for k,v in extras.items():
            edata = getval(data,exceptions[k]['path'])
            if edata:
                v.extend( exceptions[k]['new_table'](edata, [r[0],data['patientnumber']]) )

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




