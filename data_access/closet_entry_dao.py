from model.closet_entry_model import ClosetEntry
import database.db as db
import storage.aws_s3 as aws_s3
import base64
import io


class ClosetEntryDAO:
    def get_all_entries_from_closet(self, closet_id: int):
        try:
            entries = db.query_all_files_from_closet(closet_id)

            closet_entry_models = []

            for entry in entries:
                filename = entry['filename']
                description = entry['description']
                bucket_name = entry['bucket_name']
                object_key = entry['object_key']
                category = entry['category']
                base64_encoded_image = self.get_image_by_object_key(
                    bucket_name, object_key)

                closet_entry_model = ClosetEntry(
                    base64_encoded_image, filename, description, bucket_name, object_key, category)
                closet_entry_models.append(closet_entry_model)

            return closet_entry_models
        except Exception as error:
            raise error

    def get_image_by_object_key(self, bucket_name: str, object_key: str):
        img_data = aws_s3.get_image_data(bucket_name, object_key)
        return img_data

    def does_filename_exists_in_closet(self, closet_id: int, filename: str):
        try:
            files = db.query_file_key(closet_id, filename)

            if len(files) > 0:
                return True
            else:
                return False
        except Exception as error:
            raise error

    def create_closet_entry(self, closet_id: int, closet_entry_model: ClosetEntry):
        try:
            filename = closet_entry_model.filename
            description = closet_entry_model.description
            category = closet_entry_model.category

            # Pick bucket + generate key
            buckets = aws_s3.get_buckets()
            bucket_name = buckets[0]
            object_key = aws_s3.create_object_key(filename)

            db.add_file(object_key, filename, description, bucket_name, category, closet_id)
            self.upload_image(bucket_name, object_key,
                              closet_entry_model.base64_encoded_image)
        except Exception as error:
            raise error

    def upload_image(self, bucket_name: str, object_key: str, base64_encoded_image: str):
        try:
            aws_s3.upload_image(base64_encoded_image, bucket_name, object_key)
        except Exception as error:
            raise error

    def delete_closet_entry(self, closet_id: int, filename: str):
        try:
            files = db.query_file_key(closet_id, filename)
            if len(files) > 0:
                aws_s3.delete_object(files[0]['bucket_name'], files[0]['object_key'])
                db.delete_all_recommended_outfits_with_file(closet_id, filename)
                db.delete_file(files[0]['object_key'])
        except Exception as error:
            raise error


closet_entry_dao = ClosetEntryDAO()
