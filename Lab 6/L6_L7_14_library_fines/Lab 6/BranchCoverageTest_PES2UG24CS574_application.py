
import pytest
from library_fines import late_fine, can_borrow, renewal_status
# -------------------------------------------------
# 1. BRANCH TESTS FOR late_fine()
# -------------------------------------------------
def test_member_valid_and_invalid():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 10, False)

    assert late_fine("student", 10, False) == 0
def test_days_valid_and_invalid():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

    assert late_fine("student", 14, False) == 0
def test_faculty_and_non_faculty_loan_periods():
    assert late_fine("faculty", 30, False) == 0
    assert late_fine("faculty", 31, False) == 1
    assert late_fine("student", 14, False) == 0
    assert late_fine("guest", 15, False) == 5
def test_overdue_branch_and_fine_cap():
    assert late_fine("student", 14, False) == 0
    assert late_fine("student", 15, False) == 2
    assert late_fine("student", 200, False) == 200
def test_fine_cap_boundary():
    # 100 overdue days * Rs. 2 = Rs. 200
    assert late_fine("student", 114, False) == 200

    # 101 overdue days * Rs. 2 exceeds Rs. 200
    assert late_fine("student", 115, False) == 200
def test_damaged_and_undamaged_books():
    assert late_fine("student", 10, False) == 0
    assert late_fine("student", 10, True) == 150
    assert late_fine("student", 15, True) == 152
# -------------------------------------------------
# 2. BRANCH TESTS FOR can_borrow()
# -------------------------------------------------
def test_pending_fine_branch():
    assert can_borrow(0, 101, "student") is False
    assert can_borrow(0, 100, "student") is True
def test_faculty_borrowing_branches():
    assert can_borrow(9, 0, "faculty") is True
    assert can_borrow(10, 0, "faculty") is False
def test_non_faculty_borrowing_branches():
    assert can_borrow(2, 0, "student") is True
    assert can_borrow(3, 0, "student") is False
# -------------------------------------------------
# 3. BRANCH TESTS FOR renewal_status()
# -------------------------------------------------
def test_reservation_branch():
    assert renewal_status(0, True, 5) == "denied"
    assert renewal_status(0, False, 5) == "renewed"
def test_renewal_limit_branch():
    assert renewal_status(2, False, 5) == "limit reached"
    assert renewal_status(1, False, 5) == "renewed"
def test_overdue_branch():
    assert renewal_status(1, False, -1) == "overdue"
    assert renewal_status(1, False, 0) == "renewed"
def test_renewal_condition_priority():
    assert renewal_status(2, True, -1) == "denied"
