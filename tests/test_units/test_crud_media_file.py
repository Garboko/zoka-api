import pytest
from sqlalchemy.orm import Session

from app.crud import media_files as crud_media_files
from app.schemas.media_files import MediaFileCreate, MediaFileUpdate
from app.models.media_files import MediaFile


class TestMediaFilesCRUD:
    
    def test_get_media_file_by_id(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/media/sub123/file1.jpg",
            file_type="image/jpeg"
        )
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        found_media = crud_media_files.get(db_session, id=created_media.id)
        
        assert found_media is not None
        assert found_media.id == created_media.id
        assert found_media.submission_id == "sub123"
        assert found_media.file_path == "/media/sub123/file1.jpg"

    def test_get_media_file_by_id_not_found(self, db_session: Session):
        found_media = crud_media_files.get(db_session, id="non_existent_id")
        
        assert found_media is None

    def test_get_media_files_by_submission(self, db_session: Session):
        submission_id = "sub123"
        media_file_data_1 = MediaFileCreate(
            submission_id=submission_id,
            file_path="/media/sub123/file1.jpg",
            file_type="image/jpeg"
        )
        media_file_data_2 = MediaFileCreate(
            submission_id=submission_id,
            file_path="/media/sub123/file2.png",
            file_type="image/png"
        )
        crud_media_files.create(db_session, obj_in=media_file_data_1)
        crud_media_files.create(db_session, obj_in=media_file_data_2)
        
        submission_media = crud_media_files.get_by_submission(db_session, submission_id=submission_id)
        
        assert len(submission_media) == 2
        assert all(media.submission_id == submission_id for media in submission_media)

    def test_create_media_file(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/media/sub123/photo.jpg",
            file_type="image/jpeg"
        )
        
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        assert created_media is not None
        assert created_media.id is not None
        assert created_media.submission_id == "sub123"
        assert created_media.file_path == "/media/sub123/photo.jpg"
        assert created_media.file_type == "image/jpeg"

    def test_create_media_file_without_file_type(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/media/sub123/file.bin"
        )
        
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        assert created_media.file_type is None
        assert created_media.file_path == "/media/sub123/file.bin"

    def test_update_media_file(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/old/path/file.jpg",
            file_type="image/jpeg"
        )
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        update_data = MediaFileUpdate(
            file_path="/new/path/file.jpg",
            file_type="image/png"
        )
        
        updated_media = crud_media_files.update(db_session, db_obj=created_media, obj_in=update_data)
        
        assert updated_media.file_path == "/new/path/file.jpg"
        assert updated_media.file_type == "image/png"
        assert updated_media.submission_id == "sub123"

    def test_update_media_file_partial(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/path/file.jpg",
            file_type="image/jpeg"
        )
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        update_data = MediaFileUpdate(file_type="image/png")
        
        updated_media = crud_media_files.update(db_session, db_obj=created_media, obj_in=update_data)
        
        assert updated_media.file_type == "image/png"
        assert updated_media.file_path == "/path/file.jpg"
        assert updated_media.submission_id == "sub123"

    def test_delete_media_file(self, db_session: Session):
        media_file_data = MediaFileCreate(
            submission_id="sub123",
            file_path="/media/sub123/delete.jpg",
            file_type="image/jpeg"
        )
        created_media = crud_media_files.create(db_session, obj_in=media_file_data)
        
        deleted_media = crud_media_files.delete(db_session, id=created_media.id)
        
        assert deleted_media is not None
        assert deleted_media.id == created_media.id
        
        found_media = crud_media_files.get(db_session, id=created_media.id)
        assert found_media is None

    def test_delete_media_file_not_found(self, db_session: Session):
        result = crud_media_files.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_media_files(self, db_session: Session):
        media_files_data = [
            MediaFileCreate(submission_id=f"sub{i}", file_path=f"/media/sub{i}/file{i}.jpg")
            for i in range(5)
        ]
        
        for media_file_data in media_files_data:
            crud_media_files.create(db_session, obj_in=media_file_data)
        
        media_files = crud_media_files.get_multi(db_session, skip=0, limit=10)
        
        assert len(media_files) == 5
        assert all(isinstance(media, MediaFile) for media in media_files)

    def test_get_multi_media_files_with_pagination(self, db_session: Session):
        media_files_data = [
            MediaFileCreate(submission_id=f"sub{i}", file_path=f"/media/sub{i}/file{i}.jpg")
            for i in range(10)
        ]
        
        for media_file_data in media_files_data:
            crud_media_files.create(db_session, obj_in=media_file_data)
        
        first_page = crud_media_files.get_multi(db_session, skip=0, limit=4)
        second_page = crud_media_files.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {media.id for media in first_page}
        second_ids = {media.id for media in second_page}
        assert first_ids.isdisjoint(second_ids)