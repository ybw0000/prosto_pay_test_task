from typing import Type

import pytest

from core.base.error_messages import HastTableErrorMessages
from core.base.exceptions import HastTableIndexException
from core.base.exceptions import HastTableSizeException
from core.base.hashtable import hashtable


@pytest.mark.parametrize(
    argnames=("size", "expected_exception", "exception_message"),
    argvalues=(
        (0, HastTableSizeException, HastTableErrorMessages.SIZE_ERROR),
        (-1, HastTableSizeException, HastTableErrorMessages.SIZE_ERROR),
    ),
)
def test_initialize_fails(size: int, expected_exception: Type[Exception], exception_message: str):
    """Initialize with invalid size"""
    with pytest.raises(expected_exception, match=exception_message):
        hashtable(size)


@pytest.mark.parametrize(
    argnames="size",
    argvalues=(1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 154),
)
def test_initialize_success(size: int):
    """Initialize with valid size"""
    assert hashtable(size)


def test_set_item_by_method():
    """Test set item by method"""
    data = hashtable(1)
    data.set("some_key", "some_value")


def test_set_item_by_index():
    """Test set item by index"""
    data = hashtable(1)
    data["some_key"] = "some_value"


def test_set_item_with_collision():
    """Test set item with collision"""
    data = hashtable(1)
    data.set("some_key", "some_value")
    data["some_key2"] = "some_value2"


def test_get_item_by_method_1():
    """Success test get item by method"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    assert data.get("some_key") == "some_value"


def test_get_item_by_method_2():
    """Test get item by method using the wrong key without default value"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    assert data.get("some_key2") is None


def test_get_item_by_method_3():
    """Test get item by method using the wrong key with default value"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    assert data.get("some_key2", "HELLO") == "HELLO"


def test_get_item_by_index_success():
    """Success test get item by index"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    assert data["some_key"] == "some_value"


def test_get_item_by_index_fails():
    """Failure test get item by index"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    with pytest.raises(HastTableIndexException, match=HastTableErrorMessages.INDEX_ERROR % "some_key2"):
        _ = data["some_key2"]


def test_get_item_with_collision():
    """Test get item with collision"""
    data = hashtable(1)
    data.set("some_key", "some_value")
    data["some_key2"] = "some_value2"

    assert data["some_key2"] == "some_value2"
    assert data.get("some_key") == "some_value"


def test_delete_item_by_method_success_1():
    """Success test delete item by method"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    data.delete("some_key")
    assert data.get("some_key") is None


def test_delete_item_by_method_success_2():
    """Success test delete item by method with default value"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    assert data.delete("some_key2", "HELLO") == "HELLO"


def test_delete_item_by_method_success_3():
    """Failure test delete item by method without default value"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    data.delete("some_key2")


def test_delete_item_by_index_success():
    """Test delete item by index"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    del data["some_key"]
    assert data.get("some_key") is None


def test_delete_item_by_index_fails():
    """Test delete item by index"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    with pytest.raises(HastTableIndexException, match=HastTableErrorMessages.INDEX_ERROR % "some_key2"):
        del data["some_key2"]


def test_delete_item_with_collision():
    """Test delete item with collision"""
    data = hashtable(1)
    data["some_key"] = "some_value"
    data["some_key2"] = "some_value2"
    del data["some_key"]
    assert data["some_key2"] == "some_value2"
