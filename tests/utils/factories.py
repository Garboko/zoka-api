from app.schemas.users import UserCreate
from app.schemas.projects import ProjectCreate
from app.schemas.forms import FormCreate

def create_user_data():
    return UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="testpassword123"
    )

def create_project_data(user_id: str):
    return ProjectCreate(
        name="Test Project",
        description="Test Description",
        user_id=user_id
    )

def create_form_data(user_id: str, project_id: str = None):
    return FormCreate(
        title="Test Form",
        description="Test Form Description",
        user_id=user_id,
        project_id=project_id,
        public_access=False
    )