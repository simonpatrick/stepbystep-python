# _*_ coding=utf-8 _*_
import base64
import cmd
import os
import shutil
import subprocess
import re
import requests


__author__ = 'patrick'


class SvnRbClient(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        # read .reviewboardrc file as configuration
        self.rb_configuration = '.reviewboardrc'
        self.rb_url = '192.168.3.180'
        configurations = self.parse_rb_config_file()
        try:
            self.rb_audit_user = configurations['TARGET_PEOPLE']
            self.rb_username=configurations['username'.upper()]
            self.rb_password=configurations['password'.upper()]
            self.repository_name=configurations['REPOSITORY']
        except KeyError:
            print "setup is not completed,need to run setup manually"
            pass

        self.svn_diff_command = 'svn diff '
        self.svn_status_xml = 'svn status --xml'
        self.svn_status = 'svn status '
        self.svn_add = 'svn add '
        self.temp_diff_file = 'differ_temp' + os.path.sep + 'temp_differ_file.txt'
        self.rb_post = "rbt post --diff-filename %s --target-people %s --summary %s --description %s "
        self.rb_post_w_rrId = "rbt post -r %s"
        self.rb_publish = "rbt publish -r %s"

    intro = '''
        Dooioo Review Board Client, ? for help, and the total command lists:
        1. setup:setup review board setting
        2. pre:precommit your changes
        3. u_pre:update date your precommit
        4. ss:svn status,find svn status for the working copies
        5. sa:svn add,add files to local svn
        6. sd:svn delete,delete svn file
        7. sci:svn commit,commit the changes by review request id
        8. sre: revert changes
        9. sdiff: generate differ file
        10. exit: exit the client
    '''

    prompt = '(Dooioo RB Client)'

    def do_setup(self, arg):
        print "setup reviewboard configuration:"
        prompt = "<"
        print "please input your Review Board ID/Dooioo Employee ID:"
        self.rb_username = raw_input(prompt)
        print "Your review board ID %s" % (self.rb_username)
        print "please input your Review Board password："
        self.rb_password = raw_input(prompt)
        print "your review board password:%s" % (self.rb_password)
        print "please input your default reviewer employee ID:"
        self.rb_audit_user = raw_input(prompt)
        print "Default Review Employee ID:%s" % (self.rb_audit_user)

        rbt_setup_repo_cmd = 'rbt setup-repo --server %s --username %s --password %s' % (
            self.rb_url, self.rb_username, self.rb_password)
        print rbt_setup_repo_cmd
        subprocess.call(rbt_setup_repo_cmd, shell=True)
        # p = subprocess.Popen(rbt_setup_repo_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # commands.getstatusoutput(rbt_setup_repo_cmd)
        with open(self.rb_configuration, mode='a') as f:
            f.write("USERNAME=%s" % self.rb_username)
            f.write("\n")
            f.write("PASSWORD=\"%s\"" % self.rb_password)
            f.write('\n')
            f.write("TARGET_PEOPLE=%s" % self.rb_audit_user)
            f.write('\n')
            f.write("OPEN_BROWSER=True")
        # todo reload the configuration

    def do_ss(self, arg):
        self.get_changed_files()

    def do_pre(self, arg):
        """
        pre-commit changes to review board,the steps:
        # get all changed file lists
        # pass selected file to generate diff files
        # prompt summary,description,target reviewer for issues a review request draft
        # rbt post --summary %s --description %s --open_browser True --diff-filename=
        # rbt publish:publish draft review request
        # rbt get request id, and move the diff file to a folder which named as the request id
        # also create the review requests notes file
        :param arg: None args passed, leave for parsing
        :return:
        """

        print "pre-commit the changes"
        return_content = subprocess.Popen(self.svn_status, shell=True, stdout=subprocess.PIPE)
        result = return_content.communicate()
        # list all the status
        changed_file = result[0].split("\n")
        parsed_changed_file = self.get_changed_files()

        print "Please select the files IDs which your want to commit，eg.0,1,2,3, or Enter for All Files"
        prompt = "<"
        post_file_index = raw_input(prompt)
        if len(post_file_index) == 0:
            print "Files you selected:"
            submitted_file_list = self.pre_precommit(parsed_changed_file)
        else:
            print "Your selected File List:" + post_file_index
            submitted_file_list = self.pre_precommit(parsed_changed_file, post_file_index)

        print submitted_file_list + " is ready to post to review board......"
        # process rbt post to submit review request
        prompt = "Please input your reviewer ID,Entry for default Reviewer> "
        target_people = unicode(raw_input(prompt), 'utf-8')
        if len(target_people) == 0:
            target_people = self.rb_audit_user

        prompt = "Please input summary for your changes,it is nice to provide your Bug No:>"
        summary = unicode(raw_input(prompt), 'utf-8')
        prompt = "Please input detail description for your changes, Enter for use Summary as your detail description:"
        description = unicode(raw_input(prompt), 'utf-8')
        if len(description) == 0:
            description = summary

        # post_command = self.rb_post % (self.temp_diff_file, target_people, summary, description)
        # print post_command + " posting to review board to create draft request review......."
        try:
            # post_rest = subprocess.Popen(post_command, shell=True, stdout=subprocess.PIPE).communicate()

            # print 'result:' + post_rest[0]
            # rr_id = re.findall(r'[#](\d+)', post_rest[0])[0]
            rr_id = RbRequests(self.rb_username, self.rb_password,self.repository_name).create_rr(summary, description, target_people,
                                                                             self.temp_diff_file)
            print 'draft request review id :' + rr_id
            # create request review notes
            rr_dir = SVNRBTLogs().create_svn_rbt_notes(rr_id, summary, description, target_people, submitted_file_list)
            shutil.move(self.temp_diff_file, rr_dir + os.path.sep + 'diff_' + rr_id + '_latest.txt')
        finally:
            if os.path.isfile(self.temp_diff_file):
                os.remove(self.temp_diff_file)

    def do_help(self, arg):
        print self.intro

    def do_exit(self, arg):
        return -1

    ## function part
    def pre_precommit(self, changed_file_list, post_file_index=None):
        """
        处理新加的文件，同时生成所有的diff文件
        :param changed_file_list: 解析好的所有文件列表
        :param post_file_index:需要提交的文件序号，默认是None,表示提交所有文件
        :return:
        """
        file_tuple = self.get_selected_files(changed_file_list, post_file_index)
        # 添加新的文件到svn
        if len(file_tuple[0]) > 0:
            subprocess.call(self.svn_add + file_tuple[0], shell=True)
        self.generate_differ_file(file_tuple[1])
        return file_tuple[1]

    def generate_differ_file(self, changed_files):
        """
        生成的文件的differ文件
        :param changed_files:
        :return:
        """
        # svn diff <changed files> >> <file_name>
        if os.path.exists(self.temp_diff_file):
            os.remove(self.temp_diff_file)
        diff_command = self.svn_diff_command + changed_files + ' >>' + self.temp_diff_file
        # process diff file
        subprocess.call(diff_command, shell=True)

    def get_selected_files(self, changed_file_list, selected_file_index=None):
        """
        返回需要添加到SVN的列表和提交precommit review的文件列表
        :param changed_file_list: 所有改变的文件
        :param selected_file_index: 选中的文件
        :return:
        """

        file_list_to_add = ""
        post_file_name_list = ""
        if selected_file_index is None or len(selected_file_index) == 0:
            file_list_to_add = " ".join([item[1] for item in changed_file_list if (item[0] == "?")])
            post_file_name_list = " ".join(item[1] for item in changed_file_list)
        else:
            indexes = selected_file_index.split(",")
            file_list_to_add = " ".join(
                [changed_file_list[int(index)][1] for index in indexes if (changed_file_list[int(index)][0] == "?")])
            post_file_name_list = " ".join([changed_file_list[int(index)][1] for index in indexes])

        return (file_list_to_add, post_file_name_list)


    def parse_rb_config_file(self):
        """
        parse a .reviewboardrc file
        :return:
        """
        config = {
            'TREES': {},
            'ALIASES': {}
        }

        try:
            with open(self.rb_configuration) as f:
                exec (compile(f.read(), self.rb_configuration, 'exec'), config)
                return config
        except IOError:
            print "review board configuration is not correct,please configure it again:"
            self.do_setup(arg=None)
        finally:
            pass

    def get_changed_files(self):
        """
        返回SVN本地所有改变了的文件，返回格式为：
        ID | File SVN Status | File Name/File Path
        :return:
        """
        print "svn status:"
        return_content = subprocess.Popen(self.svn_status, shell=True, stdout=subprocess.PIPE)
        result = return_content.communicate()
        # list all the status
        changed_file = result[0].split("\n")
        parsed_changed_file = []
        print "Changed Files Status:"
        print "ID |FILE SVN Status|File Name/File Path "
        for i in range(len(changed_file)):
            changed_item = re.sub(' +', ",", changed_file[i]).split(",")
            if len(changed_item) > 1:
                print "%s | %s | %s" % (i, changed_item[0], changed_item[1])
                parsed_changed_file.append(changed_item)
        return parsed_changed_file

        # def do_note(self, args):
        # SVNRBTLogs().create_svn_rbt_notes(9, "test", "test", 95337, "123.txt,abcd.txt,abcd.txt,test.txt,new_files.txt")


class SVNRBTLogs():
    def __init__(self):
        pass

    BASE_PATH = 'differ_temp'
    DIFF_FILE = 'temp_differ.txt'
    NOTES_FILE = 'note.txt'

    @staticmethod
    def create_dir(dirPath):
        dirs = dirPath.split(os.path.sep)
        temp = ""
        for i in range(len(dirs)):
            temp = temp + dirs[i] + os.path.sep
            if not os.path.exists(temp):
                os.mkdir(temp)

    def create_svn_rr_folder(self, rr_id):
        """
        根据review request id 创建review request log 目录，此目录放置此次更新的review request 的描述，更新的文件列表
        以及不同的diff文件
        :param rr_id:
        :return:
        """
        rr_path = SVNRBTLogs.BASE_PATH + os.path.sep + str(rr_id)
        # create review request id folder
        self.create_dir(rr_path)
        return rr_path

    def move_differ_file(self, rr_id):
        """
        移动临时的diff 文件到temp 目录
        :param rr_id:
        :return:
        """
        rr_diff_path = self.create_svn_rr_folder(rr_id)
        shutil.move(SVNRBTLogs.BASE_PATH + os.path.sep + SVNRBTLogs.DIFF_FILE,
                    rr_diff_path)

    def create_svn_rbt_notes(self, review_request_id, summary, description, target_user, file_list):
        """
        创建request review的记录
        :param review_request_id:
        :param summary:
        :param description:
        :param target_user:
        :param file_list:
        :return:
        """
        rr_dir = self.create_svn_rr_folder(review_request_id)
        rr_note = rr_dir + os.path.sep + str(review_request_id) + '.txt'
        notes = {}
        if os.path.exists(rr_note):
            with open(rr_note, 'rw') as f:
                exec (compile(f.read(), rr_note, 'exec'), notes)
                try:
                    new_file_list = ','.join(
                        set(notes['changed_file_lists'].split(',') + file_list.split(',')))
                    self.write_to_note(rr_note, review_request_id, summary, description, new_file_list, target_user)

                except KeyError:
                    self.write_to_note(rr_note, review_request_id, summary, description, file_list, target_user)
        else:
            self.write_to_note(rr_note, review_request_id, summary, description, file_list, target_user)
        return rr_dir

    @staticmethod
    def write_to_note(rr_note, review_request_id, summary, description, file_lists, target_user):
        notes = {}
        with open(rr_note, 'w') as f:
            notes['review_request_id'] = review_request_id
            notes['summary'] = summary
            notes['description'] = description
            notes['changed_file_lists'] = file_lists
            notes['target_user'] = target_user
            for key in notes:
                f.write('%s="%s"\n' % (key, notes[key]))


class RbRequests():
    def __init__(self, username, password, repository_name):
        self.auth_codes = 'Basic ' + base64.b64encode(str(username) + ':' + password)
        self.repository_name = repository_name
        self.default_headers = {'Authorization': self.auth_codes,
                                'Content-type': 'application/json',
                                "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"
            , "Accept-Encoding": "gzip,deflate"
            , "Content-Type": "text/plaint-text; charset=utf-8"}

    def get_repository_id(self):
        repository_url = 'http://192.168.3.180/api/repositories/?start=0&max-results=200'
        r = requests.get(repository_url, headers=self.default_headers, data={'name': self.repository_name})
        for item in r.json()['repositories']:
            if item.get('name') == self.repository_name:
                self.repository_id = item['id']
                self.base_directory = item['path'] + '/' + self.repository_name
                return item['id']
        raise Exception(self.repository_name + " is not repository found")

    def create_draft_request_review(self):
        review_request_url = 'http://192.168.3.180/api/review-requests/'
        r = requests.post(review_request_url, headers=self.default_headers, data={'repository': self.repository_id})
        return r.json().get('review_request').get('id')

    def update_publish_draft_request_review(self, rr_id, summary, description, target_people):

        form = {'summary': summary,
                'description': description, 'target_people': target_people, 'public': 1}
        draft_url = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/draft/'
        try:
            r = requests.put(draft_url, headers=self.default_headers, data=form)
            print r
        except Exception:
            print "update draft failed"

    def upload_differ_file(self, rr_id, diff_file_name):

        svn_post_diff_command = 'rbt post -r %s --diff-filename %s' % (rr_id, diff_file_name)

        # upload_differ = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/draft/file-attachments/'
        # files = {'path': open(diff_file_name, 'rb'), 'basedir': self.base_directory}
        # data = {'basedir': self.base_directory}
        # r = requests.post(upload_differ, data=data, files=files, headers={'Authorization': self.auth_codes},
        # timeout=1.5)

        post_rest = subprocess.Popen(svn_post_diff_command, shell=True, stdout=subprocess.PIPE).communicate()
        print post_rest[0]


    def create_rr(self, summary, description, target_people, diff_file_name):
        self.get_repository_id()
        rr_id = self.create_draft_request_review()
        print self.upload_differ_file(rr_id, diff_file_name)
        self.update_publish_draft_request_review(rr_id, summary, description,
                                                 target_people)
        return rr_id


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    SvnRbClient().cmdloop()