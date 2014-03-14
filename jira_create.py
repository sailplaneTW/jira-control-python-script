#!/usr/bin/env python

import json
import os
import subprocess

class JiraControl:
    def __init__(self, my_name = '', my_pass = ''):
        self.username, self.password = my_name, my_pass
        self.jira_rest_api_url = 'xxx' # set jira api url
    def query_issue(self, issue):
		# TODO : myabe find "curl" command from /usr/bin/env too ?
        command = 'curl -D- -u ' + self.username + ':' + self.password + ' -X GET -H "Content-Type: application/json" "' +self.jira_rest_api_url + 'issue/' + issue + '"'
        command_result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
        n = command_result.index('\r')
        return command_result[n+1:]
    def print_all(self):
        print self.username + ' ' + self.password
    def get_gira_issue_list(self):
        return ['bug', 'new feature', 'task', 'improvement']
    def generate_create_issue_json(self, project, summary, description, issue_type):
        summary_json = "'summary':'"+summary+"'"
        description_json = "'description':'"+description+"'"
        issue_json = "'issuetype':{'name':'"+issue_type+"'}" 


class GitControl:
    def __init__(self):
        self.jira_type_list = JiraControl().get_gira_issue_list()
    def get_head_title(self):
		# TODO : myabe find "git" command from /usr/bin/env too ?
        command = 'git show --summary'
        command_result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split('\n')
        return command_result[4].strip()
    def get_head_content(self):
        command = 'git show --summary'
        command_result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split('\n')
        issue_type_line = [i for i in command_result if i.strip().lower().split(' ')[0].split(':')[0] in self.jira_type_list][0]
        n = command_result.index(issue_type_line)
        issue_type = issue_type_line.strip().lower().split(' ')[0].split(':')[0]
        content_result = ''.join([i.strip()+' ' for i in command_result[6:n-1]])
        return content_result, issue_type[0:1].upper()+issue_type[1:].lower()
    def get_project(self):
        pass # FIXME


# ---------------------------------------------------------- #

my_name = my_pass = ''
# read username/password from ~/.jira_account, and the contents are
# User xxx
# Password xxx
with open(os.environ['HOME'] + '/.jira_account', 'r') as f :
    for line in f:
        key, value = line.split(' ')
        if key == 'User' :
            my_name = value.strip()
        elif key == 'Password':
            my_pass = value.strip()

if my_name != '' and my_pass != '':
    # get data from git
    git_obj = GitControl()
    summary = git_obj.get_head_title()
    description, issue_type = git_obj.get_head_content()
    project = git_obj.get_project()

    # create issue
    jira_obj = JiraControl(my_name, my_pass)
    # Get issue with issue id
	print jira_obj.query_issue('XXX-XXX')

	# FIXME : ready for implement
    create_issue_json_data = jira_obj.generate_create_issue_json(project, summary, description, issue_type)
    print create_issue_json_data
else:
    print 'read config error'


