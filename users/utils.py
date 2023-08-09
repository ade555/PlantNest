from django.core.exceptions import ValidationError

# a simple form to check the image size uploaded by the user
def validate_image_size(image):
    max_upload_size = 2 * 1024 * 1024  # 2MB

    # prevent users from uploading images larger than 2mb
    if image.size > max_upload_size:
        raise ValidationError("The uploaded image size is too large. Please upload an image smaller than 2MB.")