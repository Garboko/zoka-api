import pytest
from sqlalchemy.orm import Session

from app.crud import devices as crud_devices
from app.schemas.devices import DeviceCreate, DeviceUpdate
from app.models.devices import Device


class TestDevicesCRUD:
    
    def test_get_device_by_id(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="device123",
            model="Samsung Galaxy",
            platform="Android",
            app_version="1.0.0"
        )
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        found_device = crud_devices.get(db_session, id=created_device.id)
        
        assert found_device is not None
        assert found_device.id == created_device.id
        assert found_device.enumerator_id == "enum123"
        assert found_device.device_uuid == "device123"

    def test_get_device_by_id_not_found(self, db_session: Session):
        found_device = crud_devices.get(db_session, id="non_existent_id")
        
        assert found_device is None

    def test_get_devices_by_enumerator(self, db_session: Session):
        enumerator_id = "enum123"
        device_data_1 = DeviceCreate(
            enumerator_id=enumerator_id,
            device_uuid="device1",
            model="Phone A",
            platform="Android"
        )
        device_data_2 = DeviceCreate(
            enumerator_id=enumerator_id,
            device_uuid="device2", 
            model="Phone B",
            platform="iOS"
        )
        crud_devices.create(db_session, obj_in=device_data_1)
        crud_devices.create(db_session, obj_in=device_data_2)
        
        enumerator_devices = crud_devices.get_by_enumerator(db_session, enumerator_id=enumerator_id)
        
        assert len(enumerator_devices) == 2
        assert all(device.enumerator_id == enumerator_id for device in enumerator_devices)

    def test_get_device_by_device_uuid(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="unique_device_123",
            model="Test Device",
            platform="Android"
        )
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        found_device = crud_devices.get_by_device_uuid(
            db_session, enumerator_id="enum123", device_uuid="unique_device_123"
        )
        
        assert found_device is not None
        assert found_device.id == created_device.id
        assert found_device.device_uuid == "unique_device_123"

    def test_get_device_by_device_uuid_not_found(self, db_session: Session):
        found_device = crud_devices.get_by_device_uuid(
            db_session, enumerator_id="enum123", device_uuid="non_existent_uuid"
        )
        
        assert found_device is None

    def test_create_device(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="new_device_123",
            model="New Phone",
            platform="iOS",
            app_version="2.0.0"
        )
        
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        assert created_device is not None
        assert created_device.id is not None
        assert created_device.enumerator_id == "enum123"
        assert created_device.device_uuid == "new_device_123"
        assert created_device.model == "New Phone"
        assert created_device.platform == "iOS"
        assert created_device.app_version == "2.0.0"
        assert created_device.is_active is True

    def test_create_device_minimal_data(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="minimal_device"
        )
        
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        assert created_device.device_uuid == "minimal_device"
        assert created_device.enumerator_id == "enum123"
        assert created_device.model is None
        assert created_device.platform is None

    def test_update_device(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="device123",
            model="Old Model",
            platform="Old Platform"
        )
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        update_data = DeviceUpdate(
            model="New Model",
            platform="New Platform",
            app_version="3.0.0",
            is_active=False
        )
        
        updated_device = crud_devices.update(db_session, db_obj=created_device, obj_in=update_data)
        
        assert updated_device.model == "New Model"
        assert updated_device.platform == "New Platform"
        assert updated_device.app_version == "3.0.0"
        assert updated_device.is_active is False
        assert updated_device.enumerator_id == "enum123"
        assert updated_device.device_uuid == "device123"

    def test_update_device_partial(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="device123",
            model="Original Model",
            platform="Android"
        )
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        update_data = DeviceUpdate(app_version="1.5.0")
        
        updated_device = crud_devices.update(db_session, db_obj=created_device, obj_in=update_data)
        
        assert updated_device.app_version == "1.5.0"
        assert updated_device.model == "Original Model"
        assert updated_device.platform == "Android"
        assert updated_device.is_active is True

    def test_delete_device(self, db_session: Session):
        device_data = DeviceCreate(
            enumerator_id="enum123",
            device_uuid="device_to_delete",
            model="Test Device"
        )
        created_device = crud_devices.create(db_session, obj_in=device_data)
        
        deleted_device = crud_devices.delete(db_session, id=created_device.id)
        
        assert deleted_device is not None
        assert deleted_device.id == created_device.id
        
        found_device = crud_devices.get(db_session, id=created_device.id)
        assert found_device is None

    def test_delete_device_not_found(self, db_session: Session):
        result = crud_devices.delete(db_session, id="non_existent_id")
        
        assert result is None

    def test_get_multi_devices(self, db_session: Session):
        devices_data = [
            DeviceCreate(enumerator_id=f"enum{i}", device_uuid=f"device{i}", model=f"Model {i}")
            for i in range(5)
        ]
        
        for device_data in devices_data:
            crud_devices.create(db_session, obj_in=device_data)
        
        devices = crud_devices.get_multi(db_session, skip=0, limit=10)
        
        assert len(devices) == 5
        assert all(isinstance(device, Device) for device in devices)

    def test_get_multi_devices_with_pagination(self, db_session: Session):
        devices_data = [
            DeviceCreate(enumerator_id=f"enum{i}", device_uuid=f"device{i}", model=f"Model {i}")
            for i in range(10)
        ]
        
        for device_data in devices_data:
            crud_devices.create(db_session, obj_in=device_data)
        
        first_page = crud_devices.get_multi(db_session, skip=0, limit=4)
        second_page = crud_devices.get_multi(db_session, skip=4, limit=4)
        
        assert len(first_page) == 4
        assert len(second_page) == 4
        
        first_ids = {device.id for device in first_page}
        second_ids = {device.id for device in second_page}
        assert first_ids.isdisjoint(second_ids)