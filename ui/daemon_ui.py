import sys

class DaemonOutputUI(object):
    def show_error(self, msg, title="Error"):
        if isinstance(msg, Exception):
            title = msg.__class__.__name__
            msg = str(msg)
        sys.stderr.write("%s\n%s" % (title, msg))

    def show_message(self, msg, title="Information"):
        pass

    def show_warning(self, msg, title="Warning"):
        pass

    def show_text(self, text):
        pass

class DaemonInputUI(object):
    def get_confirmation(self, title, msg):
        raise NotImplementedError

    def get_string(self, title, msg):
        raise NotImplementedError

    def get_open_filename(self, title="Open", filetype_filter="*.*", file_dir=None, selected_filter=None):
        raise NotImplementedError
    def get_save_filename(self, title, filetype_filter, file_dir=None, selected_filter=None):
        raise NotImplementedError


    def get_open_filenames(self, title, filetype_filter, file_dir=None):
        raise NotImplementedError

    def get_foldername(self, title='Select directory', file_dir=None):
        raise NotImplementedError

class DaemonStatusUI(object):

    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
        return sequence

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):
        return task(*args, **kwargs)

    def start_wait(self):
        pass

    def end_wait(self):
        pass

class DaemonUI(DaemonOutputUI, DaemonInputUI, DaemonStatusUI):
    pass
