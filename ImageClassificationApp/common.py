import os

def build_upload_to_path_for_images(instance, filename):
    return f"data/classification/user_uploaded_images/{instance.imageclass.task.customer.username}/{instance.imageclass.task.task_name}/{instance.imageclass.image_classname}/{filename}"


def path_for_model_artifacts_zip_upload(instance, filename):
    return f"data/classification/models_artifacts/models/{instance.task.customer.username}/{instance.task.task_name}/{filename}"


def path_for_training_history_npy_upload(instance, filename):
    return f"data/classification/models_artifacts/history/{instance.task.customer.username}/{instance.task.task_name}/{filename}"
