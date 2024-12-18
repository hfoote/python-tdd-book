import pytest

@pytest.mark.django_db
def test_bad_maths():
	assert 1 + 1 == 3