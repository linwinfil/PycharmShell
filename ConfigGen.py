#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import base64
from pyDes import des, PAD_PKCS5, ECB
from json import JSONDecodeError
import json

from tkinter import messagebox
from tkinter import *


class TkinterUtil(object):

    def __init__(self):
        object.__init__(self)

    @staticmethod
    def get_screen_size(window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    @staticmethod
    def get_window_size(window):
        return window.winfo_reqwidth(), window.winfo_reqheight()

    @staticmethod
    def center_window(root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(size)


class DesUtil(object):

    def __init__(self, secret_key):
        object.__init__(self)
        self.key = secret_key

    def encrypt(self, s):
        iv = self.key[:8]
        print(iv)
        k = des('        ')
        k.setKey(self.key)
        k.setMode(ECB)
        #print(s)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return en

    def descrypt(self, s):
        iv = self.key
        print(iv)
        k = des('        ')
        k.setKey(self.key)
        k.setMode(ECB)
        #print(s)
        de = k.decrypt(s, padmode=PAD_PKCS5)
        return de


class ConfigFrom(object):

    def __init__(self, security_key=''):
        object.__init__(self)
        self.security_key = security_key
        self.root = Tk()
        self.root.title(u'AT工作室Firebase远程配置工具')

        # 居中显示
        TkinterUtil.center_window(self.root, 800, 430)
        # self.root.geometry('800x430')

        self.sk_input_val = StringVar()
        # self.ec_text_val = StringVar()

        self.sk_entry = None
        self.encrypt_button = None
        self.descrypt_button = None
        self.head_frm_init()

        # 明文区
        self.ec_text = None
        self.encrypted_content_area_init()

        # 密文区
        self.dc_text = None
        self.descrypted_content_area_init()

        self.root.mainloop()

    def head_frm_init(self):
        sk_frm = Frame(self.root)
        opt_frm = Frame(self.root)

        Label(
            sk_frm, text=u"密钥", font=('Aria', 12)
        ).grid(row=0, column=0)
        self.sk_entry = Entry(sk_frm, textvariable=self.sk_input_val)
        self.sk_input_val.set(self.security_key)
        self.sk_entry.grid(row=0, column=1, sticky=W + E + N + S)
        sk_frm.grid(row=0, column=0)

        self.encrypt_button = Button(opt_frm, text=u"加密", width=6, height=2, command=self.encrypt)
        self.encrypt_button.grid(row=0, column=1, sticky=W + E + N + S)

        self.descrypt_button = Button(opt_frm, text=u"解密", width=6, height=2, command=self.descrypt)
        self.descrypt_button.grid(row=0, column=0, sticky=W + E + N + S)

        opt_frm.grid(row=0, column=1)

    def encrypted_content_area_init(self):
        Label(
            self.root,
            text=u"明文", font=('Aria', 12)
        ).grid(row=1, column=0)
        self.ec_text = Text(self.root, fg="white", bg="dimgray", width=56)
        self.ec_text.grid(row=2, column=0)

    def descrypted_content_area_init(self):
        Label(
            self.root,
            text=u"密文", font=('Aria', 12)
        ).grid(row=1, column=1)
        self.dc_text = Text(self.root, fg="white", bg="dimgray", width=56)
        self.dc_text.grid(row=2, column=1)

    def descrypt(self):
        key = self.sk_entry.get()
        if key:
            key = key.strip()
        else:
            messagebox.showinfo(title="Tips", message=u"请输入密钥")
            return

        try:
            des_util = DesUtil(secret_key=key)
            data = self.dc_text.get(0.0, END)
            decoded = base64.urlsafe_b64decode(data)
            des_data = des_util.descrypt(decoded)
            print('des_data:',des_data)
            # print(data)

            result = json.loads(des_data, encoding='utf-8')
            #print(result)

            format_json = json.dumps(result, indent=4)
            self.ec_text.delete(1.0, END)
            self.ec_text.insert(INSERT, format_json)
        except JSONDecodeError as e1:
            messagebox.showinfo(title="Tips", message=u"解密后明文不是json格式，请检查")
        except Exception as e2:
            print(e2)
            messagebox.showinfo(title="Tips", message=u"解密失败，请重试")

    def encrypt(self):
        key = self.sk_entry.get()
        if key:
            key = key.strip()
        else:
            messagebox.showinfo(title="Tips", message=u"请输入密钥")
            return

        try:
            des_util = DesUtil(secret_key=key)
            data = self.ec_text.get(0.0, END)
            #print(data)


            obj_data = json.loads(data, encoding='utf-8')
            data = json.dumps(obj_data)
            #obj_data_b = bytes(data,encoding='utf-8')
            # print('obj_data:',obj_data)
            # print(data)

            encr_data = des_util.encrypt(data)
            encoded = base64.urlsafe_b64encode(encr_data)

            self.dc_text.delete(1.0, END)
            self.dc_text.insert(INSERT, encoded)
        except JSONDecodeError as e1:
            messagebox.showinfo(title="Tips", message=u"明文不是json格式，请检查")
        except Exception as e2:
            print(e2)
            messagebox.showinfo(title="Tips", message=u"加密失败，请重试")


if __name__ == "__main__":
    sk = 'yJYAskGNpYjNlnQ1'
    form = ConfigFrom(sk)
