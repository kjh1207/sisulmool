def get_bridge_data():
    """
    사용자로부터 교량 길이, 단면 높이, 단면 너비 및 하중 정보를 입력받아 교량 데이터를 반환합니다.
    """
    # 교량 길이, 단면 높이, 단면 너비 입력
    while True:
        try:
            length = float(input("교량 길이를 입력하세요 (단위: m): "))
            break
        except ValueError:
            print("숫자로 입력해주세요.")

    while True:
        try:
            section_height = float(input("단면 높이를 입력하세요 (단위: m): "))
            break
        except ValueError:
            print("숫자로 입력해주세요.")

    while True:
        try:
            section_width = float(input("단면 너비를 입력하세요 (단위: m): "))
            break
        except ValueError:
            print("숫자로 입력해주세요.")

    # 단면 1차 모멘트 Q와 2차 모멘트 I 계산 (직사각형 단면)
    Q = (section_height ** 2) * section_width / 8
    I = (section_width * section_height ** 3) / 12

    # 하중 정보 입력을 위한 리스트
    point_moment_loads = []
    point_vertical_loads = []
    uniform_loads = []
    slope_loads = []

    # 부호 규약 설명
    print("\n부호 규약:")
    print("  - 외력 (하중 데이터 및 반력):")
    print("    - 전단력 V: 위쪽 (+), 아래쪽 (-)")
    print("    - 모멘트 M: 시계방향 (+), 반시계방향 (-)\n")

    # 하중 선택 및 입력 반복
    while True:
        print("\n하중 종류를 선택하세요:")
        print("위의 부호규약에 맞게 하중을 입력하세요")
        print("1. 포인트 모멘트 하중 입력")
        print("2. 포인트 수직하중 입력")
        print("3. 등분포 하중 입력")
        print("4. 사다리꼴 분포 하중 입력")
        print("5. 입력 종료")
        
        choice = input("선택 (1-5): ")
        
        if choice == '1':
            try:
                load = float(input("포인트 모멘트 하중을 입력하세요 (단위: kNm): "))
                while True:
                    position = float(input("포인트 모멘트 하중의 위치 a를 입력하세요 (단위: m): "))
                    if 0 <= position <= length:
                        break
                    else:
                        print(f"위치는 0과 {length} 사이여야 합니다.")
                point_moment_loads.append({"하중 크기": load, "위치 a": position})
            except ValueError:
                print("숫자로 입력해주세요.")
        
        elif choice == '2':
            try:
                load = float(input("포인트 수직하중을 입력하세요 (단위: kN): "))
                while True:
                    position = float(input("포인트 수직하중의 위치 a를 입력하세요 (단위: m): "))
                    if 0 <= position <= length:
                        break
                    else:
                        print(f"위치는 0과 {length} 사이여야 합니다.")
                point_vertical_loads.append({"하중 크기": load, "위치 a": position})
            except ValueError:
                print("숫자로 입력해주세요.")
        
        elif choice == '3':
            try:
                load = float(input("등분포 하중의 크기를 입력하세요 (단위: kN/m): "))
                while True:
                    start_position = float(input("등분포 하중의 시작 위치 a를 입력하세요 (단위: m): "))
                    end_position = float(input("등분포 하중의 끝 위치 b를 입력하세요 (단위: m): "))
                    if 0 <= start_position <= length and 0 <= end_position <= length:
                        break
                    else:
                        print(f"시작 및 끝 위치는 0과 {length} 사이여야 합니다.")
                uniform_loads.append({
                    "하중 크기": load,
                    "시작 위치 a": start_position,
                    "끝 위치 b": end_position
                })
            except ValueError:
                print("숫자로 입력해주세요.")
        
        elif choice == '4':
            try:
                while True:
                    start_position = float(input("사다리꼴 분포 하중의 시작 위치 a를 입력하세요 (단위: m): "))
                    end_position = float(input("사다리꼴 분포 하중의 끝 위치 b를 입력하세요 (단위: m): "))
                    if 0 <= start_position <= length and 0 <= end_position <= length:
                        break
                    else:
                        print(f"시작 및 끝 위치는 0과 {length} 사이여야 합니다.")
                
                start_load = float(input("시작 위치에서의 하중 크기를 입력하세요 (단위: kN/m): "))
                end_load = float(input("끝 위치에서의 하중 크기를 입력하세요 (단위: kN/m): "))
                
                # 삼각형 분포 하중의 기울기 계산
                triangle_slope = (end_load - start_load) / (end_position - start_position)
                
                # 삼각형 분포 하중 (증가분)
                slope_loads.append({
                    "하중 기울기": triangle_slope,
                    "시작 위치 a": start_position,
                    "끝 위치 b": end_position
                })
                
                # 등분포 하중 (시작 위치에서 고정된 하중)
                uniform_loads.append({
                    "하중 크기": start_load,
                    "시작 위치 a": start_position,
                    "끝 위치 b": end_position
                })
                
            except ValueError:
                print("숫자로 입력해주세요.")
        
        elif choice == '5':
            print("하중 입력을 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

    bridge_data = {
        "교량 길이": length,
        "단면 높이": section_height,
        "단면 너비": section_width,
        "단면 1차 모멘트 Q": Q,
        "단면 2차 모멘트 I": I,
        "포인트 모멘트 하중들": point_moment_loads,
        "포인트 수직하중들": point_vertical_loads,
        "등분포 하중들": uniform_loads,
        "경사 분포 하중들": slope_loads
    }

    return bridge_data

def calculate_support_reactions(bridge_data):
    """
    교량의 평형 조건을 사용하여 반력을 계산합니다. 
    
    """
    length = bridge_data["교량 길이"]
    
    # 각 하중을 토대로 총 하중 및 모멘트 평형을 고려하여 R_A, R_B를 계산
    total_vertical_load = 0
    total_moment_about_A = 0
    
    # 포인트 수직 하중 처리
    for load in bridge_data["포인트 수직하중들"]:
        P = load["하중 크기"]
        a = load["위치 a"]
        total_vertical_load += P
        total_moment_about_A += P * a
    
    # 포인트 모멘트 하중 처리
    for load in bridge_data["포인트 모멘트 하중들"]:
        M0 = load["하중 크기"]
        a = load["위치 a"]
        total_moment_about_A += M0  # 포인트 모멘트 하중은 직접 모멘트에 더함
    
    # 등분포 하중 처리
    for load in bridge_data["등분포 하중들"]:
        w = load["하중 크기"]
        a = load["시작 위치 a"]
        b = load["끝 위치 b"]
        length_w = b - a
        total_vertical_load += w * length_w
        total_moment_about_A += w * length_w * (a + length_w / 2)
    
    # 경사 분포 하중 처리
    for load in bridge_data["경사 분포 하중들"]:
        m = load["하중 기울기"]
        a = load["시작 위치 a"]
        b = load["끝 위치 b"]
        length_m = b - a
        total_vertical_load += (m / 2) * length_m ** 2
        total_moment_about_A += (m / 6) * length_m ** 2 * (2 * a + length_m)

    # 반력 계산 (모멘트 평형 및 수직 평형 방정식)
    R_B = total_moment_about_A / length
    R_A = total_vertical_load - R_B

    return {"R_A": R_A, "R_B": R_B}


def get_position(bridge_length, section_height, section_width):
    y_max = section_height / 2
    z_max = section_width / 2

    while True:
        try:
            position_input = input(f"구하고자 하는 위치 x (0~{bridge_length}), y (±{y_max}), z (±{z_max}) 값을 입력하세요 (쉼표로 구분, z는 기본값 0): ")
            position_values = position_input.split(",")
            
            x = float(position_values[0].strip())
            y = float(position_values[1].strip())
            z = float(position_values[2].strip()) if len(position_values) > 2 else 0.0
            
            if not (0 <= x <= bridge_length):
                print(f"x 값은 0과 {bridge_length} 사이여야 합니다.")
                continue
            if not (-y_max <= y <= y_max):
                print(f"y 값은 -{y_max}와 {y_max} 사이여야 합니다.")
                continue
            if not (-z_max <= z <= z_max):
                print(f"z 값은 -{z_max}와 {z_max} 사이여야 합니다.")
                continue

            return x, y, z

        except (ValueError, IndexError):
            print("입력 형식이 올바르지 않습니다. 예: 4, 0.5, 0 (또는 4, 0.5)")

def calculate_shear_moment_with_discontinuity(bridge_data, x, y, reactions):
    """
    포인트 하중에 의해 불연속이 발생하는 지점에서 전단력과 모멘트를 계산하고,
    불연속 발생 지점에서는 큰 값을 반환합니다.
    
    Parameters:
    - bridge_data: 교량 데이터
    - x: 내력 계산 위치
    - y: 중립축에서의 거리
    - reactions: 지점 반력
    
    Returns:
    - V_final: 전단력 (불연속 시 큰 값 반환)
    - M_final: 모멘트 (불연속 시 큰 값 반환)
    """
    V_before = reactions["R_A"]
    M_before = reactions["R_A"] * x

    # 포인트 수직 하중 처리
    for load in bridge_data["포인트 수직하중들"]:
        P = load["하중 크기"]
        a = load["위치 a"]
        
        if x > a:  # 일반적인 전단력 및 모멘트 계산
            V_before -= P
            M_before -= P * (x - a)
        elif x == a:  # 불연속 지점에서 두 값 중 큰 값 선택
            V_after = V_before - P
            M_after = M_before - P * (x - a)
            V_before = max(abs(V_before), abs(V_after)) * (1 if V_before > V_after else -1)
            M_before = max(abs(M_before), abs(M_after)) * (1 if M_before > M_after else -1)

    # 포인트 모멘트 하중 처리
    for load in bridge_data["포인트 모멘트 하중들"]:
        M0 = load["하중 크기"]
        a = load["위치 a"]
        if x == a:  # 불연속 지점에서 모멘트의 큰 값 선택
            M_after = M_before + M0
            M_before = max(abs(M_before), abs(M_after)) * (1 if M_before > M_after else -1)
        elif x > a:  # 일반적인 모멘트 계산
            M_before += M0

    # 등분포 하중 및 삼각분포 하중 처리
    for load in bridge_data["등분포 하중들"]:
        w = load["하중 크기"]
        a = load["시작 위치 a"]
        b = load["끝 위치 b"]
        if x >= a:
            if x <= b:
                V_before -= w * (x - a)
                M_before -= (w / 2) * (x - a) ** 2
            else:
                V_before -= w * (b - a)
                M_before -= (w / 2) * (b - a) * (2 * x - a - b)

    for load in bridge_data["경사 분포 하중들"]:
        m = load["하중 기울기"]
        a = load["시작 위치 a"]
        b = load["끝 위치 b"]
        if x >= a:
            if x <= b:
                V_before -= (m / 2) * (x - a) ** 2
                M_before -= (m / 6) * (x - a) ** 3
            else:
                V_before -= (m / 2) * (b - a) ** 2
                M_before -= (m / 6) * (b - a) ** 2 * (3 * x - a - b)

    V_final = V_before
    M_final = M_before

    return V_final, M_final


import numpy as np

def calculate_stress_tensor(bending_stress, shear_stress):
    """
    원래 응력 텐서를 구성하여 가장 큰 값의 유효 숫자에 따라 출력합니다.
    
    Parameters:
    - bending_stress: 휨응력 (sigma_xx)
    - shear_stress: 전단응력 (sigma_xy)
    
    Returns:
    - stress_tensor: 3x3 응력 텐서
    """
    # 3x3 응력 텐서 생성
    stress_tensor = np.array([
        [sigma_xx, sigma_xy, 0],
        [sigma_xy, 0, 0],
        [0, 0, 0]
    ])
    
    # 응력 텐서 이름
    tensor_labels = [
        ["σ_xx", "σ_xy", "σ_xz"],
        ["σ_yx", "σ_yy", "σ_yz"],
        ["σ_zx", "σ_zy", "σ_zz"]
    ]
    
    print("\n응력 텐서:")
    print_labeled_tensor(tensor_labels, stress_tensor)
    
    return stress_tensor

def calculate_principal_stresses(stress_tensor):
    """
    주응력을 계산하고, 주응력을 대각선에 배치한 3x3 텐서를 출력합니다.
    
    Parameters:
    - stress_tensor: 원래 응력 텐서 (3x3 형태의 numpy 배열)
    
    Returns:
    - principal_stress_tensor: 주응력을 대각선에 배치한 3x3 텐서
    """
    sigma_xx = stress_tensor[0, 0]
    sigma_xy = stress_tensor[0, 1]
    sigma_yy = stress_tensor[1, 1]
    
    # 주응력 계산 공식
    sigma_avg = (sigma_xx + sigma_yy) / 2
    R = np.sqrt(((sigma_xx - sigma_yy) / 2) ** 2 + sigma_xy ** 2)
    sigma_1 = sigma_avg + R
    sigma_2 = sigma_avg - R
    sigma_3 = 0  # z축 방향 응력은 0으로 가정
    
    # 주응력 텐서 생성
    principal_stress_tensor = np.array([
        [sigma_1, 0, 0],
        [0, sigma_2, 0],
        [0, 0, sigma_3]
    ])
    
    # 주응력 텐서 이름
    principal_labels = [
        ["σ_1", "0", "0"],
        ["0", "σ_2", "0"],
        ["0", "0", "σ_3"]
    ]
    
    print("\n주응력 텐서:")
    print_labeled_tensor(principal_labels, principal_stress_tensor)
    
    return principal_stress_tensor


def print_labeled_tensor(labels, tensor):
    """
    응력 텐서의 이름과 계산된 값을 나란히 출력합니다.
    
    Parameters:
    - labels: 텐서 요소의 이름 (예: "σ_xx")
    - tensor: 해당 위치의 계산된 값 (3x3 numpy 배열)
    """
    max_value = np.max(np.abs(tensor))
    max_digits = len(f"{int(max_value)}")
    precision = 4 - max_digits  # 최대 4자리로 출력
    
    for label_row, value_row in zip(labels, tensor):
        label_str = " | ".join(f"{label:>6}" for label in label_row)
        value_str = " | ".join(f"{val:>{max_digits + precision + 2}.{precision}f}" for val in value_row)
        print(f"{label_str}   =   {value_str}")



#실제 작동에 필요한 명령어 코드들


# 교량 데이터 및 반력 계산
bridge_info = get_bridge_data()
reactions = calculate_support_reactions(bridge_info)  # 실제 반력 계산 함수 호출

# 위치 정보를 한 번에 입력받아 x, y, z로 나누기
x, y, z = get_position(bridge_info["교량 길이"], bridge_info["단면 높이"], bridge_info["단면 너비"])

# 불연속을 고려하여 전단력과 모멘트 계산
V_result, M_result = calculate_shear_moment_with_discontinuity(bridge_info, x, y, reactions)

# 전단응력과 휨응력 계산
sigma_xx = -M_result * y / bridge_info["단면 2차 모멘트 I"]
sigma_xy = -V_result * bridge_info["단면 1차 모멘트 Q"] / (bridge_info["단면 2차 모멘트 I"] * bridge_info["단면 너비"])


# 반력 및 최종 결과 출력
print("\n--- 반력 결과 ---")
print(f"반력 R_A: {reactions['R_A']} kN")
print(f"반력 R_B: {reactions['R_B']} kN")
print(f"전단력 (V): {V_result} kN")
print(f"모멘트 (M): {M_result} kNm")

# 원래 응력 텐서 계산 및 출력
stress_tensor = calculate_stress_tensor(sigma_xx, sigma_xy)

# 주응력 텐서 계산 및 출력
principal_stress_tensor = calculate_principal_stresses(stress_tensor)

import os
os.system("pause")