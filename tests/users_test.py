from core.models.users import User

def test_user_filter():
    """Test the filter method of the User class."""
    # Test filtering by username
    users = User.filter(User.username == "principal")
    assert len(users.all()) == 1

    # Test filtering by email
    users = User.filter(User.email == "principal@fylebe.com")
    assert len(users.all()) == 1

def test_user_get_by_id():
    """Test the get_by_id method of the User class."""
    user = User.get_by_id(1)
    assert user.username == "student1"
    assert user.email == "student1@fylebe.com"

def test_user_get_by_email():
    """Test the get_by_email method of the User class."""
    user = User.get_by_email("teacher2@fylebe.com")
    assert user.username == "teacher2"
    assert user.email == "teacher2@fylebe.com"
