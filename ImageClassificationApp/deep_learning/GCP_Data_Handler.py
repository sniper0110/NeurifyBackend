from google.cloud import storage
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bucket_name", type=str, help="bucket name from GCP buckets", default="neurify-bucket")
parser.add_argument("--local_directory", type=str, help="local directory where downloaded data will be saved",
                    default="/media/nourislam/Data/SaaS/Neurify/Backend/NeurifySite/ImageClassificationApp/deep_learning/downloaded_data")

args = parser.parse_args()

path_to_credentials = 'neurfiy-9544c225013a.json'
#bucket_name = 'online-deeplearning-bucket'

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""

    storage_client = storage.Client.from_service_account_json(path_to_credentials)

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    return blobs


def directories_within_this_directory(bucket_name, this_directory, all_blobs):

    storage_client = storage.Client.from_service_account_json(path_to_credentials)
    this_directory_blob = storage_client.get_bucket(bucket_name).get_blob(this_directory)
    directories_inside = []
    for blob in all_blobs:
        if blob.name.endswith('/') and\
                this_directory_blob.name in blob.name and \
                blob.name != this_directory_blob.name:

            directories_inside.append(blob.name)


    return directories_inside



def download_data_to_local_directory(local_directory, bucket_name):

    storage_client = storage.Client.from_service_account_json(path_to_credentials)
    # TODO: check whether bucket exists or not
    all_blobs = storage_client.list_blobs(bucket_name)


    if not os.path.isdir(local_directory):
        os.makedirs(local_directory)

    for blob in all_blobs:
        print(blob.name)

        joined_path = os.path.join(local_directory, blob.name)
        print(joined_path)

        print('basename : ', os.path.basename(joined_path))

        if os.path.basename(joined_path) == '':
            if not os.path.isdir(joined_path):
                os.makedirs(joined_path)

        else:
            # TODO : validate that the file is an image
            if not os.path.isfile(joined_path):
                if not os.path.isdir(os.path.dirname(joined_path)):
                    os.makedirs(os.path.dirname(joined_path))
                blob.download_to_filename(joined_path)


if __name__ == "__main__":

    download_data_to_local_directory(args.local_directory, args.bucket_name)
    print(f"Finished downloading data to local directory : {args.local_directory}")

