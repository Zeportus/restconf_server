import logging
from typing import Annotated

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PlayArgs(BaseModel):
    playlist: str
    song_number: Annotated[int, Field(alias='song-number')]


def play(args: PlayArgs) -> None:
    logger.info(f'Handle rpc "play" with args: {args}')
