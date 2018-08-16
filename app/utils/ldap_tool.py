#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ldap, threading, traceback, hashlib

from get_dvd_conf import get_config

# 导入log驱动
from log_tool import LogsTool


class LdapTool(object):
    _instance_lock = threading.Lock()

    def __init__(self, config):
        self.log_ldap = LogsTool('ldap').get_instance()
        self.config_name = config
        self._con = self._get_connection()

    def __new__(cls, *args, **kwargs):
        if not hasattr(LdapTool, "_instance"):
            with LdapTool._instance_lock:
                if not hasattr(LdapTool, "_instance"):
                    LdapTool._instance = object.__new__(cls)
        return LdapTool._instance

    def _get_connection(self):
        try:
            _lcon = ldap.initialize(get_config(self.config_name, 'path'))
            _lcon.protocol_version = ldap.VERSION3
            _lcon.simple_bind_s(get_config(self.config_name, 'user'), get_config(self.config_name, 'passwd'))

            self.log_ldap.info('[The LDAP Connect success] [Config:{}]'.format(self.config_name))

            return _lcon

        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP connect failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                         traceback.format_exc()))
            return False


    def search(self, name):
        try:
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = None
            findname = 'cn=' + name
            result_id = self._con.search(get_config(self.config_name, 'base_dn'), searchScope, findname,
                                         retrieveAttributes)
            result_type, result_data = self._con.result(result_id)

            result = True if len(result_data) != 0 else False

            self.log_ldap.info('[Search the Ldap name success] [Name:{}] [Result:{}]'.format(name, result))

            return result

        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP search failed] [Config:{}] [ErrorInfo:{}] [Trace:{}]'.format(self.config_name, e,
                                                                                        traceback.format_exc()))
            return False


    def show(self, name):
        try:
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = None
            findname = 'cn=' + name
            result_id = self._con.search(get_config(self.config_name, 'base_dn'), searchScope, findname,
                                         retrieveAttributes)
            result_type, result_data = self._con.result(result_id)

            result = result_data if len(result_data) != 0 else False

            self.log_ldap.info(
                "[The LDAP execute get information success] [Config:{}] [Name:{}]".format(self.config_name, name))

            return result

        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP execute get information failed] [Config:{}] [Name:{}] [ErrorInfo:{}] [Trace:{}]'.format(
                    self.config_name, name, e, traceback.format_exc()))
            return False


    def get_info(self, name, value_type):
        # value :uid, passwd, mobile, mail
        # 用法：get_info('mengzhe', 'passwd') 函数直接返回内容，用户不存在返回false，信息不存在返回"value is error"

        try:

            result_data = self.show(name)

            if len(result_data) == 0:
                result = "User is No found"
            else:
                a, b = result_data[0]
                if value_type is 'uid':
                    result = b['uid'][0]
                elif value_type is 'passwd':
                    result = b['userPassword'][0]
                elif value_type is 'mobile':
                    result = b['mobile'][0]
                elif value_type is 'mail':
                    result = b['mail'][0]
                else:
                    result = "Value is no found"

            self.log_ldap.info(
                '[The LDAP execute get information success] [Name:{}] [Value:{}]'.format(name, value_type))
            return result

        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP execute get information failed] [Config:{}] [Name:{}] [Value:{}] [ErrorInfo:{}] [Trace:{}]'.format(
                    self.config_name, name, value_type, e, traceback.format_exc()))
            return False


    def update_passwd(self, name, passwd):
        '''
         MOD_ADD: 如果属性存在，这个属性可以有多个值，那么新值加进去，旧值保留
         MOD_DELETE ：如果属性的值存在，值将被删除
         MOD_REPLACE ：这个属性所有的旧值将会被删除，这个值被加进去

        dn: cn=test, ou=magicstack,dc=test, dc=com
        attr_list: [( ldap.MOD_REPLACE, 'givenName', 'Francis' ),
                    ( ldap.MOD_ADD, 'cn', 'Frank Bacon' )
                   ]
        '''

        try:
            result_data = self.show(name)

            dn = result_data[0][0]

            alter_list = [(ldap.MOD_REPLACE, 'userPassword', passwd)]
            result_num = self._con.modify_s(dn, alter_list)[0]

            result = True if result_num == 103 else False

            self.log_ldap.info('[The LDAP execute update_passwd success] [Name:{}]'.format(name))

            return result

        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP execute update_passwd failed] [Config:{}] [Name:{}] [ErrorInfo:{}] [Trace:{}]'.format(
                    self.config_name, name, e, traceback.format_exc()))
            return False

    def delete(self, name):
        try:
            result_data = self.show(name)

            dn = result_data[0][0]

            result_num = self._con.delete_s(dn)[0]

            result = True if result_num == 107 else False

            self.log_ldap.info('[The LDAP execute delete success] [Name:{}]'.format(name))

            return result
        except ldap.LDAPError as e:
            self.log_ldap.error(
                '[The LDAP execute delete failed] [Config:{}] [Name:{}] [ErrorInfo:{}] [Trace:{}]'.format(
                    self.config_name, name, e, traceback.format_exc()))
            return False


# l = LdapTool('ldapconfig_prod')
#
# with open('name', 'r') as f:
#     for line in f:
#         if l.search(line[:-1]):
#             r = l.get_info(line[:-1],'passwd')
#             print line[:-1]+ ': ' +r
# md5 = hashlib.md5()
# l = LdapTool('ldapconfig_prod')
# with open('name','r')as f:
#     for t in f:
#         if l.search(t[:-1]):
#             md5.update("davdian" + t[:-1])
#             p = md5.hexdigest()[0:15:2]
#             l.update_passwd(t[:-1],p)
#             print(t[:-1]+": "+p)
#         else:
#             print t[:-1]
