import unittest

from main import calc_actual_withdrawal

class TestFantasyLeagueMath(unittest.TestCase):
    
    def test_valid_withdrawal(self):
        """Test Case 1: Rút 100 token phải trả về đúng 90.0 sau khi trừ 10% phí."""
        result = calc_actual_withdrawal(100.0)
        self.assertEqual(result, 90.0, "Tính toán sai phí giao dịch cho số lượng hợp lệ.")

    def test_negative_withdrawal(self):
        """Test Case 2: Hàm phải bắn ra lỗi ValueError nếu số rút là số âm."""
        with self.assertRaises(ValueError):
            calc_actual_withdrawal(-50.0)

if __name__ == '__main__':
    unittest.main()