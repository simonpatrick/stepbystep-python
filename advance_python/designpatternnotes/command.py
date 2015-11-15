# _*_ coding=utf-8 _*_
__author__ = 'patrick'


class MoveFileCommand(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def rename(self):
        print "rename {0} to {1}".format(self.src, self.dest)

    # todo how to invoke method dynamically
    def execute(self, method_name):
        # if method_name == "rename":
        # self.rename()
        # else:
        #     self.undo()
        getattr(self, method_name)()

    def undo(self):
        print "under rename {0} to {1}".format(self.src, self.dest)


if __name__ == '__main__':
    command_stack = [MoveFileCommand("1", "2"), MoveFileCommand("2", "3")]
    for command in command_stack:
        command.execute("rename")
        command.execute("undo")

    for cmd in reversed(command_stack):
        cmd.execute("undo")