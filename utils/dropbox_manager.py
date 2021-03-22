import dropbox


class DropboxManager:
    def __init__(self, access_token):
        self.access_token = access_token
        self.dbx = dropbox.Dropbox(self.access_token)

    def upload_file(self, file_from, file_to):
        if type(file_from) == str:
            with open(file_from, 'rb') as f:
                contents = f.read()
                try:
                    self.dbx.files_upload(contents, file_to)
                # If file already exists, overwrite it.
                except Exception:
                    self.dbx.files_upload(
                        contents, file_to, mode=dropbox.files.WriteMode.overwrite)
        # For tempfiles
        else:
            file_from.seek(0)
            contents = file_from.read()
            try:
                self.dbx.files_upload(contents, file_to)
            # If file already exists, overwrite it.
            except Exception:
                self.dbx.files_upload(
                    contents, file_to, mode=dropbox.files.WriteMode.overwrite)
        url = self.dbx.sharing_create_shared_link(
            file_to).url.split('?')[0] + '?raw=1'
        return url

    def download_file(self, file_path, file_to):
        with open(file_to, 'wb') as f:
            metadata, res = self.dbx.files_download(file_path)
            f.write(res.content)
