from typing import Annotated

from pydantic import BaseModel, Field


class PlayArgs(BaseModel):
    playlist: str
    song_number: Annotated[int, Field(alias='song-number')]


def play(args: PlayArgs) -> None:
    print(f'Handle rpc "play" with args: {args}')
