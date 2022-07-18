import asyncio


async def sleep(tic=1):
    for _ in range(tic):
        await asyncio.sleep(0)


def load_frames(frames_filepath: list, double: bool = False) -> list[str]:
    frames = []
    for frame_filepath in frames_filepath:
        with open(frame_filepath, "r") as file:
            frame = file.read()
            if double:
                frames.extend([frame, frame])
            else:
                frames.append(frame)

    return frames
