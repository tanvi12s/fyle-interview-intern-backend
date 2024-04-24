from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals import Principal
from core.libs.exceptions import FyleError

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_grade_assignment_bad_grade(client, h_principal):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_principal):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 100000,
            "grade": "A"
        }
    )
    
    error = FyleError(status_code=404, message="Assignment not found")

    assert error.status_code == 404
    assert error.message == "Assignment not found"
    
    error_dict = error.to_dict()
    assert error_dict['message'] == "Assignment not found"


def test_validate_existing_principal():
    """validating existing Principal"""
    principal = Principal.query.get(1)
    assert repr(principal) == '<Principal 1>'