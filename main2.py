import requests
import os
from time import sleep
import time

API_URL = "http://api.github.com"

counter = 0

GITHUB_TOKEN = "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"
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept": "application/vnd.github.v3+json"
}

def get_from_each_dict(data, comand):
    mas = []
    for i in data:
        mas.append(i[comand])

    return mas

def get_branches(NameAvtor, NameProject):
    global counter
    if counter<5000:
        repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/branches", headers=headers)
        counter = counter + 1   
    else:
        print("ПАУЗА - 1 час")
        sleep(3610)
        repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/branches", headers=headers)
        counter = 1

    branches_json = repos.json()
    branches_array = get_from_each_dict(branches_json,'name')

    print("Ветви:")
    print(branches_array)
    return branches_array

def get_commits(NameAvtor, NameProject, branches_array):
    global counter
    commit_array = []
    for index in branches_array:
        sha_next = index
        flag_sha = ""
        while(flag_sha != str(sha_next)):
            if counter < 5000:
                repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits?per_page=100&sha="+str(sha_next), headers=headers)
                counter = counter + 1
            else:
                print("ПАУЗА - 1 час")
                sleep(3610)
                repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits?per_page=100&sha="+str(sha_next), headers=headers)
                counter = 1

            commit_json = repos.json()
            new_mas = get_from_each_dict(commit_json,'sha')

            for g in range(0,len(new_mas)):
                commit_array.append(new_mas[g])

            flag_sha = new_mas[0]

            sha_next = commit_array[len(commit_array)-1]
    print("Количество коммитов: " + str(len(commit_array)))
    return commit_array

def write_commits(sha, NameAvtor, NameProject):
    global counter
    os.mkdir(NameProject)
    for index in sha:
        print(index)
        if counter < 5000:
            repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits/" + index, headers=headers)
            counter = counter + 1        
        else:
            print("ПАУЗА - 1 час")
            sleep(3610)
            repos = requests.get(API_URL + "/repos/" + NameAvtor + "/" + NameProject + "/commits/" + index, headers=headers)
            counter = 1
        try:
            commit_f = repos.json()['files']
            commit_a = repos.json()['author']
            commit_d = repos.json()['commit']['author']
        except KeyError:
            pass

        commits_array = []

        try:
            try:
            
                if os.path.exists(NameProject + "/" + commit_a["login"]):
                    pass
                else:
                    os.mkdir(NameProject + "/" + commit_a["login"])

                if os.path.exists(NameProject + "/" + commit_a["login"] + "/" + commit_d["date"].split(":")[0][:10]):
                    pass
                else:
                    os.mkdir(NameProject + "/" + commit_a["login"] + "/" + commit_d["date"].split(":")[0][:10])
            
            except KeyError:
                print("ERROR")
        except TypeError:
            print("ERROR")

        try:
            for d in commit_f:
                com = d['patch']
                commits_array.append(com.strip())
        except KeyError:
            print("ERROR")

        try:
            try:
                try:
                    try:
                        FILE_WITH_COMMITS = open(NameProject + "/" + commit_a['login'] + "/" + commit_d["date"].split(":")[0][:10] + "/commits.txt", "w")

                        for i in commits_array:
                            FILE_WITH_COMMITS.write(i.strip() + '\n')
                        FILE_WITH_COMMITS.close()

                        FILE_WITH_COMMITS = open(NameProject + "/" + commit_a['login'] + "/" + commit_d["date"].split(":")[0][:10] + "/commits.txt", "r")
                        FILE_WITH_COMMITS2 = open(NameProject + "/" + commit_a['login'] + "/" + commit_d["date"].split(":")[0][:10] + "/commits2.txt", "w")

                        for i in FILE_WITH_COMMITS:
                            i = i.strip()
                            if len(i) != 0:
                                if i[0] == "+":
                                    FILE_WITH_COMMITS2.write(i.strip() + '\n')
                        FILE_WITH_COMMITS.close()
                        FILE_WITH_COMMITS2.close()

                        os.remove(NameProject + "/" + commit_a['login'] + "/" + commit_d["date"].split(":")[0][:10] + "/commits.txt")
                        os.rename(NameProject + "/" + commit_a['login'] + "/" + commit_d["date"].split(":")[0][:10] + "/commits2.txt",NameProject + "/" + commit_a['login'] + "/" + commit_d['date'].split(":")[0][:10] + "/" + index + ".txt")
                    except FileExistsError:
                        print("ERROR")
                except KeyError:
                    print("ERROR")
            except TypeError:
                print("ERROR")
        except UnicodeEncodeError:
            print("ERROR")


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
        write_commits(get_commits(project_author[0], project_author[1],get_branches(project_author[0], project_author[1])), project_author[0], project_author[1])

    FILE_PROJECT_AUTHOR.close()
    FILE_REQUEST_COUNTER.close()

    FILE_REQUEST_COUNTER = open("request_counter.txt", "w")
    FILE_REQUEST_COUNTER.write(str(counter))
    print(str(time.time()-start_time)+ " seconds")

if __name__ == '__main__':
    main()