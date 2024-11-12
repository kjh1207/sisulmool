import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 보의 기본 정보 입력 받기
def get_positive_value(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("값은 0보다 커야 합니다. 다시 입력해주세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

beam_height = get_positive_value("보의 단면 높이를 입력하세요 (m): ")
beam_width = get_positive_value("보의 단면 너비를 입력하세요 (m): ")
beam_length = get_positive_value("보의 길이를 입력하세요 (m): ")

# 하중 정보 입력 받기 (하중 위치에 대한 제한 추가)
def get_load_value(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

def get_load_info():
    loads = []
    while True:
        load_type = input("어떤 하중을 추가하시겠습니까? (1: 집중하중 / 2: 사다리꼴 분포하중 / 3: 포인트 모멘트 / 종료: 0): ").strip()
        if load_type == "1":
            while True:
                position = get_load_value("집중하중 위치를 입력하세요 (m): ")
                if 0 <= position <= beam_length:
                    break
                else:
                    print(f"집중하중 위치는 0 이상 {beam_length} 이하여야 합니다. 다시 입력해주세요.")
            magnitude = get_load_value("집중하중 크기를 입력하세요 (kN): ")
            loads.append({"type": "point_load", "position": position, "magnitude": magnitude})
        elif load_type == "2":
            while True:
                start_position = get_load_value("사다리꼴 분포하중 시작 위치를 입력하세요 (m): ")
                end_position = get_load_value("사다리꼴 분포하중 끝 위치를 입력하세요 (m): ")
                if 0 <= start_position <= end_position <= beam_length:
                    break
                else:
                    print(f"사다리꼴 분포하중 시작과 끝 위치는 0 이상 {beam_length} 이하여야 하며, 시작 위치는 끝 위치보다 작아야 합니다. 다시 입력해주세요.")
            start_magnitude = get_load_value("사다리꼴 분포하중 시작 크기를 입력하세요 (kN/m): ")
            end_magnitude = get_load_value("사다리꼴 분포하중 끝 크기를 입력하세요 (kN/m): ")
            loads.append({"type": "trapezoidal_load", "start_position": start_position, "end_position": end_position, "start_magnitude": start_magnitude, "end_magnitude": end_magnitude})
        elif load_type == "3":
            while True:
                position = get_load_value("포인트 모멘트 위치를 입력하세요 (m): ")
                if 0 <= position <= beam_length:
                    break
                else:
                    print(f"포인트 모멘트 위치는 0 이상 {beam_length} 이하여야 합니다. 다시 입력해주세요.")
            magnitude = get_load_value("포인트 모멘트 크기를 입력하세요 (kNm): ")
            loads.append({"type": "point_moment", "position": position, "magnitude": magnitude})
        elif load_type == "0":
            break
        else:
            print("잘못된 하중 유형입니다. 다시 시도해주세요.")
    return loads

# 하중 입력 받기
loads = get_load_info()

# 하중 합력 계산 함수 정의
def calculate_combined_loads(loads, beam_length):
    x_values = np.linspace(0, beam_length, 1000)
    combined_loads = np.zeros_like(x_values)
    combined_moments = np.zeros_like(x_values)

    for load in loads:
        if load["type"] == "point_load":
            position_index = (np.abs(x_values - load["position"])).argmin()
            combined_loads[position_index] += load["magnitude"]
        elif load["type"] == "trapezoidal_load":
            for i, x in enumerate(x_values):
                if load["start_position"] <= x <= load["end_position"]:
                    if load["end_position"] != load["start_position"]:
                        magnitude_at_x = load["start_magnitude"] + (load["end_magnitude"] - load["start_magnitude"]) * ((x - load["start_position"]) / (load["end_position"] - load["start_position"]))
                    else:
                        magnitude_at_x = load["start_magnitude"]
                    combined_loads[i] += magnitude_at_x
        elif load["type"] == "point_moment":
            position_index = (np.abs(x_values - load["position"])).argmin()
            combined_moments[position_index] += load["magnitude"]

    return x_values, combined_loads, combined_moments

# 하중 합력 계산
x_values, combined_loads, combined_moments = calculate_combined_loads(loads, beam_length)

# 지점 반력 계산 (힌지 지점은 왼쪽 끝, 롤러 지점은 오른쪽 끝)
def calculate_support_reactions(loads, beam_length):
    total_force = 0
    total_moment = 0

    for load in loads:
        if load["type"] == "point_load":
            total_force += load["magnitude"]
            total_moment += load["magnitude"] * (load["position"] - 0)
        elif load["type"] == "trapezoidal_load":
            start_pos = load["start_position"]
            end_pos = load["end_position"]
            start_mag = load["start_magnitude"]
            end_mag = load["end_magnitude"]
            length = end_pos - start_pos
            total_force += 0.5 * (start_mag + end_mag) * length
            centroid = start_pos + length * (2 * start_mag + end_mag) / (3 * (start_mag + end_mag)) if start_mag != end_mag else (start_pos + end_pos) / 2
            total_moment += 0.5 * (start_mag + end_mag) * length * (centroid - 0)
        elif load["type"] == "point_moment":
            total_moment += load["magnitude"]

    # 힌지 지점 (A)에서 수평 반력은 0으로 가정
    horizontal_reaction_a = 0
    # 롤러 지점 (B)에서의 수직 반력 계산
    vertical_reaction_b = total_moment / beam_length
    # 힌지 지점 (A)에서의 수직 반력 계산
    vertical_reaction_a = total_force - vertical_reaction_b

    return horizontal_reaction_a, vertical_reaction_a, vertical_reaction_b

# 지점 반력 계산
horizontal_reaction_a, vertical_reaction_a, vertical_reaction_b = calculate_support_reactions(loads, beam_length)
print(f"힌지 지점 반력 (A 지점) - 수평 반력: {horizontal_reaction_a:.2f} kN, 수직 반력: {vertical_reaction_a:.2f} kN")
print(f"롤러 지점 반력 (B 지점) - 수직 반력: {vertical_reaction_b:.2f} kN")

# 특정 지점 X m에서의 내력 계산 함수 정의
def calculate_internal_forces(x, loads, beam_length, horizontal_reaction_a, vertical_reaction_a):
    axial_force = horizontal_reaction_a
    shear_force = vertical_reaction_a
    bending_moment = 0

    for load in loads:
        if load["type"] == "point_load":
            if load["position"] <= x:
                shear_force += load["magnitude"]
                bending_moment += load["magnitude"] * (x - load["position"])
        elif load["type"] == "trapezoidal_load":
            if load["start_position"] <= x:
                if x <= load["end_position"]:
                    length = x - load["start_position"]
                    start_mag = load["start_magnitude"]
                    end_mag = load["end_magnitude"]
                    force = 0.5 * (start_mag + (start_mag + (end_mag - start_mag) * (length / (load["end_position"] - load["start_position"])))) * length
                    shear_force += force
                    centroid = load["start_position"] + length / 3 if start_mag == end_mag else load["start_position"] + length * (2 * start_mag + end_mag) / (3 * (start_mag + end_mag))
                    bending_moment += force * (x - centroid)
                else:
                    length = load["end_position"] - load["start_position"]
                    start_mag = load["start_magnitude"]
                    end_mag = load["end_magnitude"]
                    force = 0.5 * (start_mag + end_mag) * length
                    shear_force += force
                    centroid = load["start_position"] + length / 3 if start_mag == end_mag else load["start_position"] + length * (2 * start_mag + end_mag) / (3 * (start_mag + end_mag))
                    bending_moment += force * (x - centroid)
        elif load["type"] == "point_moment":
            if load["position"] <= x:
                bending_moment += load["magnitude"]

    return axial_force, shear_force, bending_moment

# 특정 지점 X m에서의 내력 계산
while True:
    x = get_load_value("내력을 계산할 위치 X를 입력하세요 (m): ")
    if 0 <= x <= beam_length:
        break
    else:
        print(f"위치 X는 0 이상 {beam_length} 이하여야 합니다. 다시 입력해주세요.")
axial_force, shear_force, bending_moment = calculate_internal_forces(x, loads, beam_length, horizontal_reaction_a, vertical_reaction_a)
print(f"지점 X = {x:.2f} m에서의 내력: 축력 = {axial_force:.2f} kN, 전단력 = {shear_force:.2f} kN, 휨모멘트 = {bending_moment:.2f} kNm")

# 3x3 응력 텐서 계산 및 출력
stress_tensor = np.array([
    [axial_force / (beam_width * beam_height), 0, 0],
    [0, shear_force / beam_width, 0],
    [0, 0, bending_moment / (beam_width * beam_height**2 / 6)]
])

print("3x3 응력 텐서:")
for row in stress_tensor:
    print(' '.join([f'{value:.2f}' for value in row]))

# 주응력 계산
def calculate_principal_stresses(stress_tensor):
    stress_matrix = np.array(stress_tensor)
    eigenvalues, _ = np.linalg.eig(stress_matrix)
    principal_stresses = np.sort(eigenvalues)[::-1]  # 내림차순 정렬
    return principal_stresses

principal_stresses = calculate_principal_stresses(stress_tensor)
print("주응력 (Principal Stresses):")
for i, stress in enumerate(principal_stresses, 1):
    print(f"Principal Stresses {i}: {stress:.2f} kN/m²")

# 평면응력 그림 위에 주응력 표시
fig, ax = plt.subplots()
ax.add_patch(patches.Rectangle((0, 0), beam_width, beam_height, edgecolor='black', facecolor='lightgray'))

# 주응력 화살표 그리기
stress_scale = 0.5  # 화살표 크기 조정
center_x = beam_width / 2
center_y = beam_height / 2

# 주응력 1 (가장 큰 주응력)
ax.arrow(center_x, center_y, stress_scale * principal_stresses[0], 0, head_width=0.2, head_length=0.2, fc='red', ec='red', label=r'$\sigma_{p1}$')
# 주응력 2 (두 번째 큰 주응력)
ax.arrow(center_x, center_y, 0, stress_scale * principal_stresses[1], head_width=0.2, head_length=0.2, fc='blue', ec='blue', label=r'$\sigma_{p2}$')
# 주응력 3 (세 번째 주응력)
ax.arrow(center_x, center_y, stress_scale * principal_stresses[2], stress_scale * principal_stresses[2], head_width=0.2, head_length=0.2, fc='green', ec='green', label=r'$\sigma_{p3}$')

ax.set_xlim(-beam_width, 2 * beam_width)
ax.set_ylim(-beam_height, 2 * beam_height)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel('Width (m)')
ax.set_ylabel('Height (m)')
ax.set_title('Principal Stresses on Cross-Section')
plt.legend()
plt.grid(True)
plt.show()
