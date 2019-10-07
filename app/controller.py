import ldap

#Define main variables
#LDAP server
AD_SERVER = ''
#Your domain name (Distinguished) 
AD_BASEDN = ''
#LDAP group to search(Distinguished)
AD_GROUP_BASEDN = ''
#LDAP user('username'@'domainName')
AD_BIND_USER = ''
#LDAP user password
AD_BIND_PWD = ''

def ad_auth(username=AD_BIND_USER, password=AD_BIND_PWD, address=AD_SERVER):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)

    try:
        conn.simple_bind_s(username, password)
        # print('Succesfully authenticated')
    except ldap.INVALID_CREDENTIALS:
        print('Wrong password')
        return False
    except ldap.SERVER_DOWN:
        print('Server ', AD_SERVER,'not available')
        return False
    
    return conn
# Function that returns list of group members displayName
def get_users_displayName(ad_conn = ad_auth(), basedn = AD_GROUP_BASEDN):
    result = ad_conn.search_s(basedn, ldap.SCOPE_BASE, attrlist=['member'])
    result_tmp = result[0][1]['member']
    users = []
    for i in range(0, len(result_tmp)):
        users.append((result_tmp[i].decode('utf-8').split(',')[0].replace('CN=','')))
    return users

# Functions that returns list of group members sAMAccountName, based on list that you get in get_users_displayName
def get_users_sAMAccountName(ad_conn=ad_auth(), basedn=AD_BASEDN, userList=get_users_displayName()):
    user_tmp = []
    users_sAMAN = []
    for i in range(0, len(userList)):
        filter_query = '(&(objectClass=user)(displayName=' + userList[i] + '))'
        user_tmp.append(ad_conn.search_s(basedn, ldap.SCOPE_SUBTREE, filter_query, ['sAMAccountName']))

    for i in range(0, len(user_tmp)):
        users_sAMAN.append(user_tmp[i][0][1]['sAMAccountName'])

    for i in range(0, len(users_sAMAN)):
        users_sAMAN[i] = users_sAMAN[i][0].decode('utf-8')
    return users_sAMAN