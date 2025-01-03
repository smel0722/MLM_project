import win32gui
import win32con
import win32api
import subprocess
import time
import logging
from typing import Dict, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('MainTab_Functions')

class MainTabFunctions:
    def __init__(self):
        self.window_positions = {}

    def execute_program(self, program_path: str, count: int) -> Tuple[bool, str]:
        """執行程式指定次數"""
        try:
            logger.info(f"開始執行程式: {program_path}, 次數: {count}")
            for i in range(count):
                subprocess.Popen(
                    ['start', '', program_path], 
                    shell=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                time.sleep(0.3)
            logger.info("程式執行完成")
            return True, f"成功執行程式 {count} 次"
        except Exception as e:
            error_msg = f"執行錯誤: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def get_screen_info(self) -> List[Dict]:
        """獲取所有螢幕的資訊"""
        try:
            screens = []
            # 獲取主螢幕資訊
            main_screen = {
                'left': 0,
                'top': 0,
                'width': win32api.GetSystemMetrics(win32con.SM_CXSCREEN),
                'height': win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            }
            screens.append(main_screen)

            # 檢查是否有第二螢幕
            if win32api.GetSystemMetrics(win32con.SM_CMONITORS) > 1:
                # 獲取虛擬螢幕的總大小
                virtual_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
                virtual_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
                virtual_left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
                virtual_top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

                # 如果虛擬螢幕的寬度大於主螢幕，表示有右側螢幕
                if virtual_width > main_screen['width']:
                    second_screen = {
                        'left': main_screen['width'],
                        'top': 0,
                        'width': virtual_width - main_screen['width'],
                        'height': virtual_height
                    }
                    screens.append(second_screen)
                
            logger.info(f"成功獲取螢幕資訊: {screens}")
            return screens
            
        except Exception as e:
            error_msg = f"獲取螢幕資訊時發生錯誤: {str(e)}"
            logger.error(error_msg)
            return []

    def calculate_window_capacity(self, screen_info: Dict, window_width: int, window_height: int) -> Tuple[int, int]:
        """計算螢幕可以容納多少視窗"""
        horizontal = screen_info['width'] // window_width
        vertical = screen_info['height'] // window_height
        return horizontal, vertical

    def manage_windows(self, title: str, window_width: int, window_height: int, remove_title: bool = False, dont_movewindow: bool = False, remove_border: bool = False, bypass_limit: bool = False) -> Tuple[bool, str]:
        """管理指定標題的視窗"""
        try:
            screens = self.get_screen_info()
            if not screens:
                return False, "無法獲取螢幕資訊"
            
            current_windows = []
            def enum_callback(hwnd: int, results: list):
                if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if window_title == title:
                        results.append(hwnd)
            win32gui.EnumWindows(enum_callback, current_windows)
            
            if not current_windows:
                return False, "找不到指定標題的視窗"

            existing_hwnds = set(self.window_positions.keys())
            current_hwnds = set(current_windows)
            new_hwnds = current_hwnds - existing_hwnds
            removed_hwnds = existing_hwnds - current_hwnds

            for hwnd in removed_hwnds:
                del self.window_positions[hwnd]
            
            used_positions = set((pos['x'], pos['y']) for pos in self.window_positions.values())
            available_positions = []
            
            for screen in screens:
                h_count, v_count = self.calculate_window_capacity(screen, window_width, window_height)
                for row in range(v_count):
                    for col in range(h_count):
                        x = screen['left'] + (col * window_width)
                        y = screen['top'] + (row * window_height)
                        if (x, y) not in used_positions:
                            available_positions.append((x, y))
            
            # dont_movewindow 為 True 時僅移動到當前位置
            if dont_movewindow:
                for hwnd in current_windows:
                    rect = win32gui.GetWindowRect(hwnd)
                    current_x, current_y = rect[0], rect[1]

                    self.window_positions[hwnd] = {
                        'x': current_x,
                        'y': current_y,
                        'order': len(self.window_positions) + 1
                    }

                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    if remove_title:
                        style &= ~win32con.WS_CAPTION
                    if remove_border:
                        style &= ~win32con.WS_THICKFRAME
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

                    win32gui.SetWindowPos(
                        hwnd,
                        None,
                        current_x,
                        current_y,
                        window_width,
                        window_height,
                        win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED
                    )
                return True, "視窗已移動到當前位置，但未進行排序"

            # 檢查是否有足夠空間
            if not bypass_limit and len(new_hwnds) > len(available_positions):
                return False, "螢幕空間不足，請關閉多餘的視窗"

            # 生成額外位置（若 bypass_limit 為 True）
            if bypass_limit and len(new_hwnds) > len(available_positions):
                extra_needed = len(new_hwnds) - len(available_positions)
                for i in range(extra_needed):
                    last_x = available_positions[-1][0] + window_width if available_positions else 0
                    last_y = available_positions[-1][1] if available_positions else 0
                    available_positions.append((last_x, last_y))
            
            for hwnd, (x, y) in zip(new_hwnds, available_positions):
                self.window_positions[hwnd] = {
                    'x': x,
                    'y': y,
                    'order': len(self.window_positions) + 1
                }
            
            for hwnd in current_windows:
                if hwnd in self.window_positions:
                    pos = self.window_positions[hwnd]

                    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    if remove_title:
                        style &= ~win32con.WS_CAPTION
                    if remove_border:
                        style &= ~win32con.WS_THICKFRAME
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

                    win32gui.SetWindowPos(
                        hwnd,
                        None,
                        pos['x'],
                        pos['y'],
                        window_width,
                        window_height,
                        win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED
                    )
            
            return True, f"成功處理 {len(current_windows)} 個視窗"

        except Exception as e:
            error_msg = f"管理視窗時發生錯誤: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def update_window_title(self, hwnd: int, new_title: str) -> Tuple[bool, str]:
        """更新視窗標題"""
        try:
            if not win32gui.IsWindow(hwnd):
                return False, "無效的視窗控制代碼"
                
            win32gui.SetWindowText(hwnd, new_title)
            return True, "成功更新視窗標題"
            
        except Exception as e:
            error_msg = f"更新視窗標題時發生錯誤: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def update_window_style(self, hwnd: int, remove_title: bool, remove_border: bool) -> Tuple[bool, str]:
        """更新視窗樣式"""
        try:
            if not win32gui.IsWindow(hwnd):
                return False, "無效的視窗控制代碼"
                
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            
            if remove_title:
                style &= ~win32con.WS_CAPTION
            else:
                style |= win32con.WS_CAPTION
                
            if remove_border:
                style &= ~win32con.WS_THICKFRAME
            else:
                style |= win32con.WS_THICKFRAME
                
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            win32gui.SetWindowPos(
                hwnd, None, 0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED
            )
            
            return True, "成功更新視窗樣式"
            
        except Exception as e:
            error_msg = f"更新視窗樣式時發生錯誤: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def update_window_position(self, hwnd: int, x: int, y: int, width: int, height: int) -> Tuple[bool, str]:
        """更新視窗位置"""
        try:
            if not win32gui.IsWindow(hwnd):
                return False, "無效的視窗控制代碼"

            win32gui.SetWindowPos(
                hwnd,
                None,
                x,
                y,
                width,
                height,
                win32con.SWP_NOZORDER
            )
            return True, "成功更新視窗位置"

        except Exception as e:
            error_msg = f"更新視窗位置時發生錯誤: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def get_window_list(self) -> List[Dict]:
        """獲取已管理視窗的列表"""
        window_list = []
        for hwnd, info in self.window_positions.items():
            if win32gui.IsWindow(hwnd):
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                has_caption = bool(style & win32con.WS_CAPTION)
                has_border = bool(style & win32con.WS_THICKFRAME)
                
                window_list.append({
                    'order': info['order'],
                    'title': win32gui.GetWindowText(hwnd),
                    'hwnd': hwnd,
                    'X': info['x'],
                    'Y': info['y'],
                    'has_caption': has_caption,
                    'has_border': has_border
                })
        
        return sorted(window_list, key=lambda x: x['order'])