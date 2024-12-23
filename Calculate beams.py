import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import simpledialog, messagebox

# 전역 변수 설정
length = 0
section_height = 0
section_width = 0

def get_bridge_data():
    """
    사용자로부터 교량 길이, 단면 높이, 단면 너비 및 하중 정보를 입력받아 교량 데이터를 반환합니다.
    """
    global length, section_height, section_width

    root = tk.Tk()
    root.withdraw()  # 기본 Tkinter 창 숨기기

    # 교량 길이, 단면 높이, 단면 너비 입력
    input_window = tk.Toplevel(root)
    input_window.title("교량 정보 입력")
    input_window.grab_set()  # 창 활성화

    tk.Label(input_window, text="교량 길이 (m):").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(input_window, text="단면 높이 (m):").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(input_window, text="단면 너비 (m):").grid(row=2, column=0, padx=10, pady=5)

    length_entry = tk.Entry(input_window)
    length_entry.grid(row=0, column=1, padx=10, pady=5)
    length_entry.focus_set()  # 포커스 설정
    section_height_entry = tk.Entry(input_window)
    section_height_entry.grid(row=1, column=1, padx=10, pady=5)
    section_width_entry = tk.Entry(input_window)
    section_width_entry.grid(row=2, column=1, padx=10, pady=5)

    def submit_bridge_data():
        global length, section_height, section_width
        try:
            length = float(length_entry.get())
            section_height = float(section_height_entry.get())
            section_width = float(section_width_entry.get())
            if length > 0 and section_height > 0 and section_width > 0:
                input_window.destroy()
            else:
                messagebox.showerror("입력 오류", "모든 값은 0보다 커야 합니다. 다시 입력해주세요.")
        except ValueError:
            messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

    def cancel_bridge_data():
        messagebox.showinfo("종료", "프로그램을 종료합니다.")
        root.destroy()
        exit()

    tk.Button(input_window, text="확인", command=submit_bridge_data).grid(row=3, column=0, pady=10)
    tk.Button(input_window, text="취소", command=cancel_bridge_data).grid(row=3, column=1, pady=10)

    # Enter 키로 확인 버튼 동작 연결
    input_window.bind('<Return>', lambda event: submit_bridge_data())

    input_window.grab_set()
    root.wait_window(input_window)
    if not length and not section_height and not section_width:
        try:
            root.quit()
        except tk.TclError:
            pass
        exit()

    # 하중 정보 입력을 위한 리스트
    point_moment_loads = []
    point_vertical_loads = []
    uniform_loads = []
    slope_loads = []
    
    # 하중 선택 및 입력 반복
    while True:
        choice = simpledialog.askstring("하중 종류 선택", "하중 종류를 선택하세요:\n1. 포인트 모멘트 하중 입력\n2. 포인트 수직하중 입력\n3. 등분포 하중 입력\n4. 사다리꼴 분포 하중 입력\n5. 입력 종료")
        if choice is None:
            messagebox.showinfo("종료", "프로그램을 종료합니다.")
            root.quit()
            exit()

        if choice == '1':  # 포인트 모멘트 하중 입력
            try:
                load_window = tk.Toplevel(root)
                load_window.title("포인트 모멘트 하중 입력")

                # Add moment sign convention explanation
                tk.Label(load_window, text="모멘트 하중 부호 규약:\n- 시계방향 (+)\n- 반시계방향 (-)",
                        justify="left", fg="blue", font=("Arial", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

                tk.Label(load_window, text="하중 크기 (kNm):").grid(row=1, column=0, padx=10, pady=5)
                tk.Label(load_window, text=f"위치 (m, 0 ~ {length}):").grid(row=2, column=0, padx=10, pady=5)

                load_entry = tk.Entry(load_window)
                load_entry.grid(row=1, column=1, padx=10, pady=5)
                position_entry = tk.Entry(load_window)
                position_entry.grid(row=2, column=1, padx=10, pady=5)
                
                load_window.grab_set()
                load_window.focus_force()

                # 창이 완전히 로드된 후 입력 필드 초점 설정
                load_window.after(100, lambda: load_entry.focus_set())

                def submit_load():
                    try:
                        load = float(load_entry.get())
                        position = float(position_entry.get())
                        if 0 <= position <= length:
                            point_moment_loads.append({"하중 크기": load, "위치 a": position})
                            load_window.destroy()
                        else:
                            messagebox.showerror("입력 오류", f"위치는 0과 {length} 사이여야 합니다.")
                    except ValueError:
                        messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

                tk.Button(load_window, text="확인", command=submit_load).grid(row=3, columnspan=2, pady=10)
                load_window.bind('<Return>', lambda event: submit_load())
                load_window.grab_set()
                root.wait_window(load_window)
            except ValueError:
                messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

        elif choice == '2':  # 포인트 수직하중 입력
            try:
                load_window = tk.Toplevel(root)
                load_window.title("포인트 수직하중 입력")

                # Add shear force sign convention explanation
                tk.Label(load_window, text="수직하중 부호 규약:\n- 위쪽 (-)\n- 아래쪽 (+)",
                        justify="left", fg="blue", font=("Arial", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

                tk.Label(load_window, text="하중 크기 (kN):").grid(row=1, column=0, padx=10, pady=5)
                tk.Label(load_window, text=f"위치 (m, 0 ~ {length}):").grid(row=2, column=0, padx=10, pady=5)

                load_entry = tk.Entry(load_window)
                load_entry.grid(row=1, column=1, padx=10, pady=5)
                position_entry = tk.Entry(load_window)
                position_entry.grid(row=2, column=1, padx=10, pady=5)

                load_window.grab_set()
                load_window.focus_force()

                # 창이 완전히 로드된 후 입력 필드 초점 설정
                load_window.after(100, lambda: load_entry.focus_set())

                def submit_load():
                    try:
                        load = float(load_entry.get())
                        position = float(position_entry.get())
                        if 0 <= position <= length:
                            point_vertical_loads.append({"하중 크기": load, "위치 a": position})
                            load_window.destroy()
                        else:
                            messagebox.showerror("입력 오류", f"위치는 0과 {length} 사이여야 합니다.")
                    except ValueError:
                        messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

                tk.Button(load_window, text="확인", command=submit_load).grid(row=3, columnspan=2, pady=10)
                load_window.bind('<Return>', lambda event: submit_load())
                load_window.grab_set()
                root.wait_window(load_window)
            except ValueError:
                messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

        elif choice == '3':  # 등분포 하중 입력
            try:
                load_window = tk.Toplevel(root)
                load_window.title("등분포 하중 입력")

                # Add shear force sign convention explanation
                tk.Label(load_window, text="등분포하중 부호 규약:\n- 위쪽 (-)\n- 아래쪽 (+)",
                        justify="left", fg="blue", font=("Arial", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

                tk.Label(load_window, text="하중 크기 (kN/m):").grid(row=1, column=0, padx=10, pady=5)
                tk.Label(load_window, text=f"시작 위치 a (m, 0 ~ {length}):").grid(row=2, column=0, padx=10, pady=5)
                tk.Label(load_window, text=f"끝 위치 b (m, 0 ~ {length}):").grid(row=3, column=0, padx=10, pady=5)

                load_entry = tk.Entry(load_window)
                load_entry.grid(row=1, column=1, padx=10, pady=5)
                start_position_entry = tk.Entry(load_window)
                start_position_entry.grid(row=2, column=1, padx=10, pady=5)
                end_position_entry = tk.Entry(load_window)
                end_position_entry.grid(row=3, column=1, padx=10, pady=5)

                load_window.grab_set()
                load_window.focus_force()

                # 창이 완전히 로드된 후 입력 필드 초점 설정
                load_window.after(100, lambda: load_entry.focus_set())

                def submit_load():
                    try:
                        load = float(load_entry.get())
                        start_position = float(start_position_entry.get())
                        end_position = float(end_position_entry.get())
                        if start_position == end_position:
                            messagebox.showerror("입력 오류", "시작 위치와 끝 위치는 같을 수 없습니다. 다시 입력해주세요.")
                            return
                        if 0 <= start_position <= length and 0 <= end_position <= length:
                            uniform_loads.append({
                                "하중 크기": load,
                                "시작 위치 a": start_position,
                                "끝 위치 b": end_position
                            })
                            load_window.destroy()
                        else:
                            messagebox.showerror("입력 오류", f"시작 및 끝 위치는 0과 {length} 사이여야 합니다.")
                    except ValueError:
                        messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

                tk.Button(load_window, text="확인", command=submit_load).grid(row=4, columnspan=2, pady=10)
                load_window.bind('<Return>', lambda event: submit_load())
                load_window.grab_set()
                root.wait_window(load_window)
            except ValueError:
                messagebox.showerror("입력 오류", "숫자로 입력해주세요.")


        elif choice == '4':  # 사다리꼴 분포 하중 입력
            try:
                load_window = tk.Toplevel(root)
                load_window.title("사다리꼴 분포 하중 입력")

                # Add shear force sign convention explanation
                tk.Label(load_window, text="분포하중 부호 규약:\n- 위쪽 (-)\n- 아래쪽 (+)",
                        justify="left", fg="blue", font=("Arial", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

                tk.Label(load_window, text=f"시작 위치 a (m, 0 ~ {length}):").grid(row=1, column=0, padx=10, pady=5)
                tk.Label(load_window, text=f"끝 위치 b (m, 0 ~ {length}):").grid(row=2, column=0, padx=10, pady=5)
                tk.Label(load_window, text="시작 위치 하중 크기 (kN/m):").grid(row=3, column=0, padx=10, pady=5)
                tk.Label(load_window, text="끝 위치 하중 크기 (kN/m):").grid(row=4, column=0, padx=10, pady=5)

                start_position_entry = tk.Entry(load_window)
                start_position_entry.grid(row=1, column=1, padx=10, pady=5)
                end_position_entry = tk.Entry(load_window)
                end_position_entry.grid(row=2, column=1, padx=10, pady=5)
                start_load_entry = tk.Entry(load_window)
                start_load_entry.grid(row=3, column=1, padx=10, pady=5)
                end_load_entry = tk.Entry(load_window)
                end_load_entry.grid(row=4, column=1, padx=10, pady=5)

                load_window.grab_set()
                load_window.focus_force()
                load_window.after(100, lambda: start_position_entry.focus_set())

                def submit_load():
                    try:
                        start_position = float(start_position_entry.get())
                        end_position = float(end_position_entry.get())
                        start_load = float(start_load_entry.get())
                        end_load = float(end_load_entry.get())

                        if start_position == end_position:
                            messagebox.showerror("입력 오류", "시작 위치와 끝 위치는 같을 수 없습니다. 다시 입력해주세요.")
                            return
                        if 0 <= start_position <= length and 0 <= end_position <= length:
                            slope_loads.append({
                                "하중 기울기": (end_load - start_load) / (end_position - start_position),
                                "시작 위치 a": start_position,
                                "끝 위치 b": end_position
                            })
                            uniform_loads.append({
                                "하중 크기": start_load,
                                "시작 위치 a": start_position,
                                "끝 위치 b": end_position
                            })
                            load_window.destroy()
                        else:
                            messagebox.showerror("입력 오류", f"시작 및 끝 위치는 0과 {length} 사이여야 합니다.")
                    except ValueError:
                        messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

                tk.Button(load_window, text="확인", command=submit_load).grid(row=5, columnspan=2, pady=10)
                load_window.bind('<Return>', lambda event: submit_load())
                load_window.grab_set()
                root.wait_window(load_window)
            except ValueError:
                messagebox.showerror("입력 오류", "숫자로 입력해주세요.")

        
        elif choice == '5':
            messagebox.showinfo("종료", "하중 입력을 종료합니다.")
            break
        
        else:
            messagebox.showerror("입력 오류", "잘못된 선택입니다. 다시 입력해주세요.")

    bridge_data = {
        "교량 길이": length,
        "단면 높이": section_height,
        "단면 너비": section_width,
        "포인트 모멘트 하중들": point_moment_loads,
        "포인트 수직하중들": point_vertical_loads,
        "등분포 하중들": uniform_loads,
        "경사 분포 하중들": slope_loads,
        "cracks": []
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

    # 삼각형 총 하중 계산 (절대값 사용)
        W = abs(m) / 2 * length_m ** 2
        total_vertical_load += W

    # 무게중심 계산
        if m > 0:  # 오른쪽 최대
           x_center = a + (2 / 3) * length_m
        else:  # 왼쪽 최대
           x_center = a + (1 / 3) * length_m

    # A점 기준 모멘트 계산
        M = W * x_center
        total_moment_about_A += M


    # 반력 계산 (모멘트 평형 및 수직 평형 방정식)
    R_B = total_moment_about_A / length
    R_A = total_vertical_load - R_B

    return {"R_A": R_A, "R_B": R_B}

def get_position(bridge_length, section_height, section_width):
    y_max = section_height / 2
    z_max = section_width / 2

    root = tk.Tk()
    root.title("응력 위치 입력")

    root.grab_set()
    root.focus_force()

    # Bind Enter key to submit action
    root.bind('<Return>', lambda event: submit())

    # Create and configure the input form
    tk.Label(root, text=f"x (0 ~ {bridge_length}):").grid(row=0, column=0, padx=10, pady=5)
    x_entry = tk.Entry(root)
    x_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text=f"y (±{y_max}):").grid(row=1, column=0, padx=10, pady=5)
    y_entry = tk.Entry(root)
    y_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text=f"z (±{z_max}, 기본값 0):").grid(row=2, column=0, padx=10, pady=5)
    z_entry = tk.Entry(root)
    z_entry.grid(row=2, column=1, padx=10, pady=5)

    root.after(100, lambda: x_entry.focus_set())

    def submit():
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            z = float(z_entry.get()) if z_entry.get() else 0.0

            if not (0 <= x <= bridge_length):
                messagebox.showerror("입력 오류", f"x 값은 0과 {bridge_length} 사이여야 합니다.")
                return
            if not (-y_max <= y <= y_max):
                messagebox.showerror("입력 오류", f"y 값은 -{y_max}와 {y_max} 사이여야 합니다.")
                return
            if not (-z_max <= z <= z_max):
                messagebox.showerror("입력 오류", f"z 값은 -{z_max}와 {z_max} 사이여야 합니다.")
                return
            
            root.quit()
            root.destroy()

            root.result = (x, y, z)

        except ValueError:
            messagebox.showerror("입력 오류", "입력 형식이 올바르지 않습니다. 올바른 숫자를 입력하세요.")

    def cancel():
        messagebox.showinfo("취소됨", "입력을 취소하고 코드를 종료합니다.")
        root.quit()
        root.destroy()
        root.result = None

    tk.Button(root, text="입력", command=submit).grid(row=3, column=0, pady=10)
    tk.Button(root, text="취소", command=cancel).grid(row=3, column=1, pady=10)

    root.mainloop()

    if hasattr(root, 'result') and root.result is not None:
        return root.result
    else:
        raise SystemExit("사용자가 입력을 취소했습니다.")

            
# 데이터 추가 함수
def update_bridge_data(new_data):
    global bridge_data
    bridge_data.update(new_data)

# 단면 속성 계산 함수
def calculate_section_properties(y, section_width, section_height):
    """
    직사각형 단면의 1차 모멘트 Q와 2차 모멘트 I를 계산합니다.
    """
    I = (section_width * section_height ** 3) / 12
    
    # 중립축 위치 계산
    neutral_axis = section_height / 2

    # 단면 1차 모멘트 (Q)
    if y >= 0:  # 중립축 상부
        effective_height = neutral_axis - y
    else:  # 중립축 하부
        effective_height = neutral_axis + y

    if effective_height > 0:
        area = section_width * effective_height
        centroid_distance = effective_height / 2 + abs(y)  # 무게중심까지의 거리
        Q = area * centroid_distance
    else:
        Q = 0  # 사용할 수 있는 단면이 없으면 Q는 0

    return Q, I

# 내력 계산
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
    
    외력 부호규약 적용
    전단력 V: 위쪽 (-), 아래쪽 (+)
    모멘트 M: 시계방향 (+), 반시계방향 (-)
    
    평형방정식 규약
    모멘트는 전부 시계방향을 +로 계산했음(결과값과는 무관함)
    """
    V_before = reactions["R_A"]
    M_before = reactions["R_A"] * x

    # 포인트 수직 하중 처리
    for load in bridge_data["포인트 수직하중들"]:
        P = load["하중 크기"]
        a = load["위치 a"]
        
        if x > a:  # 일반적인 전단력 및 모멘트 계산
            V_before -= P #-V+(-P)=0
            M_before -= P * (x - a)
        elif x == a:  # 불연속 지점에서 두 값 중 큰 값 선택
            V_after = V_before - P
            M_after = M_before - P * (x - a)
            # 전단력 비교: 절대값이 큰 값을 선택
            if abs(V_after) > abs(V_before):
                V_before = V_after
            else:
                V_before = V_before

            # 모멘트 비교: 절대값이 큰 값을 선택
            if abs(M_after) > abs(M_before):
                M_before = M_after
            else:
                M_before = M_before

    # 포인트 모멘트 하중 처리
    for load in bridge_data["포인트 모멘트 하중들"]:
        M0 = load["하중 크기"]
        a = load["위치 a"]
        if x == a:  # 불연속 지점에서 모멘트의 큰 값 선택
            M_after = M_before + M0
            
            if abs(M_after) > abs(M_before) :
                M_before = M_after
            else:
                M_before = M_before
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
    """
    max_value = np.max(np.abs(tensor))
    max_digits = len(f"{int(max_value)}") if max_value > 0 else 1  # 최소 1자리 확보
    precision = max(4 - max_digits, 0)  # 음수가 되지 않도록 제한

    for label_row, value_row in zip(labels, tensor):
        label_str = " | ".join(f"{label:>6}" for label in label_row)
        value_str = " | ".join(f"{val:>{max_digits + precision + 2}.{precision}f}" for val in value_row)
        print(f"{label_str}   =   {value_str}")

def plot_results_with_reactions(positions, reactions, shear_forces, bending_moments, bending_stresses, shear_stresses):
    bridge_length = max(positions)

    # Create subplots
    fig, axs = plt.subplots(4, 1, figsize=(12, 20), sharex=True)

    # Reaction forces diagram
    reaction_positions = [0, bridge_length]
    reaction_values = [reactions['R_A'], reactions['R_B']]
    axs[0].bar(reaction_positions, reaction_values, width=0.2, color='purple', label='Reaction Forces')
    axs[0].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axs[0].set_title("Reaction Forces Diagram")
    axs[0].set_ylabel("Force (kN)")
    axs[0].legend()
    axs[0].grid(True)

    # Shear force diagram
    axs[1].plot(positions, shear_forces, label="Shear Force (V)", color='blue', linewidth=2)
    axs[1].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axs[1].set_title("Shear Force Diagram")
    axs[1].set_ylabel("Shear Force (kN)")
    axs[1].legend()
    axs[1].grid(True)

    # Bending moment diagram
    axs[2].plot(positions, bending_moments, label="Bending Moment (M)", color='orange', linewidth=2)
    axs[2].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axs[2].set_title("Bending Moment Diagram")
    axs[2].set_ylabel("Moment (kNm)")
    axs[2].legend()
    axs[2].grid(True)

    # Stress distribution
    axs[3].plot(positions, bending_stresses, label="Bending Stress (σ_xx)", color='green', linewidth=2)
    axs[3].plot(positions, shear_stresses, label="Shear Stress (τ_xy)", color='red', linewidth=2)
    axs[3].axhline(0, color='black', linestyle='--', linewidth=0.8)
    axs[3].set_title("Stress Distribution")
    axs[3].set_xlabel("Position along the beam (m)")
    axs[3].set_ylabel("Stress (kN/m²)")
    axs[3].legend()
    axs[3].grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()

def visualize_results_with_reactions(bridge_data, reactions):
    bridge_length = bridge_data['교량 길이']

    # 균열 위치를 포함한 x 좌표 생성
    crack_positions = [crack["position"] for crack in bridge_data["cracks"]]
    positions = np.unique(np.round(np.concatenate((
        np.linspace(0, bridge_length, 200),
        crack_positions
    )), 3))

    tolerance = 1e-3  # 허용 오차

    # 선도 데이터 계산
    shear_forces = []
    bending_moments = []
    bending_stresses = []
    shear_stresses = []

    for x in positions:
        V, M = calculate_shear_moment_with_discontinuity(bridge_data, x, 0, reactions)

        # 균열 위치에서 응력을 0으로 설정
        matching_crack = next((crack for crack in bridge_data["cracks"] if abs(round(crack["position"], 3) - round(x, 3)) < tolerance), None)
        if matching_crack:
            # 균열 위치에서 응력을 0으로 설정
            bending_stresses.append(0)
            shear_stresses.append(0)
        else:
            # 정상적인 응력 계산
            I = bridge_data["단면 2차 모멘트 I"]
            bending_stresses.append(M / I if I > 0 else 0)
            shear_stresses.append(V / (bridge_data["단면 너비"] * bridge_data["단면 높이"]))

        shear_forces.append(V)
        bending_moments.append(M)

    # 선도 출력
    plot_results_with_reactions(positions, reactions, shear_forces, bending_moments, bending_stresses, shear_stresses)


#Quest 1에 실제 작동에 필요한 명령어 코드들

# 전역 딕셔너리 선언
bridge_data = get_bridge_data()

# 교량 데이터 및 반력 계산
reactions = calculate_support_reactions(bridge_data)  # 실제 반력 계산 함수 호출

while True:
    # 위치 정보를 한 번에 입력받아 x, y, z로 나누기
    x, y, z = get_position(bridge_data["교량 길이"], bridge_data["단면 높이"], bridge_data["단면 너비"])

    # Q와 I 계산
    section_width = bridge_data["단면 너비"]
    section_height = bridge_data["단면 높이"]

    Q, I = calculate_section_properties(y, section_width, section_height)

    # Q와 I를 bridge_data에 추가
    update_bridge_data({
        "단면 1차 모멘트 Q": Q,
        "단면 2차 모멘트 I": I
    })                

    # 불연속을 고려하여 전단력과 모멘트 계산
    V_result, M_result = calculate_shear_moment_with_discontinuity(bridge_data, x, y, reactions)

    # 전단응력과 휨응력 계산
    sigma_xx = -M_result * y / bridge_data["단면 2차 모멘트 I"]
    sigma_xy = -V_result * bridge_data["단면 1차 모멘트 Q"] / (bridge_data["단면 2차 모멘트 I"] * bridge_data["단면 너비"])

    
    # 결과 출력 및 부호 규약 설명
    print("\n--- 결과 ---")
    print("반력의 부호규약 (외력): 위(+) 아래(-)")
    print("전단력과 모멘트의 부호규약 (내력 - 우측 단면): 위(-) 아래(+) 시계(-) 반시계(+)")
    print("전단응력과 휨응력의 부호규약: 위(+) 아래(-) 압축(-) 인장(+)")

    print(f"위치 x: {x}, y: {y}, z: {z}")
    print(f"반력 R_A: {reactions['R_A']} kN")
    print(f"반력 R_B: {reactions['R_B']} kN")
    print(f"전단력 (V): {V_result} kN")
    print(f"모멘트 (M): {M_result} kNm")
    print(f"휨응력 (σ_xx): {sigma_xx:.3f} kN/m²")
    print(f"전단응력 (τ_xy): {sigma_xy:.3f} kN/m²")

    # 원래 응력 텐서 계산 및 출력
    stress_tensor = calculate_stress_tensor(sigma_xx, sigma_xy)

    # 주응력 텐서 계산 및 출력
    principal_stress_tensor = calculate_principal_stresses(stress_tensor)

    # Visualize after data input and reaction calculation
    visualize_results_with_reactions(bridge_data, reactions)


    # 응력 시각화 (균열 고려 전)
    X, Y = np.meshgrid(
        np.linspace(0, bridge_data["교량 길이"], 200),  # X는 교량 길이에 따른 좌표
        np.linspace(-bridge_data["단면 높이"] / 2, bridge_data["단면 높이"] / 2, 200)  # Y는 단면 높이에 따른 좌표
    )

    # 휨응력 및 전단응력 계산용 배열 초기화
    sigma_xx_vals = np.zeros_like(Y)
    sigma_xy_vals = np.zeros_like(Y)

    # X, Y 좌표를 순회하며 응력 계산
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x_pos = X[i, j]  # x 좌표
            y_pos = Y[i, j]  # y 좌표

            # 단면 속성 계산 (균열 없음)
            Q, I = calculate_section_properties(y_pos, bridge_data["단면 너비"], bridge_data["단면 높이"])

            if I > 0:
                # 각 x에서의 모멘트(M) 및 전단력(V) 계산
                V_x, M_x = calculate_shear_moment_with_discontinuity(bridge_data, x_pos, y_pos, reactions)
                sigma_xx_vals[i, j] = -M_x * y_pos / I  # 휨응력 계산
                sigma_xy_vals[i, j] = -V_x * Q / (I * bridge_data["단면 너비"])  # 전단응력 계산

    # 휨응력 시각화
    plt.figure(figsize=(12, 6))
    plt.contourf(X, Y, sigma_xx_vals, levels=100, cmap='coolwarm')
    plt.colorbar(label="Bending Stress σ_xx (kPa)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Pre-Crack Bending Stress Distribution (σ_xx)")
    plt.show()

    # 전단응력 시각화
    plt.figure(figsize=(12, 6))
    plt.contourf(X, Y, sigma_xy_vals, levels=100, cmap='Spectral')
    plt.colorbar(label="Shear Stress σ_xy (kPa)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Pre-Crack Shear Stress Distribution (σ_xy)")
    plt.show()



    # 사용자에게 다시 실행 여부 묻기
    repeat = input("\n다른 위치에서 계산하려면 'y'를 입력하세요. 종료하려면 'n'을 입력하세요: ").strip().lower()
    if repeat != 'y':
        print("다음 단계로 넘어갑니다.")
        break

###############################################################################

#Quest2 균열 크기 데이터 입력
def get_crack_data(bridge_length, section_height):
    """
    사용자로부터 교량 균열 위치와 깊이를 입력받아 반환합니다.
    
    Parameters:
    - bridge_length: 교량 길이
    - section_height: 단면 높이
    
    Returns:
    - crack_position: 균열 위치 (x 값)
    - crack_depth: 균열 깊이 (y 값)
    """
    while True:
        try:
            crack_position = float(input(f"균열이 발생한 위치 x를 입력하세요 (0 ~ {bridge_length} m): "))
            if 0 <= crack_position <= bridge_length:
                break
            else:
                print(f"x 값은 0과 {bridge_length} 사이여야 합니다. 다시 입력해주세요.")
        except ValueError:
            print("숫자로 입력해주세요.")
    
    while True:
        try:
            crack_depth = float(input(f"균열의 깊이를 입력하세요 (0 ~ {section_height} m): "))
            if 0 <= crack_depth <= section_height:
                break
            else:
                print(f"균열 깊이는 0과 {section_height} 사이여야 합니다. 다시 입력해주세요.")
        except ValueError:
            print("숫자로 입력해주세요.")
    
    return crack_position, crack_depth


#새로운 Q와 I의 계산
def calculate_section_properties_with_crack(y, section_width, section_height, crack_depth):
    """
    균열 깊이를 고려하여 직사각형 단면의 1차 모멘트 Q와 2차 모멘트 I를 계산합니다.
    
    Parameters:
    - y: 중립축으로부터의 거리
    - section_width: 단면의 너비
    - section_height: 단면의 전체 높이
    - crack_depth: 균열 깊이 (사용할 수 없는 단면 높이)

    Returns:
    - Q: 수정된 단면 1차 모멘트
    - I: 수정된 단면 2차 모멘트
    """
    # 균열로 인해 사용할 수 있는 단면 높이를 계산 (단면 하부에만 균열 발생 가정)
    effective_height = section_height - crack_depth

    # 새로운 중립축 위치 계산
    neutral_axis = effective_height / 2

    # 단면 2차 모멘트 (I)
    if effective_height > 0:
        I = (section_width * effective_height ** 3) / 12
    else:
        I = 0  # 균열이 전체 단면을 차지하면 I는 0

    # 단면 1차 모멘트 (Q)
    if y >= 0:  # 중립축 상부
        effective_y = neutral_axis - y
    else:  # 중립축 하부
        effective_y = neutral_axis + y

    if effective_y > 0:
        area = section_width * effective_y
        centroid_distance = effective_y / 2 + abs(y)    
        Q = area * centroid_distance
    else:
        Q = 0  # 사용할 수 있는 단면이 없으면 Q는 0

    return Q, I

# 기존 코드의 Q와 I 추가 부분 대체

#Quest2 실제 작동 코드

# 균열 데이터를 리스트로 관리
bridge_data["cracks"] = []

# 여러 균열 입력 처리
def input_crack_data():
    """
    균열 데이터를 입력받아 bridge_data["cracks"]를 초기화하고 새로 입력합니다.
    """
    bridge_data["cracks"] = []  # 균열 데이터를 초기화

    while True:
        crack_position, crack_depth = get_crack_data(bridge_data["교량 길이"], bridge_data["단면 높이"])
        bridge_data["cracks"].append({
            "position": crack_position,
            "depth": crack_depth
        })

        while True:  # 올바른 입력을 받을 때까지 반복
            repeat = input("다른 균열을 추가하려면 'y', 종료하려면 'n'을 입력하세요: ").strip().lower()
            if repeat == 'y':
                break  # 추가 입력
            elif repeat == 'n':
                return  # 함수 종료
            else:
                print("경고: 올바른 값을 입력하세요 ('y' 또는 'n').")

# 처음 균열 데이터 입력
input_crack_data()

# 위치 정보 입력 및 계산
while True:
    # 위치 정보를 입력받기
    x, y, z = get_position(bridge_data["교량 길이"], bridge_data["단면 높이"], bridge_data["단면 너비"])

    # 균열 위치 확인 시 허용 오차 추가
    tolerance = 1e-4  # 허용 오차 확대

    # 균열 위치 확인
    matching_crack = next((crack for crack in bridge_data["cracks"] if crack["position"] == x), None)


   # 926 ~ 936 줄의 기존 처리 내용
    if matching_crack:
        crack_depth = matching_crack["depth"]
        print(f"\n균열 위치 {x}m에서 깊이 {crack_depth}m 데이터가 적용됩니다.")

        # 균열 영역 확인
        if -bridge_data["단면 높이"] / 2 - crack_depth/2 <= y <= -bridge_data["단면 높이"] / 2 + crack_depth/2:
            # 균열 영역에 포함되면 응력을 0으로 설정
            sigma_xx = 0
            sigma_xy = 0
            print("경고: 해당 위치는 균열 영역에 포함됩니다. 응력은 0으로 간주됩니다.")
            
            repeat = input("\n다른 위치를 입력하려면 'y', 균열 데이터를 다시 입력하려면 'crack', 프로그램을 종료하시려면 'n'을 입력하세요: ").strip().lower()
            if repeat == 'y':
                continue  # 위치 입력 반복
            elif repeat == 'crack':
                input_crack_data()  # 균열 데이터 초기화 및 재입력
            elif repeat == 'n':
                print("프로그램을 종료합니다.")
                break
    else:
        print(f"\n위치 {x}m에서 균열 데이터가 없습니다. 균열 깊이를 0으로 간주합니다.")
        crack_depth = 0  # 균열이 없으면 깊이 0으로 처리

    # Q와 I 계산
    Q, I = calculate_section_properties_with_crack(y, bridge_data["단면 너비"], bridge_data["단면 높이"], crack_depth)

    if I == 0:
        print("경고: 단면 2차 모멘트 I가 0입니다. 계산을 중단합니다.")
        continue

    # 전단력 및 휨 모멘트 계산
    V_result, M_result = calculate_shear_moment_with_discontinuity(bridge_data, x, y, reactions)

    # 응력 계산
    sigma_xx = -M_result * y / I
    sigma_xy = -V_result * Q / (I * bridge_data["단면 너비"])

    # 결과 출력
    print("\n--- 응력 결과 ---")
    print(f"위치 x: {x}, y: {y}, z: {z}")
    print(f"Q: {Q}, I: {I}")
    print(f"휨응력 (σ_xx): {sigma_xx:.3f} kN/m²")
    print(f"전단응력 (τ_xy): {sigma_xy:.3f} kN/m²")

    # 응력 텐서 출력
    stress_tensor = calculate_stress_tensor(sigma_xx, sigma_xy)
    principal_stress_tensor = calculate_principal_stresses(stress_tensor)

    # 균열 위치를 포함한 x 좌표 생성
    crack_positions = [crack["position"] for crack in bridge_data["cracks"]]
    x_values = np.unique(np.concatenate((
        np.linspace(0, bridge_data["교량 길이"], 200),  # 기존 균등 분할
        crack_positions  # 균열 위치 추가
    )))
    X, Y = np.meshgrid(
        x_values,
        np.linspace(-bridge_data["단면 높이"] / 2, bridge_data["단면 높이"] / 2, 200)
    )


    # 휨응력 및 전단응력 계산용 배열 초기화
    sigma_xx_vals = np.zeros_like(Y)
    sigma_xy_vals = np.zeros_like(Y)

    # X, Y 좌표를 순회하며 응력 계산
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x_pos = X[i, j]  # x 좌표
            y_pos = Y[i, j]  # y 좌표

            # 균열 위치 확인
            matching_crack = next((crack for crack in bridge_data["cracks"] if abs(crack["position"] - x_pos) < tolerance), None)

            if matching_crack:
                crack_depth = matching_crack["depth"]

                # 균열 영역이면 응력을 0으로 설정
                if -bridge_data["단면 높이"] / 2 <= y_pos <= -bridge_data["단면 높이"] / 2 + crack_depth:
                    sigma_xx_vals[i, j] = 0
                    sigma_xy_vals[i, j] = 0
                    continue  # 균열 영역에서 계산 건너뜀

            # 균열 영역이 아니면 기존 응력 계산 로직 적용
            Q, I = calculate_section_properties_with_crack(y_pos, bridge_data["단면 너비"], bridge_data["단면 높이"], 0)

            if I > 0:
                # 각 x에서의 모멘트(M) 및 전단력(V) 계산
                V_x, M_x = calculate_shear_moment_with_discontinuity(bridge_data, x_pos, y_pos, reactions)
                sigma_xx_vals[i, j] = -M_x * y_pos / I  # 휨응력 계산
                sigma_xy_vals[i, j] = -V_x * Q / (I * bridge_data["단면 너비"])  # 전단응력 계산

    # 선도 시각화
    visualize_results_with_reactions(bridge_data, reactions)

    # 휨응력 시각화
    plt.figure(figsize=(12, 6))
    plt.contourf(X, Y, sigma_xx_vals, levels=100, cmap='coolwarm')
    plt.colorbar(label="Bending Stress σ_xx (kPa)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Post-Crack Bending Stress Distribution (σ_xx)")
    plt.show()

    # 전단응력 시각화
    plt.figure(figsize=(12, 6))
    plt.contourf(X, Y, sigma_xy_vals, levels=100, cmap='Spectral')
    plt.colorbar(label="Shear Stress σ_xy (kPa)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Post-Crack Shear Stress Distribution (σ_xy)")
    plt.show()

    # 사용자 입력에 따라 반복 여부 결정
    repeat = input("\n다른 위치를 입력하려면 'y', 균열 데이터를 다시 입력하려면 'crack', 프로그램을 종료하시려면 'n'을 입력하세요: ").strip().lower()
    if repeat == 'y':
        continue
    elif repeat == 'crack':
        input_crack_data()  # 균열 데이터 초기화 및 재입력
    elif repeat == 'n':
        print("프로그램을 종료합니다.")
        break

############################################################################################################

#quest3 파괴여부 판단

import tkinter as tk
from tkinter import messagebox

def get_user_input_gui():
    """
    사용자로부터 극한 응력 값을 입력받는 GUI 인터페이스를 제공합니다.
    """
    root = tk.Tk()
    root.title("극한 응력 값 입력")

    # Label for instructions
    tk.Label(root, text="극한 응력 값을 입력하세요.", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Labels and entry fields for inputs
    tk.Label(root, text="극한 압축응력 (σ_{ult,c}) [MPa]:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    sigma_ult_c_entry = tk.Entry(root)
    sigma_ult_c_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="극한 인장응력 (σ_{ult,t}) [MPa]:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    sigma_ult_t_entry = tk.Entry(root)
    sigma_ult_t_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="극한 전단응력 (τ_{ult}) [MPa]:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    tau_ult_entry = tk.Entry(root)
    tau_ult_entry.grid(row=3, column=1, padx=10, pady=5)

    # Reference ranges
    tk.Label(root, text="참고: 범위", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=5)
    reference_text = (
        "콘크리트:\n"
        "  - 압축: -30 ~ -50 MPa\n"
        "  - 인장: 2 ~ 5 MPa\n"
        "  - 전단: 0.8 ~ 1.2 MPa\n\n"
        "고강도 콘크리트:\n"
        "  - 압축: -60 ~ -100 MPa\n"
        "  - 인장: 5 ~ 10 MPa\n"
        "  - 전단: 1.2 ~ 1.8 MPa\n\n"
        "철근콘크리트:\n"
        "  - 압축: -20 ~ -35 MPa\n"
        "  - 인장: 2 ~ 4 MPa\n"
        "  - 전단: 2 ~ 4 MPa"
    )
    tk.Label(root, text=reference_text, justify="left", font=("Arial", 10), anchor="w").grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    root.grab_set()
    root.focus_force()
    root.after(100, lambda: sigma_ult_c_entry.focus_set())  # 첫 번째 입력 필드에 초점 설정


    def submit():
        try:
            # Parse and validate inputs
            sigma_ult_c = float(sigma_ult_c_entry.get())
            sigma_ult_t = float(sigma_ult_t_entry.get())
            tau_ult = float(tau_ult_entry.get())

            # Validation for inputs
            if sigma_ult_c >= 0:
                raise ValueError("극한 압축응력은 음수여야 합니다.")
            if sigma_ult_t <= 0:
                raise ValueError("극한 인장응력은 양수여야 합니다.")
            if tau_ult <= 0:
                raise ValueError("극한 전단응력은 양수여야 합니다.")

            # Close the GUI with result
            root.result = (sigma_ult_c, sigma_ult_t, tau_ult)
            root.quit()
            root.destroy()

        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))

    def cancel():
        # Exit without saving results
        root.result = None
        root.quit()
        root.destroy()

    # Buttons for submit and cancel
    tk.Button(root, text="결정", command=submit).grid(row=6, column=0, pady=10)
    tk.Button(root, text="취소", command=cancel).grid(row=6, column=1, pady=10)

    # Bind Enter key to trigger the submit function
    root.bind('<Return>', lambda event: submit())

    # Run the GUI event loop
    root.mainloop()

    if hasattr(root, "result") and root.result is not None:
        return root.result
    else:
        raise SystemExit("사용자가 입력을 취소했습니다.")


def calculate_principal_stresses_2d(stress_tensor):
    """
    2D 응력 텐서에서 주응력을 계산합니다.
    """
    # 응력 텐서 값 (kN/m^2 → MPa 변환)
    sigma_xx = stress_tensor[0, 0] * 0.001
    sigma_yy = stress_tensor[1, 1] * 0.001
    tau_xy = stress_tensor[0, 1] * 0.001

    # 평균 응력
    sigma_avg = (sigma_xx + sigma_yy) / 2

    # 반지름 (Mohr의 원)
    R = np.sqrt(((sigma_xx - sigma_yy) / 2) ** 2 + tau_xy ** 2)

    # 주응력 계산
    sigma_1 = sigma_avg + R  # 최대 주응력
    sigma_2 = sigma_avg - R  # 최소 주응력

    return sigma_1, sigma_2



def check_failure_criteria_2d(sigma_1, sigma_2, sigma_ult_c, sigma_ult_t, tau_ult):
    """
    2D 주응력을 기반으로 Mohr의 파괴 기준을 확인합니다.

    Parameters:
    - sigma_1: 최대 주응력
    - sigma_2: 최소 주응력
    - sigma_ult_c: 극한 압축응력
    - sigma_ult_t: 극한 인장응력
    - tau_ult: 극한 전단응력

    Returns:
    - is_safe: True (안전), False (파괴)
    """
    # Mohr의 파괴 기준 검사
    failure = False

    # 1. 최대 인장응력 검사
    if sigma_1 > sigma_ult_t:
        failure = True

    # 2. 최대 압축응력 검사
    if sigma_2 < sigma_ult_c:
        failure = True

    # 3. 최대 전단응력 검사 (Mohr의 원 반지름)
    tau_max = (sigma_1 - sigma_2) / 2
    if abs(tau_max) > tau_ult:
        failure = True

    return not failure

def main(bridge_data, reactions):
    """
    Quest2의 결과값을 기반으로 균열을 고려한 응력 계산 및 Mohr의 파괴 기준에 따른 안전성 평가를 수행합니다.

    Parameters:
    - bridge_data: Quest2에서 계산된 교량 데이터
    - reactions: Quest2에서 계산된 지점 반력
    """
    while True:  # 전체 프로그램 반복
        # 극한 응력 입력
        sigma_ult_c, sigma_ult_t, tau_ult = get_user_input_gui()  # 극한 응력 값 입력

        while True:
            # 위치 입력
            x, y, z = get_position(bridge_data["교량 길이"], bridge_data["단면 높이"], bridge_data["단면 너비"])

            # 균열 위치 확인
            tolerance = 1e-4
            matching_crack = next((crack for crack in bridge_data["cracks"] if abs(crack["position"] - x) < tolerance), None)

            if matching_crack:
                crack_depth = matching_crack["depth"]
                effective_height = bridge_data["단면 높이"] - crack_depth  # 유효 단면 높이
                neutral_axis = effective_height / 2                        # 새로운 중립축

                print(f"\n균열 위치 {x}m에서 깊이 {crack_depth}m 데이터가 적용됩니다.")

                # 균열 영역 확인
                if -bridge_data["단면 높이"] / 2 - crack_depth/2 <= y <= -bridge_data["단면 높이"] / 2 + crack_depth/2:
                    # 균열 내부 영역
                    sigma_xx = 0
                    sigma_xy = 0
                    print("경고: 해당 위치는 균열 영역에 포함됩니다. 응력은 0으로 간주됩니다.")
                elif -neutral_axis < y <= neutral_axis:
                    # 균열을 제외한 유효 단면 영역
                    Q, I = calculate_section_properties_with_crack(
                        y, bridge_data["단면 너비"], bridge_data["단면 높이"], crack_depth
                    )
                    if I > 0:
                        V_result, M_result = calculate_shear_moment_with_discontinuity(
                            bridge_data, x, y, reactions
                        )
                        sigma_xx = -M_result * y / I
                        sigma_xy = -V_result * Q / (I * bridge_data["단면 너비"])
                    else:
                        sigma_xx = 0
                        sigma_xy = 0
                        print("경고: 유효 단면 모멘트(I)가 0입니다. 계산을 중단합니다.")
                else:
                    print("경고: 입력된 y 값이 유효 단면 범위를 벗어났습니다.")
            else:
                # 균열이 없는 경우
                Q, I = calculate_section_properties_with_crack(
                    y, bridge_data["단면 너비"], bridge_data["단면 높이"], 0
                )
                V_result, M_result = calculate_shear_moment_with_discontinuity(
                    bridge_data, x, y, reactions
                )
                sigma_xx = -M_result * y / I if I > 0 else 0
                sigma_xy = -V_result * Q / (I * bridge_data["단면 너비"]) if I > 0 else 0

            # 응력 텐서 생성
            stress_tensor = np.array([
                [sigma_xx, sigma_xy],
                [sigma_xy, 0]  # σ_yy는 0으로 가정
            ])

            # 주응력 계산
            sigma_1, sigma_2 = calculate_principal_stresses_2d(stress_tensor)

            # Mohr의 파괴 기준 적용
            is_safe = check_failure_criteria_2d(sigma_1, sigma_2, sigma_ult_c, sigma_ult_t, tau_ult)

            # 결과 출력
            tau_max = abs((sigma_1 - sigma_2) / 2)
            print("\n--- 응력 결과 ---")
            print(f"위치 x: {x}, y: {y}, z: {z}")
            print(f"휨응력 (σ_xx): {sigma_xx:.3f} kN/m²")
            print(f"전단응력 (τ_xy): {sigma_xy:.3f} kN/m²")
            print("===== 주응력 분석 결과 =====")
            print(f"  σ1 = {sigma_1:.3f} MPa")
            print(f"  σ2 = {sigma_2:.3f} MPa")
            print(f"최대 전단응력 (τ_max): {tau_max:.3f} MPa")
            print("\n===== 입력된 극한 강도 =====")
            print(f"극한 압축 강도 (σ_ult,c): {sigma_ult_c:.3f} MPa")
            print(f"극한 인장 강도 (σ_ult,t): {sigma_ult_t:.3f} MPa")
            print(f"극한 전단 강도 (τ_ult): {tau_ult:.3f} MPa")
            print(f"구조물 상태: {'안전' if is_safe else '파괴 발생'}")

            # Call the function to plot
            plot_mohr_failure(sigma_ult_c, sigma_ult_t, tau_ult, sigma_1, sigma_2)

            # 사용자 입력에 따라 종료 여부 결정
            repeat = input("\n다른 위치를 입력하려면 'y', 극한 응력 값을 다시 입력하려면 'reset', 프로그램을 종료하시려면 'n'을 입력하세요: ").strip().lower()
            if repeat == 'y':
                continue
            elif repeat == 'reset':
                break  # 새로운 극한 응력 값 입력
            elif repeat == 'n':
                print("프로그램을 종료합니다.")
                return  # 프로그램 완전 종료



def plot_mohr_failure(sigma_ult_c, sigma_ult_t, tau_ult, sigma_1, sigma_2):
    """
    Plot the Mohr failure envelope, shear stress limit, and principal stresses.

    Parameters:
    - sigma_ult_c: Ultimate compressive stress (negative value)
    - sigma_ult_t: Ultimate tensile stress (positive value)
    - tau_ult: Ultimate shear stress (positive value)
    - sigma_1: Principal stress 1
    - sigma_2: Principal stress 2
    """
    # Calculate tau_max and Mohr circle center
    tau_max = abs((sigma_1 - sigma_2) / 2)
    center = (sigma_1 + sigma_2) / 2  # Mohr circle center

    # Define common colors
    boundary_color = 'red'      # 붉은색 외곽선
    fill_color = 'lightcoral'   # 연한 붉은색 내부 채우기

    # 1사분면: 극한 인장 응력을 기준으로 정사각형 정의
    q1_x = [0, sigma_ult_t, sigma_ult_t, 0, 0]
    q1_y = [0, 0, sigma_ult_t, sigma_ult_t, 0]

    # 3사분면: 극한 압축 응력을 기준으로 정사각형 정의
    q3_x = [0, sigma_ult_c, sigma_ult_c, 0, 0]
    q3_y = [0, 0, sigma_ult_c, sigma_ult_c, 0]

    # 2사분면: 주어진 수식 적용
    sigma_2_vals = np.linspace(0, sigma_ult_t, 500)
    sigma_1_vals_2nd = sigma_ult_c * (1 - (sigma_2_vals / sigma_ult_t))

    # 4사분면: 주어진 수식 적용
    sigma_1_vals = np.linspace(0, sigma_ult_t, 500)
    sigma_2_vals_4th = sigma_ult_c * (1 - (sigma_1_vals / sigma_ult_t))

    # Set up the plot
    plt.figure(figsize=(10, 10))

    # Fill the interior with a light red color
    plt.fill(q1_x, q1_y, color=fill_color, alpha=0.3)  # 1st Quadrant Interior
    plt.fill(q3_x, q3_y, color=fill_color, alpha=0.3)  # 3rd Quadrant Interior
    plt.fill_betweenx(sigma_2_vals, sigma_1_vals_2nd, 0, color=fill_color, alpha=0.3)  # 2nd Quadrant Interior
    plt.fill_between(sigma_1_vals, sigma_2_vals_4th, 0, color=fill_color, alpha=0.3)  # 4th Quadrant Interior

    # Draw the boundary lines with red color
    plt.plot(q1_x, q1_y, color=boundary_color, linewidth=2)  # 1st Quadrant Boundary
    plt.plot(q3_x, q3_y, color=boundary_color, linewidth=2)  # 3rd Quadrant Boundary
    plt.plot(sigma_1_vals_2nd, sigma_2_vals, color=boundary_color, linewidth=2)  # 2nd Quadrant Boundary
    plt.plot(sigma_1_vals, sigma_2_vals_4th, color=boundary_color, linewidth=2, label="Failure Area")  # 4th Quadrant Boundary

    # Define the shear stress limit circle with the same center as the Mohr circle
    theta = np.linspace(0, 2 * np.pi, 500)
    shear_circle_x = center + tau_ult * np.cos(theta)  # Adjusted to Mohr circle center
    shear_circle_y = tau_ult * np.sin(theta)

    # Plot the shear stress limit circle
    plt.plot(shear_circle_x, shear_circle_y, label="Shear Stress Limit", color="orange", linestyle="--")

    # Plot the Mohr circle
    mohr_circle_x = center + tau_max * np.cos(theta)
    mohr_circle_y = tau_max * np.sin(theta)
    plt.plot(mohr_circle_x, mohr_circle_y, 'b-', label="Mohr's Circle")

    # Plot principal stresses
    plt.scatter([sigma_1, sigma_2], [0, 0], color='red', zorder=5, label="Principal Stresses (σ₁, σ₂)")

    # Set axis labels and legend
    plt.xlabel("Normal Stress (σ) [MPa]", fontsize=12)
    plt.ylabel("Shear Stress (τ) [MPa]", fontsize=12)
    plt.title("Mohr Failure Envelope and Principal Stresses", fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()


#quest3 실행코드(간편화)

 # Main 실행
main(bridge_data, reactions)
