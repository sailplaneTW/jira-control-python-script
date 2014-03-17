#!/usr/bin/env python

import json
import os
import subprocess

class JiraDataJson:
    def __init__(self):
        pass
    def add_braces(self, data):
        return '{' + data + '}'
    def add_key_value(self, key, value):
        return '"' + key + '" : ' + value
    def generate_create_issue_json(self, project, summary, description, issue_type):
        project_json = self.add_key_value('project', self.add_braces(self.add_key_value('key', project)))
        summary_json = self.add_key_value('summary', summary)
        description_json = self.add_key_value('description', description)
        issuetype_json = self.add_key_value('issuetype', self.add_key_value('name', issue_type))
        fields_json = self.add_braces(project_json+','+summary_json+','+description_json+','+issuetype_json)
        return self.add_braces(self.add_key_value('fields', fields_json))

class JiraControl:
    def __init__(self, my_name = '', my_pass = '', my_jira_url = ''):
        self.username, self.password = my_name, my_pass
        self.jira_rest_api_url = my_jira_url
    def get_gira_issue_list(self):
        return ['bug', 'new feature', 'task', 'improvement']
    def query_issue(self, issue):
		# TODO : myabe find "curl" command from /usr/bin/env too ?
        command = 'curl -D- -u ' + self.username + ':' + self.password + ' -X GET -H "Content-Type: application/json" "' +self.jira_rest_api_url + 'issue/' + issue + '"'
        command_result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
        n = command_result.index('\r')
        return command_result[n+1:]
	def create_issue(self, issue_json):
		command = 'curl -D- -u ' + self.username + ':' + self.password + ' -X POST --data ' + issue_json + ' -H "Content-Type: application/json" "' +self.jira_rest_api_url + 'issue/'
		command_result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
		return command_result

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
        return 'xxx' # FIXME

# ---------------------------------------------------------- #

my_name = my_pass = my_jira_url = ''
# read username/password from ~/.jira_script_env, and the contents are
# User xxx
# Password xxx
with open(os.environ['HOME'] + '/.jira_script_env', 'r') as f :
    for line in f:
        key, value = line.split(' ')
        if key == 'User' :
            my_name = value.strip()
        elif key == 'Password':
            my_pass = value.strip()
        elif key == 'JiraApiUrl':
            my_jira_url = value.strip()

if my_name != '' and my_pass != '' and my_jira_url:
    # get data from git
    git_obj = GitControl()
    summary = git_obj.get_head_title()
    description, issue_type = git_obj.get_head_content()
    project = git_obj.get_project()

    # create issue
    jira_obj = JiraControl(my_name, my_pass, my_jira_url)
    # Get issue with issue id
	#print jira_obj.query_issue('XXX-XXX')

	# FIXME : ready for implement
    issue_json_data = JiraDataJson().generate_create_issue_json(project, summary, ''.join(description), ''.join(issue_type))
    print issue_json_data
	#print jira_obj.create_issue(issue_json_data)
else:
    print 'read config error'


