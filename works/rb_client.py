# _*_ coding=utf-8 _*_
import cmd
import subprocess
import os
import re

__author__ = 'patrick'


def do_pre_change():
    print "upload new diff files,please provide your Review Request ID:"
    prompt = "<"
    rr_id = raw_input(prompt)


class RbClient(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        # read .reviewboardrc file as configuration
        self.rb_configuration = '.reviewboardrc'
        self.rb_url = '192.168.3.180'
        configurations = self.parse_rb_config_file()
        try:
            self.rb_audit_user = configurations['TARGET_PEOPLE']
        except KeyError:
            print "setup is not completed,need to run setup manually"
            pass

        self.svn_diff_command = 'svn diff '
        self.svn_status_xml = 'svn status --xml'
        self.svn_status = 'svn status '
        self.svn_add = 'svn add '
        self.temp_diff_file = 'differ_temp/temp_differ_file.txt'
        self.rb_post = "rbt post --diff-filename %s --target-people %s --summary %s --description %s "
        self.rb_post_w_rrId = "rbt post -r %s"
        self.rb_publish = "rbt publish -r %s"

    intro = '''
        Review Board Client, ? for help, and the total command lists:
        1. setup:setup review board setting
        2. pre:precommit your changes
        3. u_pre:update date your precommit
        4. ss:svn status,find svn status for the working copies
        5. s_add:svn add,add files to local svn
        6. s_d:svn delete,delete svn file
        7. s_ci:svn commit,commit the changes by review request id
        8. re: revert changes
    '''

    prompt = '( RB Client)'

    def do_help(self, arg):
        print self.intro

    def do_setup(self, arg):
        print "setup reviewboard configuration:"
        prompt = "<"
        print "please input your Review Board ID/ Employee ID:"
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

    def do_pre(self, arg):
        # svn status --xml to get xml file
        # pass selected file to generate diff files
        # prompt summary and description for issues
        # rbt post --summary %s --description %s --open_browser True --diff-filename=
        # rbt publish => get status
        # rbt get request id
        # handle files
        print "pre-commit the changes"
        return_content = subprocess.Popen(self.svn_status, shell=True, stdout=subprocess.PIPE)
        result = return_content.communicate()
        # list all the status
        changed_file = result[0].split("\n")
        parsed_changed_file = []
        print "changed files status:"
        print "ID | File SVN Status | File Name/File Path "
        for i in range(len(changed_file)):
            changed_item = re.sub(' +', ",", changed_file[i]).split(",")
            if len(changed_item) > 1:
                print "%s | %s | %s" % (i, changed_item[0], changed_item[1])
                parsed_changed_file.append(changed_item)

        print "Please select the files IDs which your want to commit，eg.0,1,2,3, or Enter for All Files"
        prompt = "<"
        post_file_index = raw_input(prompt)
        if len(post_file_index) == 0:
            print "Files you selected:"
            submitted_file_list = self.pre_precommit(parsed_changed_file)
        else:
            print "Your selected File List:" + post_file_index
            submitted_file_list = self.pre_precommit(parsed_changed_file, post_file_index)

        print submitted_file_list
        # process rbt post to submit review request
        prompt = "Please input your reviewer ID,Entry for default Reviewer> "
        target_people = raw_input(prompt)
        if len(target_people) == 0:
            target_people = self.rb_audit_user

        prompt = "Please input summary for your changes,it is nice to provide your Bug No:>"
        summary = raw_input(prompt)
        prompt = "Please input detail description for your changes, Enter for use Summary as your detail description:"
        description = raw_input(prompt)
        if len(description) == 0:
            description = summary

        post_command = self.rb_post % (self.temp_diff_file, target_people, summary, description)
        print post_command
        try:
            post_rest = subprocess.Popen(post_command, shell=True, stdout=subprocess.PIPE).communicate()
            print post_rest
            rr_id = re.findall(r'[#](\d+)', post_rest)
            # mkdir for this request ,and move the differ file to it and also write the summary
            try:
                os.mkdir("differ_temp/" + rr_id)
                # add file to temp file
                # write summary and files
                # file structure: 1. description.txt, differ files
                # execfile
            except OSError:
                pass
        finally:
            if os.path.isfile(self.temp_diff_file):
                os.remove(self.temp_diff_file)

    def do_u_pre(self, arg):
        print "update pre-commit"

    def do_ss(self, arg):
        self.get_changed_files()

    def do_s_add(self, arg):
        print "Add files to SVN"
        self.do_ss(arg=None)
        print "Please select the files IDs which your want to commit，eg.0,1,2,3, or Enter for All Files"
        prompt = "<"
        selected_file_index = raw_input(prompt)
        file_list = self.get_selected_files(self.get_changed_files(), selected_file_index)
        print "adding files for:" + file_list[0]
        if len(file_list[0]) > 0:
            subprocess.call(self.svn_add + file_list[0], shell=True)

    def do_revert(self, args):
        print "revert changes"
        self.do_ss(arg=None)
        print "Please select the files IDs which your want to commit，eg.0,1,2,3, or Enter for All Files"
        prompt = "<"
        selected_file_index = raw_input(prompt)
        files_lists = self.get_selected_files(self.get_changed_files(), selected_file_index)[1]
        subprocess.call("svn revert %s --depth infinity" % files_lists, shell=True)

    def do_s_d(self, arg):
        print "svn delete"

    def do_ci(self, arg):
        print "svn commit files"

    def do_exit(self, arg):
        return -1


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

    def get_changed_files(self):
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

    def generate_differ_file(self, changed_files):
        # svn diff <changed files> >> <file_name>
        diff_command = self.svn_diff_command + changed_files + ' >>' + self.temp_diff_file
        # process diff file
        subprocess.call(diff_command, shell=True)


if __name__ == '__main__':
    RbClient().cmdloop()