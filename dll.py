import win32pipe
import win32file
import struct


def receive(pipe: int) -> str:
    recieved = win32file.ReadFile(
        pipe, struct.unpack("i", win32file.ReadFile(pipe, 4)[1])[0]
    )[1]

    message: str = recieved.decode()

    return message


def send(pipe: int, msg: str) -> bool:
    data: bytes = msg.encode() + b"\0"
    win32file.WriteFile(pipe, struct.pack("i", len(data)))
    win32file.WriteFile(pipe, data)
    return True


def create_pipe() -> int:
    pipe: int = win32pipe.CreateNamedPipe(
        r"\\.\pipe\boogie",
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE
        | win32pipe.PIPE_READMODE_MESSAGE
        | win32pipe.PIPE_WAIT,
        1,
        65536,
        65536,
        0,
        None,
    )

    return pipe


def wait_for_connect(pipe: int):
    win32pipe.ConnectNamedPipe(pipe, None)


def close(pipe: int):
    win32file.CloseHandle(pipe)
