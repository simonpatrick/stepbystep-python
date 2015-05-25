# _*_ coding=utf-8 _*_
import os
import shutil

__author__ = 'patrick'


class SVNLogs():

    BASE_PATH='differ_temp'
    DIFF_FILE='temp_differ.txt'
    NOTES_FILE='note.txt'

    def create_dir(self, dirPath):
        dirs = dirPath.split(os.path.sep)
        temp = ""
        for i in range(len(dirs)):
            temp = temp + dirs[i] + os.path.sep
            if not os.path.exists(temp):
                os.mkdir(temp)

    def create_svn_rr_folder(self,rr_id):
        rr_path = SVNLogs.BASE_PATH+os.path.sep+rr_id
        # create review request id folder
        self.create_dir(rr_path)
        return rr_path

    def move_differ_file(self,rr_id):
        rr_diff_path=self.create_svn_rr_folder(rr_id)
        shutil.move(SVNLogs.BASE_PATH+os.path.sep+SVNLogs.DIFF_FILE,
                    rr_diff_path)

    def create_request_note(self,rr_id,summary,target_user
                            ,file_lists,description=None):

        notes={}
        notes.add('rr_id',rr_id)
        notes.add('summary',summary)
        notes.add('target_user',target_user)
        notes.add('file_lists',file_lists)
        notes.add('description',description)
        rr_location = self.create_svn_rr_folder(rr_id)

    # def create_note_file(self,rr_location):
    #     notes_path = rr_location+os.path.sep+SVNLogs.NOTES_FILE
    #     if not os.path.exists(notes_path):
    #         os.

if __name__ == '__main__':
    SVNLogs().create_dir(SVNLogs.BASE_PATH+os.path.sep+'8')
