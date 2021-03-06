import base64
import sys

import pyDes

DES_KEY = "11272737"
DES_IV = "11272737"
MAGIC_SUFFIX = "Buy272737"


def get_volume_serial_number(root_path_name: str = "C:\\") -> int:
    """
    获取逻辑卷序列号
    """
    assert sys.platform == 'win32'
    from ctypes import POINTER, byref, c_bool, c_int, c_uint, c_wchar_p, windll

    f = windll.kernel32.GetVolumeInformationW
    f.argtypes = [
        c_wchar_p,
        POINTER(c_wchar_p),
        c_uint,
        POINTER(c_int),
        POINTER(c_uint),
        POINTER(c_uint),
        POINTER(c_wchar_p),
        c_uint,
    ]
    f.restype = c_bool

    volume_serial_number = c_int()
    if f(
        c_wchar_p(root_path_name),
        None,
        0,
        byref(volume_serial_number),
        None,
        None,
        None,
        0,
    ):
        return volume_serial_number.value
    return 0


def get_des() -> pyDes.des:
    """
    获取des实例，防止复用实例造成数据干扰
    """
    return pyDes.des(
        DES_KEY, mode=pyDes.CBC, IV=DES_IV, pad=None, padmode=pyDes.PAD_PKCS5
    )


def encrypt(plain_text: str) -> str:
    """
    加密
    """
    try:
        data = plain_text.encode("utf-8")
        result = base64.b64encode(get_des().encrypt(data))
        return result.decode("utf-8")
    except:
        return None


def decrypt(cipher_text: str) -> str:
    """
    解密
    """
    try:
        data = cipher_text.encode("utf-8")
        result = get_des().decrypt(base64.b64decode(data))
        return result.decode("utf-8")
    except:
        return None


def default_serial_number() -> str:
    """
    获取本机序列号（明码）
    """
    volume_serial_number = get_volume_serial_number("C:\\")
    return str(volume_serial_number)


def calc_registration_code(serial_number: str) -> str:
    """
    获取注册码（明码）
    """
    if serial_number:
        return serial_number + MAGIC_SUFFIX
    return None


def print_help_then_exit():
    print("非Windows 系统只能根据序列号计算注册码，不能获取默认序列号以及注册码。")
    sys.exit(-1)


def print_sn_and_rc(cipher_sn: str = None):
    if cipher_sn is None:
        plain_sn = default_serial_number()
        cipher_sn = encrypt(plain_sn)
    else:
        plain_sn = decrypt(cipher_sn)

    if plain_sn is None:
        print("序列号无法识别！")
        return

    plain_rc = calc_registration_code(plain_sn)
    cipher_rc = encrypt(plain_rc)

    print(f"序列号：{cipher_sn}")
    print(f"注册码：{cipher_rc}")


def main():
    if len(sys.argv) != 1:
        cipher_sn = "".join(sys.argv[1:])
        print_sn_and_rc(cipher_sn)
        return

    if sys.platform == "win32":
        print_sn_and_rc()
        return

    print_help_then_exit()


if __name__ == "__main__":
    main()
