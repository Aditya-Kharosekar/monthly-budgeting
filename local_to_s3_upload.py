import config
from pathlib import Path
import os
from utils.s3_utils import connect_to_s3, upload_file_to_s3


def collect_files_to_upload():
    """Gets the files that need to be uploaded to S3. The files will be placed and renamed manually by me.

    Returns a dict of type Str:List where the key is the name of a financial institution,
    and the value is a list of file names that need to be uploaded.
    """
    financial_institutions = [x[1] for x in os.walk(config.SOURCE_LOCAL_DIRECTORY)][0]
    files_dict = {}
    for fi in financial_institutions:
        files_dict[fi] = [
            x[2] for x in os.walk(str(Path(config.SOURCE_LOCAL_DIRECTORY) / fi))
        ][0]

    return files_dict


def upload_files(client, files_dict):
    """Handles uploading of all files that were found in the local directory. Adds a prefix of `input`

    Args:
        client (s3.Client): the boto3 client already authenticated and connected to S3
        files_dict (Dict[Str, List]): the output of `collect_files_to_upload`
    """
    for institution in files_dict.keys():
        files = files_dict[institution]
        for f in files:
            file_name = str(Path(config.SOURCE_LOCAL_DIRECTORY) / institution / f)
            object_name = str("inputs" / Path(institution) / f)
            response = upload_file_to_s3(
                client=client,
                file_name=file_name,
                object_name=object_name,
            )
            if response:
                print(f"Successfully uploaded {file_name}")
            else:
                print(f"An error occurred when trying to upload {file_name}")


def main():
    files_dict = collect_files_to_upload()
    s3_client = connect_to_s3()
    upload_files(s3_client, files_dict)


if __name__ == "__main__":
    main()
