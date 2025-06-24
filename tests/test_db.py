from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

    # assert asdict(user) == {
    #     'id': 1,
    #     'username': 'test',
    #     'email': 'test@test',
    #     'password': 'secret',
    #     'created _at': time,
    # }
    user_dict = asdict(user)

    assert user_dict['id'] == 1
    assert user_dict['username'] == 'test'
    assert user_dict['email'] == 'test@test'
    assert user_dict['password'] == 'secret'
    assert user_dict['created_at'].isoformat() == time.isoformat()
