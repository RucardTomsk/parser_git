import requests
import os
from time import sleep
import time
import shutil

from random import randint

API_URL = "http://api.github.com"

counter = 0
#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
GITHUB_TOKEN = "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"
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept": "application/vnd.github.v3+json"
}


def get_from_each_dict(data, comand):
    mas = []
    for i in data:
        try:
            mas.append(i[comand])
        except TypeError:
            pass

    return mas


def get_branches(NameAvtor, NameProject):
    global counter
    if counter < 5000:
        repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/branches", headers=headers)
        counter = counter + 1
    else:
        print("ПАУЗА - 1 час")
        sleep(3610)
        repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/branches", headers=headers)
        counter = 1

    branches_json = repos.json()
    branches_array = get_from_each_dict(branches_json, 'name')

    print("Ветви:")
    print(branches_array)
    return branches_array


def get_commits(NameAvtor, NameProject, branches_array):
    global counter
    commit_array = []
    for index in branches_array:
        print(index)
        sha_next = index
        flag_sha = ""
        while (flag_sha != str(sha_next)):
            print("     "+ flag_sha)
            if counter < 5000:
                repos = requests.get(
                    API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits?per_page=100&sha=" + str(sha_next),
                    headers=headers)
                counter = counter + 1
            else:
                print("ПАУЗА - 1 час")
                sleep(3610)
                repos = requests.get(
                    API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits?per_page=100&sha=" + str(sha_next),
                    headers=headers)
                counter = 1

            commit_json = repos.json()
            new_mas = get_from_each_dict(commit_json, 'sha')

            for g in range(0, len(new_mas)):
                commit_array.append(new_mas[g])

            try:
                flag_sha = new_mas[0]
            except IndexError:
                break

            sha_next = commit_array[len(commit_array) - 1]
    print("Количество коммитов: " + str(len(commit_array)))

    FAIL_ALL_COMMITS = open(NameProject+"/all_commits.txt",'w')
    commit_str = ""
    for i in commit_array:
        commit_str = commit_str + i + ','

    FAIL_ALL_COMMITS.write(commit_str)
    FAIL_ALL_COMMITS.close()
    return commit_array


def сleaning_empty_folders(NameProject):
    dirlist = [item for item in os.listdir(NameProject) if os.path.isdir(os.path.join(NameProject, item))]

    for path in dirlist:
        dirlist2 = [item for item in os.listdir(NameProject + '/' + path) if
                    os.path.isdir(os.path.join(NameProject + '/' + path, item))]
        print(dirlist2)
        for path2 in dirlist2:
            dirlist3 = [item for item in os.listdir(NameProject + '/' + path + '/' + path2) if
                        os.path.isdir(os.path.join(NameProject + '/' + path + '/' + path2, item))]
            print(dirlist3)
            for path3 in dirlist3:
                directory_list = list()
                for root, dirs, files in os.walk(NameProject + '/' + path + '/' + path2+ '/' + path3, topdown=False):
                    for name in files:
                        directory_list.append(os.path.join(root, name))
                if len(directory_list) == 0:
                    shutil.rmtree(os.path.join(NameProject + '/' + path + '/' + path2+ '/' + path3))

            dirlist3 = [item for item in os.listdir(NameProject + '/' + path + '/' + path2) if
                        os.path.isdir(os.path.join(NameProject + '/' + path + '/' + path2, item))]
            if len(dirlist3) == 0:
                shutil.rmtree(os.path.join(NameProject + '/' + path + '/' + path2))

        dirlist2 = [item for item in os.listdir(NameProject + '/' + path) if
                    os.path.isdir(os.path.join(NameProject + '/' + path, item))]
        if len(dirlist2) == 0:
            shutil.rmtree(os.path.join(NameProject + '/' + path))

    os.remove(NameProject + '/all_commits.txt')
    os.remove(NameProject + '/last_commit.txt')

def checking_for_a_unicode_error(way,text):
    text = text.replace(' ','')
    INTERMEDIATE_FILE = open(way + "/intermediate_file.txt", "w")
    try:
        intermediate_text = text
        com = ""
        for text_position in range(0, len(intermediate_text)):
            try:
                INTERMEDIATE_FILE.write(intermediate_text[text_position])
                com = com + intermediate_text[text_position]
            except UnicodeEncodeError:
                pass
    except KeyError:
        INTERMEDIATE_FILE.close()
        os.remove(way+ "/intermediate_file.txt")
        return 0

    INTERMEDIATE_FILE.close()
    os.remove(way + "/intermediate_file.txt")
    return com

                       
def write_commits(sha, NameAvtor, NameProject,mas1,mas2,rewrite_flag):
    global counter
    for index in sha:
        print(index)
        if counter < 5000:
            repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits/" + index,headers=headers)
            counter = counter + 1
        else:
            print("ПАУЗА - 1 час")
            sleep(3610)
            repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits/" + index,
                                 headers=headers)
            counter = 1
        try:
            commit_f = repos.json()['files']
            commit_a = repos.json()['author']
            commit_d = repos.json()['commit']['author']
            commit_l = repos.json()['commit']['committer']
        except:
            continue


        try:
             login = checking_for_a_unicode_error(NameProject,commit_l["name"])
        except TypeError:
            try:
                login = checking_for_a_unicode_error(NameProject,commit_a["login"])
            except TypeError:
                login = checking_for_a_unicode_error(NameProject,commit_d["name"])

        if login == 0:
            continue

        if login == "":
            try:
                if mas1.count(commit_a['login']) == 0:
                    mas1.append(commit_a['login'])
                    mas2.append("Asian№"+ str(randint(0,10000)))
                    login = mas2[mas1.index(commit_a['login'])]
                else:
                    login = mas2[mas1.index(commit_a['login'])]
            except:
                if mas1.count(commit_d["name"]) == 0:
                    mas1.append(commit_d["name"])
                    mas2.append("Asian№"+ str(randint(0,10000)))
                    login = mas2[mas1.index(commit_d["name"])]
                else:
                    login = mas2[mas1.index(commit_d["name"])]

        if os.path.exists(NameProject + "/" + login):
            pass
        else:
            os.mkdir(NameProject + "/" + login)

        data = commit_d["date"].split(":")[0][:10]

        if os.path.exists(NameProject + "/" + login + "/" + data):
            pass
        else:
            os.mkdir(NameProject + "/" + login + "/" + data)

        for d in commit_f:

            p = d["filename"].split(".")[len(d["filename"].split("."))-1]
            s = ""
            for i in range(0, len(p)):
                if p[i] != '/':
                    s = s + p[i]

            p = s

            if os.path.exists(NameProject + "/" + login + "/" + data + "/" +
                              p):
                pass
            else:
                os.mkdir(NameProject + "/" + login + "/" + data + '/' +
                         p)
            try:
                com = checking_for_a_unicode_error(NameProject + "/" + login + "/" + data+ '/'+ p,d["patch"])
            except KeyError:
                continue                                                               

            if com == 0:
                continue

            FILE_WITH_COMMITS = open(
                NameProject + "/" + login + "/" + data+ '/'+ p + "/commits.txt", "w")

            FILE_WITH_COMMITS.write(com)

            FILE_WITH_COMMITS.close()

            FILE_WITH_COMMITS = open(
                NameProject + "/" + login + "/" + data+ '/'+ p + "/commits.txt", "r")
            FILE_WITH_COMMITS2 = open(
                NameProject + "/" + login + "/" + data+ '/'+ p + "/commits2.txt",
                "w")

            for i in FILE_WITH_COMMITS:
                i = i.strip()
                if len(i) != 0:
                    if i[0] == "+":
                        FILE_WITH_COMMITS2.write(i.strip() + '\n')
            FILE_WITH_COMMITS.close()
            FILE_WITH_COMMITS2.close()

            with open(NameProject + "/" + login + "/" + data + '/'+ p+ "/commits2.txt") as f:
                line_count = 0
                for line in f:
                    line_count += 1

            if os.path.getsize(NameProject + "/" + login + "/" + data+ '/'+ p + "/commits2.txt") > 0 and line_count >= 10:
                os.remove(
                    NameProject + "/" + login + "/" + data+ '/'+ p + "/commits.txt")
                try:
                    os.rename(NameProject + "/" + login + "/" + data+ '/'+ p + "/commits2.txt",
                              NameProject + "/" + login + "/" + data+ '/'+ p + "/" +
                              d['sha'] + ".txt")
                except FileExistsError:
                    os.remove(NameProject + "/" + login + "/" + data+ '/'+ p + "/commits2.txt")
            else:
                os.remove(
                    NameProject + "/" + login + "/" + data+ '/'+ p + "/commits.txt")
                os.remove(
                    NameProject + "/" + login + "/" + data+ '/'+ p + "/commits2.txt")

        FAIL_LAST_COMMIT = open(NameProject+"/last_commit.txt","w")
        FAIL_LAST_COMMIT.write(index)
        FAIL_LAST_COMMIT.close()

                # UnicodeEncodeError:
                #    UnboundLocalError:
                # TypeError:
                # KeyError:
                # FileExistsError:

def main():
    start_time = time.time()
    FILE_PROJECT_AUTHOR = open("project_author.txt", "r")
    FILE_REQUEST_COUNTER = open("request_counter.txt", "r")

    global counter
    counter = int(FILE_REQUEST_COUNTER.readline())
    print("Запросов на данный момент: " + str(counter))

    for index in FILE_PROJECT_AUTHOR:
        print(index)
        project_author = index.strip().split(',')
        print("Проект " + project_author[1])
        rewrite_flag = True

        if os.path.exists(project_author[1]):
            a = input("Проект уже существует, перезаписать? (y/n)") 
            if a == "y":
                rewrite_flag = True
            if a == "n":
                rewrite_flag = False

            if rewrite_flag == True:
                path = os.path.join(project_author[1])
                shutil.rmtree(path)

        if os.path.exists(project_author[1]) == False:
            os.mkdir(project_author[1])

        if rewrite_flag == True:
            sha = get_commits(project_author[0], project_author[1],get_branches(project_author[0], project_author[1]))
        else:
            FAIL_ALL_COMMITS = open(project_author[1]+'/all_commits.txt','r')
            sha_str = FAIL_ALL_COMMITS.readline()
            FAIL_ALL_COMMITS.close()

            sha = sha_str.split(",")

            flag = True
            mas = []
            FAIL_LAST_COMMIT = open(project_author[1]+'/last_commit.txt','r')
            last_sha = FAIL_LAST_COMMIT.readline()
            FAIL_LAST_COMMIT.close()
            for i in sha:
                if i != last_sha and flag == True:
                    continue
                else:
                    mas.append(i)
                    flag = False
            sha = mas

        write_commits(sha,project_author[0], project_author[1],[],[],rewrite_flag)

        print("Конец проверки папок для проекта - " + project_author[1])

        сleaning_empty_folders(project_author[1])

    FILE_PROJECT_AUTHOR.close()
    FILE_REQUEST_COUNTER.close()

    FILE_REQUEST_COUNTER = open("request_counter.txt", "w")
    FILE_REQUEST_COUNTER.write(str(counter))
    print(str(time.time() - start_time) + " seconds")


if __name__ == '__main__':
    main()