"""
- Dùng snake_case, Type Hinting, tách hàm phụ trợ (find_player_by_id, calc_actual_withdrawal).
- File 'fantasy_league.log' | Format: %(asctime)s - %(levelname)s - %(message)s.
- Dùng try...except ValueError trong vòng lặp while để ép nhập số. Dùng dict.get() tránh KeyError.
"""

import logging

logging.basicConfig(
    filename='fantasy_league.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_player_by_id(players: list, player_id: str) -> int:
    target_id = player_id.strip().upper()
    for index, player in enumerate(players):
        if player.get("player_id", "").upper() == target_id:
            return index
    return -1

def calc_actual_withdrawal(withdraw_amount: float) -> float:
    if withdraw_amount < 0:
        raise ValueError("Số lượng rút không được là số âm.")
    return withdraw_amount * 0.9

def display_market(players: list) -> None:
    if not players:
        print("\nSàn giao dịch hiện chưa có tuyển thủ nào.")
        return

    print("\n--- SÀN GIAO DỊCH TUYỂN THỦ ---")
    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Giá trị thị trường':<18} | {'Fan Token':<10} | {'Điểm trận':<10} | {'Hệ số':<6} | Trạng thái đầu tư")
    print("-" * 105)

    for player in players:
        p_id = player.get("player_id", "Unknown")
        name = player.get("name", "Unknown")
        market_value = player.get("market_value", 0)
        fan_tokens = player.get("fan_tokens", 0)
        match_points = player.get("match_points", 0)
        form_multiplier = player.get("form_multiplier", 1.0)

        if fan_tokens == 0:
            status = "Chưa có người đầu tư"
        elif 0 < fan_tokens <= 1000:
            status = "Đang thu hút"
        else:
            status = "Tuyển thủ Hot"

        print(f"{p_id:<8} | {name:<15} | {market_value:<18,.0f} | {fan_tokens:<10,.0f} | {match_points:<10,.0f} | {form_multiplier:<6.1f} | {status}")
    
    logging.info("User viewed the player market.")

def invest_tokens(players: list) -> None:
    print("\n--- ĐẦU TƯ FAN TOKEN ---")
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    index = find_player_by_id(players, player_id)
    if index == -1:
        print("\nKhông tìm thấy tuyển thủ!")
        logging.warning(f"Invest failed - Player {player_id} not found")
        return

    while True:
        try:
            invest_amount = int(input("Nhập số token muốn đầu tư: ").strip())
            if invest_amount <= 0:
                print("\nSố token phải là số nguyên dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("\nSố token phải là số nguyên dương. Vui lòng nhập lại.")
            logging.warning("Invalid token input while investing")

    players[index]["fan_tokens"] = players[index].get("fan_tokens", 0) + invest_amount
    player_name = players[index].get("name", "Unknown")
    
    print(f"\nThành công: Đã đầu tư {invest_amount:,} token vào tuyển thủ {players[index]['player_id']}.")
    print(f"Số Fan Token hiện tại của {player_name}: {players[index]['fan_tokens']:,}")
    logging.info(f"Invested {invest_amount} tokens into {players[index]['player_id']}")

def withdraw_tokens(players: list) -> None:
    print("\n--- RÚT VỐN FAN TOKEN ---")
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    index = find_player_by_id(players, player_id)
    if index == -1:
        print("\nKhông tìm thấy tuyển thủ!")
        logging.warning(f"Withdraw failed - Player {player_id} not found")
        return

    current_tokens = players[index].get("fan_tokens", 0)
    player_name = players[index].get("name", "Unknown")

    while True:
        try:
            withdraw_amount = int(input("Nhập số token muốn rút: ").strip())
            if withdraw_amount <= 0:
                print("\nSố token phải là số nguyên dương. Vui lòng nhập lại.")
                continue
            
            if withdraw_amount > current_tokens:
                print("\nKhông thể rút. Số token muốn rút vượt quá số Fan Token hiện có.")
                print(f"Fan Token hiện có của {player_name}: {current_tokens:,}")
                logging.warning("Withdraw failed - Amount exceeds current fan tokens")
                return
            break
        except ValueError:
            print("\nSố token phải là số nguyên dương. Vui lòng nhập lại.")

    try:
        actual_received = calc_actual_withdrawal(withdraw_amount)
        fee = withdraw_amount - actual_received
    except ValueError as e:
        print(f"\nLỗi hệ thống: {e}")
        return

    players[index]["fan_tokens"] -= withdraw_amount

    print(f"\nThành công: Đã rút {withdraw_amount:,} token khỏi tuyển thủ {players[index]['player_id']}.")
    print(f"Phí giao dịch 10%: {fee:,.1f} token")
    print(f"Số token thực nhận về ví: {actual_received:,.1f} token")
    print(f"Fan Token còn lại của {player_name}: {players[index]['fan_tokens']:,}")
    logging.info(f"Withdrawn {withdraw_amount} tokens from {players[index]['player_id']}. Actual received: {actual_received}")

def update_form(players: list) -> None:
    print("\n--- CẬP NHẬT HỆ SỐ PHONG ĐỘ ---")
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    index = find_player_by_id(players, player_id)
    if index == -1:
        print("\nKhông tìm thấy tuyển thủ!")
        logging.warning(f"Update form failed - Player {player_id} not found")
        return

    player_name = players[index].get("name", "Unknown")

    while True:
        try:
            new_form = float(input("Nhập hệ số phong độ mới (0.5 - 2.5): ").strip())
            if not (0.5 <= new_form <= 2.5):
                print("\nHệ số phong độ chỉ được nằm trong khoảng 0.5 đến 2.5.")
                continue
            break
        except ValueError:
            print("\nHệ số phong độ phải là số thực. Vui lòng nhập lại.")

    players[index]["form_multiplier"] = new_form
    print(f"\nThành công: Đã cập nhật hệ số phong độ cho {player_name}.")
    print(f"Hệ số mới: x{new_form}")
    logging.info(f"Updated form multiplier for {players[index]['player_id']} to {new_form}")

def calculate_match_points(players: list) -> None:
    print("\n--- CHẤM ĐIỂM SAU TRẬN ĐẤU ---")
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    index = find_player_by_id(players, player_id)
    if index == -1:
        print("\nKhông tìm thấy tuyển thủ!")
        logging.warning(f"Calculate points failed - Player {player_id} not found")
        return

    while True:
        try:
            base_points = float(input("Nhập điểm gốc của trận đấu: ").strip())
            break
        except ValueError:
            print("\nĐiểm gốc phải là số. Vui lòng nhập lại.")

    player_name = players[index].get("name", "Unknown")
    form_multiplier = players[index].get("form_multiplier", 1.0)
    
    actual_points = base_points * form_multiplier
    players[index]["match_points"] = players[index].get("match_points", 0) + actual_points

    print(f"\n>> Tuyển thủ {player_name} nhận được {actual_points:,.0f} điểm (Hệ số x{form_multiplier}).")
    print(f"Tổng điểm: {players[index]['match_points']:,.0f}")
    logging.info(f"Added {actual_points} match points to {players[index]['player_id']}")

def main() -> None:
    players = [
        {"player_id": "T101", "name": "Faker", "market_value": 5000, "fan_tokens": 1500, "match_points": 0, "form_multiplier": 1.0},
        {"player_id": "GEN01", "name": "Chovy", "market_value": 4800, "fan_tokens": 800, "match_points": 500, "form_multiplier": 1.2},
        {"player_id": "DRX01", "name": "Deft", "market_value": 3000, "fan_tokens": 0, "match_points": 0, "form_multiplier": 0.8}
    ]

    while True:
        print("\n===== HỆ THỐNG RIKKEI ESPORTS FANTASY =====")
        print("1. Xem Sàn Giao Dịch Tuyển Thủ")
        print("2. Đầu tư Fan Token")
        print("3. Rút vốn (Hoàn trả Token)")
        print("4. Biến động phong độ (Cập nhật hệ số)")
        print("5. Chấm điểm sau trận đấu")
        print("6. Thoát hệ thống")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-6): ").strip()
        
        match choice:
            case "1":
                display_market(players)
            case "2":
                invest_tokens(players)
            case "3":
                withdraw_tokens(players)
            case "4":
                update_form(players)
            case "5":
                calculate_match_points(players)
            case "6":
                print("\nĐóng hệ thống Rikkei Esports Fantasy.")
                logging.info("System closed by user.")
                break
            case _:
                print("\nLựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 6.")

if __name__ == "__main__":
    main()