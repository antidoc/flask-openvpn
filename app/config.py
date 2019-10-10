
class ldap_conn():
    def __init__(self):
        #LDAP server
        self.AD_SERVER = ''
        #Your domain name (Distinguished) 
        self.AD_BASEDN = ''
        #LDAP group to search(Distinguished)
        self.AD_GROUP_BASEDN = ''
        #LDAP user('username'@'domainName')
        self.AD_BIND_USER = ''
        #LDAP user password
        self.AD_BIND_PWD = ''

class org_fields():
    def __init__(self):
        # Org fields
        self.C = ''
        self.ST = ''
        self.L = ''
        self.Org = ''
        self.OU = ''
        self.email = ''
        #ca.crt and ca.key location
        self.CACERT = ''
        self.CAKEY = ''