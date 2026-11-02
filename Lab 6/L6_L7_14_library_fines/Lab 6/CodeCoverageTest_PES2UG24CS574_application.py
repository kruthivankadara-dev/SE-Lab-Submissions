
import pytest
from library_fines import late_fine, can_borrow, renewal_status
# -------------------------------------------------
# 1. TEST CASES FOR late_fine()
# -------------------------------------------------
def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 20, False)
def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)
def test_student_on_time():
    assert late_fine("student", 14, False) == 0
def test_student_overdue():
    assert late_fine("student", 15, False) == 2
def test_faculty_overdue():
    assert late_fine("faculty", 31, False) == 1
def test_guest_overdue():
    assert late_fine("guest", 15, False) == 5
def test_fine_capped_at_200():
    assert late_fine("student", 200, False) == 200
def test_damaged_book_without_overdue():
    assert late_fine("student", 10, True) == 150
def test_damaged_book_with_overdue():
    assert late_fine("student", 15, True) == 152
def test_damaged_book_with_capped_fine():
    assert late_fine("student", 200, True) == 350
# -------------------------------------------------
# 2. TEST CASES FOR can_borrow()
# -------------------------------------------------
def test_pending_fine_above_100():
    assert can_borrow(0, 101, "student") is False
def test_pending_fine_exactly_100():
    assert can_borrow(0, 100, "student") is True
def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True
def test_faculty_reached_book_limit():
    assert can_borrow(10, 0, "faculty") is False
def test_student_can_borrow():
    assert can_borrow(2, 0, "student") is True
def test_student_reached_book_limit():
    assert can_borrow(3, 0, "student") is False
# -------------------------------------------------
# 3. TEST CASES FOR renewal_status()
# -------------------------------------------------
def test_renewal_denied_due_to_reservation():
    assert renewal_status(0, True, 5) == "denied"
def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"
def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"
def test_renewal_successful():
    assert renewal_status(0, False, 5) == "renewed"
def test_reservation_takes_priority():
    assert renewal_status(2, True, -1) == "denied"
