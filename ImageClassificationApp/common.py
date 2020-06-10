import os

def build_upload_to_path_for_images(instance, filename):
    return f"data/classification/{instance.imageclass.task.customer.username}/{instance.imageclass.task.task_name}/{instance.imageclass.image_classname}/{filename}"


