from typing import Any
from typing import Type

from core.base.error_messages import HastTableErrorMessages
from core.base.exceptions import HastTableIndexException
from core.base.exceptions import HastTableSizeException


class HashTable(object):

    def __init__(self, size: int):
        if size < 1:
            raise HastTableSizeException(HastTableErrorMessages.SIZE_ERROR)

        self.__size: int = size
        self.__hash_table: list[list[tuple]] = self.__create_buckets()

    def __create_buckets(self) -> list[list]:
        return [[] for _ in range(self.__size)]

    def __found_key(self, key: str) -> tuple[list[tuple], bool, int | None, Any | None]:
        hashed_key = hash(key) % self.__size

        bucket = self.__hash_table[hashed_key]

        is_found, index, record_key, record_val = False, None, None, None
        for index, record in enumerate(bucket):
            record_key, record_val = record

            if record_key == key:
                is_found = True
                break

        return bucket, is_found, index, record_val

    def set(self, key, value) -> None:
        bucket, is_found, index, _ = self.__found_key(key)

        if is_found:
            bucket[index] = (key, value)  # type: ignore
        else:
            bucket.append((key, value))

    __setitem__ = set

    def get(self, key, default=None) -> Any:
        _, is_found, _, record_val = self.__found_key(key)

        if is_found:
            return record_val
        return default

    def __getitem__(self, key) -> Any:
        _, is_found, _, record_val = self.__found_key(key)
        if is_found:
            return record_val
        raise HastTableIndexException(HastTableErrorMessages.INDEX_ERROR % key)

    def delete(self, key, default=None):
        bucket, is_found, index, _ = self.__found_key(key)

        if is_found:
            return bucket.pop(index)
        return default

    def __delitem__(self, key):
        bucket, is_found, index, _ = self.__found_key(key)
        if is_found:
            bucket.pop(index)
            return
        raise HastTableIndexException(HastTableErrorMessages.INDEX_ERROR % key)

    def __str__(self):
        return "".join(str(item) for item in self.__hash_table)


hashtable: Type[HashTable] = HashTable
