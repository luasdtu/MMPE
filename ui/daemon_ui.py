
class DaemonOutputUI(object):
    def show_error(self, msg, title="Error"):
        pass

    def show_message(self, msg, title="Information"):
        pass

    def show_warning(self, msg, title="Warning"):
        pass

    def show_text(self, text):
        pass


class DaemonStatusUI(object):

    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
        return sequence

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):
        return task(*args, **kwargs)

    def start_wait(self):
        pass

    def end_wait(self):
        pass

class DaemonUI(DaemonOutputUI, DaemonStatusUI):
    pass
